# ========== 第1步：下载数据并算双均线 ==========
raw = yf.download(TICKER, period=PERIOD, progress=False, multi_level_index=False)  # 下载股票日线行情
df = raw[['Close']].dropna().copy()  # 删除空值行
df.columns = ['Close']           # 列名统一为 Close

df['MA5'] = df['Close'].rolling(5).mean()  # 滚动窗口计算
df['MA20'] = df['Close'].rolling(20).mean()  # 滚动窗口计算
df['signal'] = (df['MA5'] > df['MA20']).astype(int)  # 收盘算出的「理论信号」

# ========== 第2步：信号推迟一天，避免用未来数据 ==========
df['position'] = df['signal'].shift(1).fillna(0).astype(int)  # 今天实际仓位

# ========== 第3步：标记买入、卖出日 ==========
df['position_change'] = df['position'].diff().fillna(0)  # 仓位变化：0→1买，1→0卖
df['action'] = ''  # 初始化动作列
df.loc[df['position_change'] > 0, 'action'] = '买入'  # 标记买入或卖出文字
df.loc[df['position_change'] < 0, 'action'] = '卖出'  # 标记买入或卖出文字

trades = df[df['action'] != '']  # 所有调仓日
print(f'标的 {TICKER}，共 {len(df)} 个交易日')  # 打印统计结果
print(f'模拟交易：买入 { (df["action"]=="买入").sum() } 次，卖出 { (df["action"]=="卖出").sum() } 次')  # 打印分隔线或结论
print('\n最近几次调仓：')  # 打印输出
display(trades[['Close', 'MA5', 'MA20', 'position', 'action']].tail(6))  # 在 Notebook 中美观显示表格
