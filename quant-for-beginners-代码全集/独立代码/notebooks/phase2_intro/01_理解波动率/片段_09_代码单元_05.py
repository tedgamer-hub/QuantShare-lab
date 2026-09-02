# ========== 5.4 标准差 ≈ 波动率 ==========
def step_returns(prices):
    return pd.Series(prices).pct_change().dropna()

r_a = step_returns(stock_a)
r_b = step_returns(stock_b)
vol_a = float(r_a.std())
vol_b = float(r_b.std())

print('── 玩具案例（5.1）──')
print(f'股票 A 日波动率(标准差): {vol_a:.2%}')
print(f'股票 B 日波动率(标准差): {vol_b:.2%}')
print(f'B 约为 A 的 {vol_b / vol_a:.0f} 倍\n')

daily_vol = float(df['return'].std())
print('── AAPL 真实数据 ──')
print(f'日波动率(标准差): {daily_vol:.4%}')
print(f'粗略直觉: 典型单日涨跌幅度大约在 ±{daily_vol:.2%} 附近')