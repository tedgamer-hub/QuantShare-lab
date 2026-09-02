# ========== 环境准备：导入库 + 量化小工具 ==========
import warnings                                   # 导入警告控制模块
warnings.filterwarnings('ignore')              # 隐藏次要警告，Notebook 输出更干净

import statistics as stats                      # 标准库：均值、中位数、标准差
import numpy as np                              # 数值计算（协方差、开方等）
import pandas as pd                             # 表格数据处理
import matplotlib.pyplot as plt                 # 绘图
import akshare as ak                            # 国内金融数据接口（本章拉美股）
import time                                     # 批量请求间隔，避免触发接口限速

plt.rcParams['font.sans-serif'] = [              # 跨平台中文字体回退
    'PingFang SC', 'Microsoft YaHei', 'SimHei',
    'Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans',
]
plt.rcParams['axes.unicode_minus'] = False      # 坐标轴负号正常显示

TRADING_DAYS = 252                              # 美股常用年化交易日数


def annualize_return(daily_returns: pd.Series) -> float:
    """日收益率 → 年化收益率（复利近似）。"""
    mean_daily = daily_returns.mean()           # 日收益算术平均
    return (1 + mean_daily) ** TRADING_DAYS - 1  # 复利外推至 252 个交易日


def annualize_volatility(daily_returns: pd.Series) -> float:
    """日收益率 → 年化波动率。"""
    daily_std = daily_returns.std()             # 日收益标准差
    return daily_std * np.sqrt(TRADING_DAYS)    # 日波动 × √252 → 年化波动


def sharpe_ratio(daily_returns: pd.Series, rf_annual: float) -> float:
    """简化夏普：(年化收益 − 无风险利率) / 年化波动。"""
    ann_ret = annualize_return(daily_returns)   # 先算年化收益
    ann_vol = annualize_volatility(daily_returns)  # 再算年化波动
    excess = ann_ret - rf_annual                # 超额收益 = 收益 − 无风险
    return excess / ann_vol                     # 每单位风险对应的超额回报


def beta_vs_market(stock: pd.Series, market: pd.Series) -> tuple[float, float]:
    """numpy 与 pandas 双算法计算 Beta，便于交叉验证。"""
    cov = np.cov(stock, market)                 # 2×2 协方差矩阵 [[Var股, Cov], [Cov, Var市]]
    beta_numpy = cov[0, 1] / cov[1, 1]          # Cov(股, 市) / Var(市)
    beta_pandas = stock.cov(market) / market.var()  # pandas 等价写法
    return beta_numpy, beta_pandas              # 返回双结果供对照


print('环境就绪 ✓')                               # 提示：环境加载完成
