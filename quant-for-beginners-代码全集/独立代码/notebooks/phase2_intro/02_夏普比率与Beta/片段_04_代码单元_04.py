# ========== Beta：相对 SPY 的敏感度（numpy ⟷ pandas 对照）==========
MARKET = returns['SPY']                            # 大盘基准（标普 500 ETF）
STOCKS = [t for t in tickers if t != 'SPY']       # 其余 9 只个股，逐一算 Beta

beta_rows = []                                     # 收集每只股票的 Beta 结果
for ticker in STOCKS:                              # 遍历 9 只个股
    stock = returns[ticker]                        # 该股日收益率序列
    b_np, b_pd = beta_vs_market(stock, MARKET)     # numpy / pandas 双算法
    beta_rows.append({                             # 追加一行结果
        '股票': ticker,
        'Beta(numpy)':  b_np,
        'Beta(pandas)': b_pd,
    })

beta_df = pd.DataFrame(beta_rows).set_index('股票')  # 转为表格，股票代码作行索引

print('Beta 相对 SPY（β>1 比大盘更冲，β<1 更稳）：')
display(beta_df.map('{:.2f}'.format))              # 保留两位小数展示
