# ========== 检测金叉、死叉 ==========
df['spread'] = df['MA5'] - df['MA20']              # 短均线减长均线
df['cross'] = np.sign(df['spread']).diff()         # 符号变化：正=金叉，负=死叉

golden = df[df['cross'] > 0].dropna(subset=['MA5', 'MA20'])  # 金叉那些天
death = df[df['cross'] < 0].dropna(subset=['MA5', 'MA20'])    # 死叉那些天

print(f'样本期内 金叉 {len(golden)} 次，死叉 {len(death)} 次')  # 打印统计结果
print('\n最近 3 次金叉日期：')  # 打印输出
print(golden.tail(3).index.strftime('%Y-%m-%d').tolist())  # 打印输出
print('\n最近 3 次死叉日期：')  # 打印输出
print(death.tail(3).index.strftime('%Y-%m-%d').tolist())  # 打印输出
