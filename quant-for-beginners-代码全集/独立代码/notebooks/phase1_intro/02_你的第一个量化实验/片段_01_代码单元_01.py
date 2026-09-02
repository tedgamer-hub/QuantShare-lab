# ========== 环境准备：导入库并设置画图中文 ==========
import warnings                          # 导入警告控制模块
warnings.filterwarnings('ignore')  # 忽略次要警告，输出更干净

import numpy as np           # 数值计算
import pandas as pd          # 表格数据处理
import matplotlib.pyplot as plt  # 绘图
import yfinance as yf        # 下载雅虎财经股票数据（需联网）

plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows 黑体；Mac 可改 PingFang SC
plt.rcParams['axes.unicode_minus'] = False     # 负号正常显示

print('环境就绪 ✓')                       # 提示：环境加载完成
