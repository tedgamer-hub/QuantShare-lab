# ========== 【海外用户】用 yfinance 下载并计算 MA5、MA20 ==========
# 大陆网络若连不上 Yahoo，请跳过本格，运行下方 AkShare 那一格
raw = yf.download(TICKER, period=PERIOD, progress=False, multi_level_index=False)  # 下载行情
df = raw[['Close']].dropna().copy()   # 只留收盘价，去掉空行
df.columns = ['Close']                # 列名统一成 Close

df['MA5'] = df['Close'].rolling(5).mean()    # 5日均线 = 最近5天收盘均价
df['MA20'] = df['Close'].rolling(20).mean()  # 20日均线

print(f'{TICKER} 共 {len(df)} 个交易日')  # 打印统计结果
display(df.tail(8))  # 显示最后8行，检查算得对不对
