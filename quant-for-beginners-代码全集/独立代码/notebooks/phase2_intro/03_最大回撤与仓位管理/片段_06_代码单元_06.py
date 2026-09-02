# ========== 三条净值曲线：仓位如何改变命运 ==========
STYLE = {                                        # 线型 / 颜色 / 粗细
    'Equity_100': dict(color='#007AFF', lw=1.6, ls='-',  label='双均线 · 满仓'),
    'Equity_50':  dict(color='#34C759', lw=1.6, ls='-',  label='双均线 · 半仓'),
    'Equity_BH':  dict(color='#8E8E93', lw=1.3, ls='--', label='买入持有'),
}

fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor('#FAFAFA')
ax.set_facecolor('#FFFFFF')

for col, kw in STYLE.items():                    # 同一循环画三条曲线
    ax.plot(df.index, df[col], **kw)

ax.set_title(f'{TICKER} 双均线（{MA_SHORT}/{MA_LONG}）· 仓位对比 · AkShare 行情', fontsize=14)
ax.set_ylabel('净值')
ax.set_xlabel('日期')
ax.legend(loc='upper left', framealpha=0.92)
ax.grid(True, linestyle='--', alpha=0.35)

plt.tight_layout()
plt.show()
