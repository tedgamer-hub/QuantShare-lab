# ========== 5.7 小实验：10 个点风险-收益散点 ==========
EXP_TICKERS = ['KO', 'JPM', 'AAPL', 'MSFT', 'META', 'NVDA', 'TSLA', 'COIN']
EXP_NAMES = {
    'KO': '可口可乐', 'JPM': '摩根大通', 'AAPL': '苹果', 'MSFT': '微软',
    'META': 'Meta', 'NVDA': '英伟达', 'TSLA': '特斯拉', 'COIN': 'Coinbase',
}
EXP_COLORS = ['#8B4513', '#003366', '#007AFF', '#00A4EF', '#0668E1', '#76B900', '#E82127', '#1652F0']

def annual_stats(series):
    s = series.dropna()
    return {
        'ret': float((1 + s.mean()) ** TRADING_DAYS - 1),
        'vol': float(s.std() * np.sqrt(TRADING_DAYS)),
    }

exp_raw = yf.download(EXP_TICKERS, period='2y', progress=False)['Close']
exp_rets = exp_raw.pct_change().dropna()

fig, ax = plt.subplots(figsize=(10, 7))

for t, c in zip(EXP_TICKERS, EXP_COLORS):
    st = annual_stats(exp_rets[t])
    ax.scatter(st['vol'], st['ret'], s=130, color=c, edgecolors='white', linewidth=1.2, zorder=3)
    ax.annotate(EXP_NAMES[t], (st['vol'], st['ret']),
                xytext=(6, 5), textcoords='offset points', fontsize=9)

ax.scatter(0.50, 0.40, s=200, facecolors='none', edgecolors='#333', linewidths=2,
           linestyle='--', label='选项 A · 40% / 50%', zorder=2)
ax.scatter(0.10, 0.20, s=200, facecolors='none', edgecolors='#333', linewidths=2,
           linestyle='--', label='选项 B · 20% / 10%', zorder=2)

ax.set_xlabel('年化波动率 →  风险 / 持有体验')
ax.set_ylabel('年化收益率 →  预期回报')
ax.set_title('5 年不能卖：10 个点，你会选哪个？', fontsize=14)
ax.legend(loc='upper left', fontsize=8, ncol=2)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print('── 10 个点一览（近 2 年历史）──')
rows = []
for t in EXP_TICKERS:
    st = annual_stats(exp_rets[t])
    rows.append({'名称': EXP_NAMES[t], '年化收益': f"{st['ret']:.1%}", '年化波动': f"{st['vol']:.1%}"})
rows.append({'名称': '选项 A（虚构）', '年化收益': '40.0%', '年化波动': '50.0%'})
rows.append({'名称': '选项 B（虚构）', '年化收益': '20.0%', '年化波动': '10.0%'})
display(pd.DataFrame(rows))