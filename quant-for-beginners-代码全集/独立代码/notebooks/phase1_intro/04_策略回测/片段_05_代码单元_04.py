# ========== 算日收益率 ==========
df['ret'] = df['Close'].pct_change().fillna(0)  # 股票本身每天涨跌

# ========== 策略收益：只有持仓日才吃到涨跌 ==========
df['strategy_ret'] = df['position'] * df['ret']  # 实际持仓（信号推迟一天）

# ========== 基准1：买入持有（一直满仓）==========
df['buyhold_ret'] = df['ret']  # 股票日收益率

# ========== 基准2：同期持有大盘 SPY ==========
spy = yf.download(BENCHMARK, period=PERIOD, progress=False, multi_level_index=False)[['Close']]  # 下载股票日线行情
spy.columns = ['SPY_Close']  # 重命名大盘收盘价列
df = df.join(spy, how='inner')  # 按日期对齐，只保留两边都有数据的行
df['market_ret'] = df['SPY_Close'].pct_change().fillna(0)  # 计算日收益率（今天相对昨天）

# ========== 累计净值：从 1 元钱出发连乘 ==========
df['nav_strategy'] = (1 + df['strategy_ret']).cumprod()  # 连乘得到累计净值/价格
df['nav_buyhold'] = (1 + df['buyhold_ret']).cumprod()  # 连乘得到累计净值/价格
df['nav_market'] = (1 + df['market_ret']).cumprod()  # 连乘得到累计净值/价格

total_strategy = df['nav_strategy'].iloc[-1] - 1  # 策略累计收益
total_buyhold = df['nav_buyhold'].iloc[-1] - 1  # 买入持有累计收益
total_market = df['nav_market'].iloc[-1] - 1  # 判断上交所 sh 还是深交所 sz

print('=== 样本期累计收益（不含手续费，仅供学习）===')  # 打印分隔线或结论
print(f'  双均线策略 ({TICKER}): {total_strategy:+.2%}')  # 格式化打印
print(f'  买入持有 ({TICKER}):     {total_buyhold:+.2%}')  # 格式化打印
print(f'  买入持有 ({BENCHMARK} 大盘): {total_market:+.2%}')  # 格式化打印
