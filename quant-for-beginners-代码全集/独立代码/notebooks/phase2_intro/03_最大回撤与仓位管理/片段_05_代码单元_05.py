# ========== 双均线策略：满仓 vs 半仓 ==========
MA_SHORT, MA_LONG = 5, 20                        # 短/长均线窗口（交易日）
HALF_SIZE         = 0.5                          # 半仓 = 50% 资金参与

df = pd.DataFrame({'Close': prices, 'Return': returns}).dropna()  # 对齐价格与收益
df['MA_S'] = df['Close'].rolling(MA_SHORT).mean()   # 短期均线
df['MA_L'] = df['Close'].rolling(MA_LONG).mean()    # 长期均线
df['Signal'] = (df['MA_S'] > df['MA_L']).astype(float)  # 1=多头, 0=空仓
df['StratRet'] = df['Signal'].shift(1) * df['Return']     # 次日按昨日信号交易（无未来函数）
df = df.dropna()                                 # 去掉 MA 暖机期的 NaN

df['Equity_100'] = buy_hold_equity(df['StratRet'])              # 满仓净值
df['Equity_50']  = buy_hold_equity(df['StratRet'] * HALF_SIZE) # 半仓：收益按仓位缩放
df['Equity_BH']  = buy_hold_equity(df['Return'])               # 买入持有对照

scenarios = [                                    # 统一遍历，避免重复代码
    ('双均线 · 满仓', 'Equity_100'),
    ('双均线 · 半仓', 'Equity_50'),
    ('买入持有',      'Equity_BH'),
]

print('最大回撤对比：')
for label, col in scenarios:
    dd = max_drawdown(df[col])                   # 复用上文工具函数
    print(f'  {label:12s}: {dd:.2%}')
