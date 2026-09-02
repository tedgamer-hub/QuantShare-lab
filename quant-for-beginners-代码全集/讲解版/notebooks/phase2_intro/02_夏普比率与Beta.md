# 02_夏普比率与Beta：代码片段与讲解

来源 Notebook：`notebooks/phase2_intro/02_夏普比率与Beta.ipynb`

下列片段严格按照原 Notebook 的代码单元顺序排列。代码内容保持原样；说明用于帮助理解，不属于原始代码。

## 代码片段 01：环境准备：导入库 + 量化小工具

- 原始位置：`notebooks/phase2_intro/02_夏普比率与Beta.ipynb · cell[4]`
- 所属小节：环境准备
- 用途：计算风险收益指标，把收益表现与承担的波动或市场风险联系起来。
- 处理过程：导入本段所需的计算、数据处理或绘图库；利用协方差与方差计算 Beta，衡量相对大盘的敏感度；计算夏普比率，用单位风险对应的超额收益评价表现；计算标准差或年化波动率以刻画风险；封装可复用函数，减少后续单元中的重复计算；打印关键数值，便于核验中间结果和最终指标。
- 运行结果：终端/单元格文字摘要。
- 代码特点：环境准备、风险指标、波动分析、函数封装、结果展示
- 主要依赖：warnings、statistics、numpy、pandas、matplotlib.pyplot、akshare、time、matplotlib

### 原始代码

```python
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
```

---

## 代码片段 02：下载行情 → 日收益 → 年化指标与 Sharpe

- 原始位置：`notebooks/phase2_intro/02_夏普比率与Beta.ipynb · cell[6]`
- 所属小节：指标拓展与现实应用
- 用途：下载并整理真实市场数据，为本章后续计算和绘图建立数据基础。
- 处理过程：通过 AkShare 获取美股历史行情并整理日期与价格字段；从价格序列计算相邻交易日收益率；利用协方差与方差计算 Beta，衡量相对大盘的敏感度；计算夏普比率，用单位风险对应的超额收益评价表现；计算标准差或年化波动率以刻画风险；封装可复用函数，减少后续单元中的重复计算。
- 运行结果：Notebook 表格、终端/单元格文字摘要。
- 代码特点：联网数据、收益率计算、风险指标、波动分析、函数封装
- 主要依赖：pandas、akshare
- 使用提示：Notebook 代码通常按顺序共享变量；单独运行本片段前，请先运行其前置单元。

### 原始代码

```python
# ========== 下载行情 → 日收益 → 年化指标与 Sharpe ==========
# 数据链：akshare → ak.stock_us_daily() → 新浪财经美股日线（联网，非模拟）

tickers = [                                      # 共 10 只：9 只个股 + 1 只大盘 ETF
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META',    # 科技巨头
    'NVDA', 'TSLA', 'AMD',  'JPM',              # 高波动成长 + 银行对照
    'SPY',                                       # 标普 500 ETF，作 Beta 基准
]
period_years = 3                                 # 回溯约 3 年
rf_annual    = 0.04                              # 无风险利率近似 4%

start_date = (                                   # 计算样本起始日
    pd.Timestamp.today()                         # 今天
    - pd.DateOffset(years=period_years, days=30) # 往前 3 年，多留 30 天缓冲
).strftime('%Y-%m-%d')                           # 格式化为 'YYYY-MM-DD'

print(f'akshare 版本: {ak.__version__}')         # 打印库版本，便于排查
print('接口: ak.stock_us_daily(symbol, adjust="qfq")  # 新浪财经 · 前复权')


def fetch_us_close(symbol: str, start: str) -> pd.Series:
    """联网拉取单只美股前复权收盘价，并按起始日裁剪。"""
    df = ak.stock_us_daily(symbol=symbol, adjust='qfq')  # 发起 HTTP 请求
    if df is None or df.empty:                     # 网络/接口异常时主动报错
        raise RuntimeError(f'{symbol} 未返回数据，请检查网络或 akshare 版本')

    df['date'] = pd.to_datetime(df['date'])        # 字符串 → 日期类型
    close = (                                      # 整理为以日期为索引的收盘价序列
        df.set_index('date')                       # 日期列设为行索引
          .sort_index()                             # 按时间升序排列
          ['close']                                 # 只保留收盘价列
          .rename(symbol)                           # Series 命名 = 股票代码
    )
    return close.loc[close.index >= start]         # 截取 start 之后的样本


print(f'\n正在下载 {len(tickers)} 只美股（约 {period_years} 年）…')
frames = {}
for t in tickers:
    frames[t] = fetch_us_close(t, start_date)
    time.sleep(1)                                # 新浪接口限速，连续请求间隔 1 秒
prices = pd.DataFrame(frames).dropna()           # 宽表：每列一只股票

returns = prices.pct_change().dropna()             # 简单日收益率 r_t = P_t/P_{t-1} − 1

api_tail = ak.stock_us_daily(symbol='AAPL', adjust='qfq').tail(1)  # 再拉一次 API 末行作核验
print('\n【核验】AAPL 接口原始末行（AkShare 直接返回）：')
display(api_tail)                                  # Notebook 内美观显示表格
print(f'样本区间：{prices.index[0].date()} → {prices.index[-1].date()}，共 {len(returns)} 个交易日')
print(f'AAPL 末收（对齐后）: {prices["AAPL"].iloc[-1]:.2f}')  # 应与 api_tail 的 close 一致

metrics = pd.DataFrame({                           # 数值版指标表（供后续作图）
    t: {                                           # 每列对应一只 ticker
        '年化收益': annualize_return(returns[t]),
        '年化波动': annualize_volatility(returns[t]),
        'Sharpe': sharpe_ratio(returns[t], rf_annual),
    }
    for t in tickers                               # 遍历全部 10 只
}).T.rename_axis('股票')                            # 转置后行 = 股票代码

summary = metrics.copy()                           # 复制一份用于格式化展示
summary['年化收益'] = summary['年化收益'].map('{:.2%}'.format)  # 收益 → 百分比字符串
summary['年化波动'] = summary['年化波动'].map('{:.2%}'.format)  # 波动 → 百分比字符串
summary['Sharpe']   = summary['Sharpe'].map('{:.2f}'.format)    # Sharpe 保留两位小数

print('\n风险收益一览（近似 Sharpe）：')
display(summary)                                   # 展示格式化后的汇总表
```

