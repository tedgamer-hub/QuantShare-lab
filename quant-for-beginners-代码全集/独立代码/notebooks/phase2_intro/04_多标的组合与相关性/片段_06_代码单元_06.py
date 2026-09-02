# ========== 等权组合 vs SPY 净值（第二期收官图）==========
equity_port = buy_hold_equity(port_returns)            # 等权组合买入持有净值
equity_spy  = buy_hold_equity(returns['SPY'])          # SPY 大盘买入持有净值

fig, ax = plt.subplots(figsize=(12, 5))              # 宽幅画布，便于看长期走势
fig.patch.set_facecolor('#FAFAFA')                   # 画布背景
ax.set_facecolor('#FFFFFF')                          # 绘图区背景

ax.plot(                                               # 绘制等权组合净值曲线
    equity_port.index, equity_port,                    # x=日期，y=净值
    color='#007AFF', linewidth=1.6,                    # 蓝色实线
    label='等权组合 (AAPL+MSFT+JPM+XLE)',             # 图例文字
)                                                      # 第一条 plot 结束
ax.plot(                                               # 绘制 SPY 大盘净值曲线
    equity_spy.index, equity_spy,                      # x=日期，y=SPY 净值
    color='#FF9500', linewidth=1.5, linestyle='--',  # 橙色虚线
    label='SPY 大盘',                                  # 图例文字
)                                                      # 第二条 plot 结束

ax.set_title('等权组合 vs 标普500：净值对比（AkShare · 约 3 年）', fontsize=14)  # 标题
ax.set_ylabel('净值（起点=1）')                        # 纵轴
ax.set_xlabel('日期')                                  # 横轴
ax.legend(loc='upper left', framealpha=0.92)         # 图例：左上角
ax.grid(True, linestyle='--', alpha=0.35)            # 虚线网格
plt.tight_layout()                                     # 调整边距
plt.show()                                             # 显示图表
