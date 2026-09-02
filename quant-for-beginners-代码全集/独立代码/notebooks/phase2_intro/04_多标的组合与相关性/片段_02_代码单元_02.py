# ========== 下载多标的并对齐（AkShare · 宽表）==========
TICKERS      = ['AAPL', 'MSFT', 'JPM', 'XLE', 'SPY']  # 4 只个股/ETF + 大盘 SPY
PERIOD_YEARS = 3                                       # 回溯约 3 年

print(f'akshare 版本: {ak.__version__}')                 # 打印库版本，便于排查
print('接口: ak.stock_us_daily(symbol, adjust="qfq")')   # 说明数据来源

prices  = fetch_us_prices(TICKERS, PERIOD_YEARS)       # 收盘价宽表：行=日期，列=标的
returns = prices.pct_change().dropna()                 # 简单日收益率 r_t = P_t/P_{t-1}−1

print(f'\n样本: {len(returns)} 个交易日 × {len(TICKERS)} 只标的')  # 样本规模
print(f'区间: {returns.index[0].date()} → {returns.index[-1].date()}')  # 起止日期
display(returns.head())                                # 预览前 5 行