---

## 代码片段 03：风险-收益散点图（横轴波动 · 纵轴收益 · 10 只标的）

- 原始位置：`notebooks/phase2_intro/02_夏普比率与Beta.ipynb · cell[8]`
- 所属小节：6.2 风险收益散点图
- 用途：把本节的核心数据或计算结果可视化，使趋势和差异更直观。
- 处理过程：导入本段所需的计算、数据处理或绘图库；通过循环批量处理多个标的、参数或交易区间；把价格、收益、风险或策略结果绘制成图。
- 运行结果：图表。
- 代码特点：环境准备、批量处理、数据可视化
- 主要依赖：matplotlib.ticker、matplotlib
- 使用提示：Notebook 代码通常按顺序共享变量；单独运行本片段前，请先运行其前置单元。

### 原始代码

```python
# ========== 风险-收益散点图（横轴波动 · 纵轴收益 · 10 只标的）==========
from matplotlib.ticker import FuncFormatter       # 坐标轴百分比格式化工具

PALETTE = {                                         # 10 只股票各配一色，图例清晰
    'AAPL':  '#007AFF', 'MSFT':  '#00A4EF', 'GOOGL': '#4285F4',
    'AMZN':  '#FF9900', 'META':  '#0668E1', 'NVDA':  '#76B900',
    'TSLA':  '#E82127', 'AMD':   '#ED1C24', 'JPM':   '#006747',
    'SPY':   '#FF9500',
}

fig, ax = plt.subplots(figsize=(10, 7))            # 10 个点，画布略放大
fig.patch.set_facecolor('#FAFAFA')                # 画布浅灰底
ax.set_facecolor('#FFFFFF')                       # 绘图区白底

for ticker, row in metrics.iterrows():            # 复用上格 metrics，避免重复计算
    vol = row['年化波动']                          # 横坐标：年化波动
    ret = row['年化收益']                          # 纵坐标：年化收益
    color = PALETTE.get(ticker, '#666666')        # 取调色板颜色，缺省灰色
    ax.scatter(
        vol, ret,                                 # 单点坐标
        s=140,                                    # 点的大小
        c=color,                                  # 填充色
        edgecolors='white',                       # 白边，点与点更易区分
        linewidths=1.0,
        label=ticker,                             # 图例标签
        zorder=3,                                 # 图层顺序（点在网格之上）
        alpha=0.90,                               # 轻微透明
    )
    ax.annotate(
        ticker,                                   # 标注文字 = 代码
        (vol, ret),                               # 锚点坐标
        textcoords='offset points',               # 偏移量单位 = 像素点
        xytext=(6, 5),                            # 文字相对锚点的偏移
        fontsize=9,                               # 10 只时字号略小，防重叠
        fontweight='bold',
        color=color,
    )

pct = FuncFormatter(lambda x, _pos: f'{x:.0%}')     # 0.25 显示为 25%
ax.xaxis.set_major_formatter(pct)                 # 横轴百分比格式
ax.yaxis.set_major_formatter(pct)                 # 纵轴百分比格式

ax.set_xlabel('年化波动率', fontsize=12)           # 横轴标题
ax.set_ylabel('年化收益率', fontsize=12)           # 纵轴标题
ax.set_title('风险-收益散点图（10 只 · 约 3 年 · AkShare 行情）', fontsize=14, pad=12)
ax.grid(True, linestyle='--', alpha=0.35)         # 虚线网格，轻量不抢戏
ax.legend(loc='upper left', ncol=2, fontsize=9, framealpha=0.9)  # 两列图例省空间
plt.tight_layout()                                # 自动调整边距
plt.show()                                        # 在 Notebook 中显示图表
```

