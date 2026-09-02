# ========== 5.2 电梯 vs 过山车 ==========
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)

axes[0].plot(x, stock_a, 'o-', color='#007AFF', linewidth=2.5, markersize=8)
axes[0].set_title('股票 A · 像坐电梯\n上涨平稳', fontsize=12)
axes[0].set_xticks(x)
axes[0].set_xticklabels(days, fontsize=9)
axes[0].grid(True, alpha=0.3)

axes[1].plot(x, stock_b, 's-', color='#E82127', linewidth=2.5, markersize=8)
peak = np.maximum.accumulate(stock_b)
axes[1].fill_between(x, stock_b, peak, alpha=0.35, color='#E82127', label='从高点回落')
axes[1].set_title('股票 B · 像坐过山车\n大起大落', fontsize=12)
axes[1].set_xticks(x)
axes[1].set_xticklabels(days, fontsize=9)
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)

for ax in axes:
    ax.set_ylabel('价格')

fig.suptitle('市场中的「不稳定程度」不同', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()