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
