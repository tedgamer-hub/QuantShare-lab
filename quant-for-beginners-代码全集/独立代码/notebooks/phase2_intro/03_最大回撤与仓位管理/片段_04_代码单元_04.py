# ========== 净值 + 水下曲线（Underwater Plot）==========
running_peak = equity.cummax()                    # 历史最高净值（用于上图虚线）

PALETTE = dict(equity='#007AFF', underwater='#E82127')  # 统一配色

fig, (ax1, ax2) = plt.subplots(
    2, 1,                                       # 上下两个子图
    figsize=(12, 7),
    sharex=True,                                # 共用横轴（日期）
    gridspec_kw={'height_ratios': [2, 1]},      # 上图占 2/3 高度
)
fig.patch.set_facecolor('#FAFAFA')             # 画布浅灰底

ax1.set_facecolor('#FFFFFF')
ax1.plot(equity.index, equity, color=PALETTE['equity'], linewidth=1.6, label='买入持有净值')
ax1.plot(running_peak.index, running_peak, color='gray', linestyle='--', alpha=0.55, label='历史最高')
ax1.set_title(f'{TICKER} 买入持有净值 & 回撤（水下曲线 · AkShare）', fontsize=14)
ax1.set_ylabel('净值（起点=1）')
ax1.legend(loc='upper left')
ax1.grid(True, linestyle='--', alpha=0.35)

ax2.set_facecolor('#FFFFFF')
ax2.fill_between(drawdown.index, drawdown, 0, color=PALETTE['underwater'], alpha=0.45)
ax2.axhline(max_dd, color='#333333', linestyle=':', linewidth=1.2, label=f'最大回撤 {max_dd:.1%}')
ax2.set_ylabel('回撤')
ax2.set_xlabel('日期')
ax2.legend(loc='lower left')
ax2.grid(True, linestyle='--', alpha=0.35)

plt.tight_layout()                              # 自动调整边距
plt.show()                                      # 在 Notebook 中显示