---

## 代码片段 04：Beta：相对 SPY 的敏感度（numpy ⟷ pandas 对照）

- 原始位置：`notebooks/phase2_intro/02_夏普比率与Beta.ipynb · cell[10]`
- 所属小节：6.3 Beta：相对大盘的敏感度
- 用途：计算风险收益指标，把收益表现与承担的波动或市场风险联系起来。
- 处理过程：利用协方差与方差计算 Beta，衡量相对大盘的敏感度；通过循环批量处理多个标的、参数或交易区间；以表格形式展示数据样本或计算结果；打印关键数值，便于核验中间结果和最终指标。
- 运行结果：Notebook 表格、终端/单元格文字摘要。
- 代码特点：风险指标、批量处理、结果展示
- 主要依赖：pandas
- 使用提示：Notebook 代码通常按顺序共享变量；单独运行本片段前，请先运行其前置单元。

### 原始代码

```python
# ========== Beta：相对 SPY 的敏感度（numpy ⟷ pandas 对照）==========
MARKET = returns['SPY']                            # 大盘基准（标普 500 ETF）
STOCKS = [t for t in tickers if t != 'SPY']       # 其余 9 只个股，逐一算 Beta

beta_rows = []                                     # 收集每只股票的 Beta 结果
for ticker in STOCKS:                              # 遍历 9 只个股
    stock = returns[ticker]                        # 该股日收益率序列
    b_np, b_pd = beta_vs_market(stock, MARKET)     # numpy / pandas 双算法
    beta_rows.append({                             # 追加一行结果
        '股票': ticker,
        'Beta(numpy)':  b_np,
        'Beta(pandas)': b_pd,
    })

beta_df = pd.DataFrame(beta_rows).set_index('股票')  # 转为表格，股票代码作行索引

print('Beta 相对 SPY（β>1 比大盘更冲，β<1 更稳）：')
display(beta_df.map('{:.2f}'.format))              # 保留两位小数展示
```

---

## 代码片段 05：statistics 标准库：AAPL 日收益分布快照

- 原始位置：`notebooks/phase2_intro/02_夏普比率与Beta.ipynb · cell[12]`
- 所属小节：6.4 用 statistics 看收益分布
- 用途：完成“6.4 用 statistics 看收益分布”小节中的计算或数据处理任务。
- 处理过程：打印关键数值，便于核验中间结果和最终指标。
- 运行结果：终端/单元格文字摘要。
- 代码特点：结果展示
- 主要依赖：依赖前序单元中已创建的变量，或仅使用 Python 内置能力
- 使用提示：Notebook 代码通常按顺序共享变量；单独运行本片段前，请先运行其前置单元。

### 原始代码

```python
# ========== statistics 标准库：AAPL 日收益分布快照 ==========
aapl_daily = returns['AAPL'].dropna().tolist()     # Series → list，供 statistics 使用

print('── AAPL 日收益率分布（statistics 标准库）──')  # 分隔标题
print(f'均值:       {stats.mean(aapl_daily):>8.4%}')    # 算术平均（易受极端值影响）
print(f'中位数:     {stats.median(aapl_daily):>8.4%}')  # 50% 分位，更抗极端值
print(f'标准差:     {stats.pstdev(aapl_daily):>8.4%}')  # 总体标准差（除以 N）
print(f'最大单日涨: {max(aapl_daily):>8.2%}')           # 样本内最佳单日表现
print(f'最大单日跌: {min(aapl_daily):>8.2%}')           # 样本内最差单日表现
```

---

## 代码片段 06：🎯 挑战任务（第六章通关）

- 原始位置：`notebooks/phase2_intro/02_夏普比率与Beta.ipynb · cell[14]`
- 所属小节：🎯 挑战任务（第六章通关）
- 用途：这是原仓库保留的空代码单元，用作练习、挑战题填写区或章节间隔。
- 处理过程：原单元没有任何可执行语句，因此这里按原样保留为空文件。
- 运行结果：无输出；学习者可在此补写自己的实验代码。
- 代码特点：空白练习单元、结构占位
- 主要依赖：无

### 原始代码

_原仓库中的这个代码单元为空；独立代码目录中保留了对应的空文件。_

---
