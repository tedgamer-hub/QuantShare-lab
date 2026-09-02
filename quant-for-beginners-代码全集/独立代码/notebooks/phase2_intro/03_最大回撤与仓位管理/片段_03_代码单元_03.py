# ========== 下载 AAPL → 买入持有净值 → 最大回撤 ==========
TICKER       = 'AAPL'                            # 演示标的
PERIOD_YEARS = 3                                 # 回溯约 3 年

print(f'akshare 版本: {ak.__version__}')
print('接口: ak.stock_us_daily(symbol, adjust="qfq")  # 新浪财经 · 前复权')

prices  = fetch_us_close(TICKER, PERIOD_YEARS)   # 收盘价序列（DatetimeIndex）
returns = prices.pct_change().dropna()           # 简单日收益率 r_t = P_t/P_{t-1} − 1
equity  = buy_hold_equity(returns)               # 买入持有净值曲线

drawdown = compute_drawdown(equity)              # 逐日回撤序列（≤ 0）
max_dd   = max_drawdown(equity)                  # 整段样本最深回撤
worst_dt = drawdown.idxmin()                     # 回撤最深的那一天

print(f'\n样本区间：{prices.index[0].date()} → {prices.index[-1].date()}，共 {len(returns)} 个交易日')
print(f'{TICKER} 买入持有 · 最大回撤: {max_dd:.2%}')
print(f'回撤最深日期: {worst_dt.date()}')
print(f'末收（AkShare）: {prices.iloc[-1]:.2f}')
