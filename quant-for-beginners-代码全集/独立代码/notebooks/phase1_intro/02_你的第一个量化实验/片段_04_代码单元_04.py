# ========== 配图2：最近8天 OHLC 示意图 ==========
sample = aapl.tail(8).copy()   # 取最后 8 个交易日
dates = range(len(sample))     # 0,1,...,7 用作横轴位置

fig, ax = plt.subplots(figsize=(12, 5))  # 创建子图

for i, (idx, row) in enumerate(sample.iterrows()):  # 逐行遍历每一天
    o, h, l, c = row['Open'], row['High'], row['Low'], row['Close']  # 开高低收
    color = 'tab:red' if c < o else 'tab:green'   # 收跌红色、收涨绿色
    ax.vlines(i, l, h, color=color, linewidth=2, alpha=0.85)   # 竖线：最低到最高
    ax.hlines(o, i - 0.15, i + 0.15, color=color, linewidth=2)  # 开盘价短横线
    ax.hlines(c, i - 0.15, i + 0.15, color=color, linewidth=3)  # 收盘价粗横线

ax.set_xticks(dates)  # 设置横轴刻度位置
ax.set_xticklabels([d.strftime('%m-%d') for d in sample.index], rotation=45)  # 日期标签
ax.set_ylabel('价格 (美元)')  # 设置子图纵轴
ax.set_title('最近 8 个交易日：竖线 = High↔Low，短横线 = Open / Close（粗线=收盘）', fontsize=13)  # 设置子图标题
ax.grid(True, axis='y', alpha=0.3)  # 显示网格

from matplotlib.lines import Line2D  # 自定义图例用的小线段
legend_elements = [  # 自定义图例项
    Line2D([0], [0], color='tab:green', linewidth=2, label='收涨日 (Close ≥ Open)'),  # 线宽
    Line2D([0], [0], color='tab:red', linewidth=2, label='收跌日 (Close < Open)'),  # 线宽
]                                              # 数组拼接结束
ax.legend(handles=legend_elements, loc='upper left')  # 显示图例
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片

print('小贴士：一天之内，价格一定满足  Low ≤ Open, Close ≤ High')  # 打印小贴士
