# ========== 环境准备：导入库 + 回撤 / 仓位工具函数 ==========
import warnings                                   # 导入警告控制模块
warnings.filterwarnings('ignore')              # 隐藏次要警告，输出更干净

import statistics as stats                      # 标准库：均值、中位数等
import numpy as np                              # 数值计算
import pandas as pd                             # 表格数据处理
import matplotlib.pyplot as plt                 # 绘图
import akshare as ak                            # 国内金融数据接口（本章拉美股）

plt.rcParams['font.sans-serif'] = [              # 跨平台中文字体回退
    'PingFang SC', 'Microsoft YaHei', 'SimHei',
    'Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans',
]
plt.rcParams['axes.unicode_minus'] = False      # 坐标轴负号正常显示

TRADING_DAYS = 252                              # 美股常用年化交易日数


def fetch_us_close(symbol: str, years: float = 3.0) -> pd.Series:
    """联网拉取美股前复权收盘价（AkShare → 新浪财经）。"""
    start = (
        pd.Timestamp.today()
        - pd.DateOffset(years=years, days=30)   # 多留缓冲，避免边界缺数据
    ).strftime('%Y-%m-%d')
    df = ak.stock_us_daily(symbol=symbol, adjust='qfq')  # 发起 HTTP 请求
    if df is None or df.empty:                   # 网络异常时主动报错
        raise RuntimeError(f'{symbol} 未返回数据，请检查网络或 akshare 版本')
    df['date'] = pd.to_datetime(df['date'])      # 字符串 → 日期
    close = (
        df.set_index('date')                     # 日期作索引
          .sort_index()                          # 时间升序
          ['close']                              # 只保留收盘价
          .loc[lambda s: s.index >= start]       # 截取样本区间
          .rename(symbol)                        # Series 命名 = 代码
    )
    return close


def buy_hold_equity(daily_returns: pd.Series) -> pd.Series:
    """买入持有：日收益连乘 → 净值曲线（起点 ≈ 1）。"""
    return (1 + daily_returns).cumprod()


def compute_drawdown(equity: pd.Series) -> pd.Series:
    """回撤序列 = 当前净值 / 历史最高净值 − 1（≤ 0）。"""
    running_peak = equity.cummax()               # 截至当日的历史最高净值
    return equity / running_peak - 1             # 相对高点的跌幅


def max_drawdown(equity: pd.Series) -> float:
    """最大回撤 = 回撤序列中的最小值（最深的那次坑）。"""
    return compute_drawdown(equity).min()


print('环境就绪 ✓')                               # 提示：环境加载完成