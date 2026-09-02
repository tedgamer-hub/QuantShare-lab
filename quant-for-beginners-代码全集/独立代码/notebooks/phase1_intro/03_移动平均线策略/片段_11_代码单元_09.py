# ========== 第一个策略：MA5>MA20 则持仓 ==========
df['signal'] = (df['MA5'] > df['MA20']).astype(int)  # 满足条件=1，否则=0

df['trade'] = 0                              # 默认无交易
df.loc[df['cross'] > 0, 'trade'] = 1         # 金叉日标记买入
df.loc[df['cross'] < 0, 'trade'] = -1        # 死叉日标记卖出

hold_days = df['signal'].sum()             # signal=1 的天数
print(f'规则：MA5 > MA20 则持仓 (signal=1)')  # 格式化打印
print(f'样本期内约 {hold_days} 个交易日处于持仓状态（共 {len(df)} 天）')  # 打印统计结果
print(f'共产生 { (df["trade"] != 0).sum() } 次调仓信号（买+卖）')  # 格式化打印

display(df[df['trade'] != 0][['Close', 'MA5', 'MA20', 'signal', 'trade']].tail(6))  # 在 Notebook 中美观显示表格
