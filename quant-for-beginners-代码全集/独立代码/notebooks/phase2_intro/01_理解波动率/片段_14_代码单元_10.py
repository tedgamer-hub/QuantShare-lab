# ========== 5.8 挑战 Starter 代码 ==========
# ── Lv.1：换一只股票 ──
lv1_ticker = 'AMD'
lv1_raw = yf.download(lv1_ticker, period='1y', progress=False)
lv1_ret = get_close(lv1_raw, lv1_ticker).pct_change().dropna()
lv1_ann_vol = float(lv1_ret.std() * np.sqrt(TRADING_DAYS))
print(f'[Lv.1] {lv1_ticker} 年化波动率: {lv1_ann_vol:.2%}')

# ── Lv.2：加入 MSFT ──
lv2_tickers = ['AAPL', 'TSLA', 'NVDA', 'MSFT']
lv2_raw = yf.download(lv2_tickers, period='1y', progress=False)['Close']
lv2_rets = lv2_raw.pct_change().dropna()
lv2_vols = lv2_rets.std() * np.sqrt(TRADING_DAYS)
print('\n[Lv.2] 含 MSFT 的年化波动率：')
print(lv2_vols.sort_values(ascending=False).map(lambda x: f'{float(x):.2%}'))

# ── Lv.3：收益率分布图（以 MSFT 为例）──
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(lv2_rets['MSFT'] * 100, bins=30, color='#00A4EF', alpha=0.75, edgecolor='white')
ax.axvline(0, color='black', linestyle='--', linewidth=0.8)
ax.set_title('[Lv.3] MSFT 日收益率分布', fontsize=13)
ax.set_xlabel('日收益率 (%)')
ax.set_ylabel('天数')
plt.tight_layout()
plt.show()

# ── Lv.4：近 1 年波动率最高的股票 ──
candidates = ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'AMD', 'META', 'NFLX', 'COIN']
cand_raw = yf.download(candidates, period='1y', progress=False)['Close']
cand_vols = cand_raw.pct_change().dropna().std() * np.sqrt(TRADING_DAYS)
cand_vols = cand_vols.sort_values(ascending=False)
print('\n[Lv.4] 近 1 年年化波动率排名：')
for t, v in cand_vols.items():
    print(f'  {t}: {float(v):.2%}')
print(f'\n🏆 波动率最高: {cand_vols.index[0]} ({float(cand_vols.iloc[0]):.2%})')