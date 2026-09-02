# ========== 5.5 三票波动率 PK ==========
TICKERS = ['AAPL', 'TSLA', 'NVDA']
NAMES = {'AAPL': '苹果', 'TSLA': '特斯拉', 'NVDA': '英伟达'}
COLORS = ['#007AFF', '#E82127', '#76B900']

multi_raw = yf.download(TICKERS, period='2y', progress=False)
multi_close = multi_raw['Close']
multi_rets = multi_close.pct_change().dropna()

records = []
ann_vols = []
for t in TICKERS:
    r = multi_rets[t]
    dvol = float(r.std())
    avol = dvol * np.sqrt(TRADING_DAYS)
    aret = float((1 + r.mean()) ** TRADING_DAYS - 1)
    ann_vols.append(avol)
    records.append({
        '名称': NAMES[t],
        '日波动率': f'{dvol:.2%}',
        '年化波动率': f'{avol:.2%}',
        '年化收益(约)': f'{aret:.2%}',
    })

vol_table = pd.DataFrame(records, index=TICKERS)
print('波动率对比表：')
display(vol_table)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar([NAMES[t] for t in TICKERS], [v * 100 for v in ann_vols],
              color=COLORS, edgecolor='white', linewidth=1.2)
ax.set_ylabel('年化波动率 (%)')
ax.set_title('谁最稳？谁最刺激？· 年化波动率柱状图', fontsize=14)
ax.grid(True, axis='y', alpha=0.3)
for bar, v in zip(bars, ann_vols):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{v:.1%}', ha='center', fontsize=11)
plt.tight_layout()
plt.show()

rank = sorted(zip(TICKERS, ann_vols), key=lambda x: x[1])
print(f"最稳: {NAMES[rank[0][0]]} ({rank[0][1]:.1%})")
print(f"最刺激: {NAMES[rank[-1][0]]} ({rank[-1][1]:.1%})")