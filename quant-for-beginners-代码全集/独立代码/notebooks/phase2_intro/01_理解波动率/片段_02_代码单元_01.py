# ========== 环境准备 ==========
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

plt.rcParams['font.sans-serif'] = [              # 跨平台中文字体回退
    'PingFang SC', 'Microsoft YaHei', 'SimHei',
    'Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans',
]
plt.rcParams['axes.unicode_minus'] = False

TRADING_DAYS = 252   # 美股一年大约 252 个交易日


def get_close(data, ticker=None):
    """兼容 yfinance 单标的 / 多标的返回格式"""
    close = data['Close']
    if isinstance(close, pd.DataFrame):
        return close[ticker] if ticker else close.squeeze()
    return close

print('环境就绪 ✓')