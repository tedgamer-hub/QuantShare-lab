# ========== 5.3 收益率曲线 + 直方图 ==========
TICKER = 'AAPL'
raw = yf.download(TICKER, period='1y', progress=False)
df = pd.DataFrame({'Close': get_close(raw, TICKER)})
df['return'] = df['Close'].pct_change()
df = df.dropna().copy()

df['cum_return'] = (1 + df['return']).cumprod() - 1

fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

axes[0].plot(df.index, df['cum_return'] * 100, color='#007AFF', linewidth=1.5)
axes[0].axhline(0, color='gray', linestyle='--', linewidth=0.8)
axes[0].set_title(f'{TICKER} · 累计收益率曲线', fontsize=13)
axes[0].set_ylabel('累计收益率 (%)')
axes[0].grid(True, alpha=0.3)

axes[1].hist(df['return'] * 100, bins=30, color='#007AFF', alpha=0.75, edgecolor='white')
axes[1].axvline(0, color='black', linestyle='--', linewidth=0.8)
axes[1].set_title(f'{TICKER} · 日收益率直方图', fontsize=13)
axes[1].set_xlabel('日收益率 (%)')
axes[1].set_ylabel('天数')

fig.suptitle('用收益率观察波动：直方图越「散」，日常越颠', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

print(f'样本: {len(df)} 个交易日')
print(f'累计收益: {df["cum_return"].iloc[-1]:.2%}')