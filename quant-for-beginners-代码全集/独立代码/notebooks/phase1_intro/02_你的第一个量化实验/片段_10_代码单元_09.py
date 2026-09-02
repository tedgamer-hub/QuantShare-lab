# ========== 小实验：下载三只股票并算波动 ==========
tickers = {  # 要对比的股票列表
    'AAPL': '苹果',  # 字典字段
    'TSLA': '特斯拉',  # 字典字段
    'NVDA': '英伟达',  # 字典字段
}  # 执行本行代码

period = '1y'   # 时间长度，可改成 '6mo'、'2y'
all_rets = {}   # 用字典存每只股票的中文名 → 日收益率序列

for symbol, name in tickers.items():  # 逐只股票下载
    data = yf.download(symbol, period=period, progress=False, multi_level_index=False).dropna()  # 下载股票日线行情
    all_rets[name] = data['Close'].pct_change().dropna()  # 只关心收盘价涨跌
    print(f'{name} ({symbol}): {len(all_rets[name])} 个交易日')  # 打印统计结果

vol = pd.Series({name: s.std() for name, s in all_rets.items()}).sort_values(ascending=False)  # 求标准差（波动大小）
print('\n=== 日收益率波动（标准差，越大越猛）===')  # 打印分隔线或结论
for name, v in vol.items():  # 代码块开始
    print(f'  {name}: {v:.3%}')  # 格式化打印
