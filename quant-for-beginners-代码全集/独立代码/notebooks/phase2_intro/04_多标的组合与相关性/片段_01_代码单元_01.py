# ========== 环境准备：导入库 + 多标的 / 组合工具函数 ==========
import warnings                                   # 导入警告控制模块
warnings.filterwarnings('ignore')              # 隐藏次要警告，Notebook 输出更干净

import statistics as stats                      # 标准库：均值、中位数等
import numpy as np                              # 数值计算、矩阵运算
import pandas as pd                             # 表格数据处理
import matplotlib.pyplot as plt                 # 绘图
import akshare as ak                            # 国内金融数据接口（本章拉美股/ETF）
import time                                     # 批量请求间隔，避免触发接口限速

plt.rcParams['font.sans-serif'] = [              # 跨平台中文字体回退
    'PingFang SC', 'Microsoft YaHei', 'SimHei',
    'Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans',
]
plt.rcParams['axes.unicode_minus'] = False      # 坐标轴负号正常显示

TRADING_DAYS = 252                              # 美股常用年化交易日数


def fetch_us_close(symbol: str, years: float = 3.0) -> pd.Series:  # 工具：拉取单只美股/ETF 收盘价
    """联网拉取单只美股/ETF 前复权收盘价。"""                      # 函数文档字符串
    start = (                                    # 计算样本起始日字符串
        pd.Timestamp.today()                     # 今天
        - pd.DateOffset(years=years, days=30)   # 往前 years 年，多留 30 天缓冲
    ).strftime('%Y-%m-%d')                       # 格式化为 'YYYY-MM-DD'
    df = ak.stock_us_daily(symbol=symbol, adjust='qfq')  # 发起 HTTP 请求 · 前复权
    if df is None or df.empty:                   # 网络/接口异常
        raise RuntimeError(f'{symbol} 未返回数据，请检查网络或 akshare 版本')  # 主动报错
    df['date'] = pd.to_datetime(df['date'])      # 字符串 → datetime
    close = (                                    # 整理为收盘价 Series
        df.set_index('date')                     # 日期列 → 行索引
          .sort_index()                          # 按时间升序
          ['close']                              # 只保留收盘价
          .loc[lambda s: s.index >= start]       # 截取 start 之后
          .rename(symbol)                        # 命名 = 股票代码
    )                                              # 链式调用结束，得到 close Series
    return close                                 # 返回单标的收盘价序列


def fetch_us_prices(tickers: list[str], years: float = 3.0) -> pd.DataFrame:  # 工具：批量下载宽表
    """批量下载并宽表对齐：列 = 标的，行 = 日期。"""                      # 函数文档字符串
    frames = {}
    for t in tickers:
        frames[t] = fetch_us_close(t, years)
        time.sleep(1)                            # 新浪接口限速，连续请求间隔 1 秒
    return pd.DataFrame(frames).dropna()         # 宽表对齐，删缺失行（非共同交易日）


def annualize_volatility(daily_returns: pd.Series) -> float:  # 工具：日收益 → 年化波动
    """日收益率 → 年化波动率（σ · √252）。"""                      # 函数文档字符串
    daily_std = daily_returns.std()             # 日收益标准差
    return daily_std * np.sqrt(TRADING_DAYS)    # 日波动 × √252


def equal_weight_returns(returns: pd.DataFrame, tickers: list[str]) -> pd.Series:  # 工具：等权组合日收益
    """等权组合日收益 = 各成分日收益的逐行平均。"""                  # 函数文档字符串
    subset = returns[tickers]                    # 取出组合成分列
    return subset.mean(axis=1)                   # axis=1：每行求平均 → 等权


def buy_hold_equity(daily_returns: pd.Series) -> pd.Series:  # 工具：买入持有净值曲线
    """买入持有净值 = 日收益连乘（起点 ≈ 1）。"""                  # 函数文档字符串
    growth = 1 + daily_returns                   # 日增长因子 1+r_t
    return growth.cumprod()                        # 连乘 → 净值曲线


print('环境就绪 ✓')                               # 提示：环境加载完成
