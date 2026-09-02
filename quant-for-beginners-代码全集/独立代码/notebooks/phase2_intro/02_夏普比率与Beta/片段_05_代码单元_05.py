# ========== statistics 标准库：AAPL 日收益分布快照 ==========
aapl_daily = returns['AAPL'].dropna().tolist()     # Series → list，供 statistics 使用

print('── AAPL 日收益率分布（statistics 标准库）──')  # 分隔标题
print(f'均值:       {stats.mean(aapl_daily):>8.4%}')    # 算术平均（易受极端值影响）
print(f'中位数:     {stats.median(aapl_daily):>8.4%}')  # 50% 分位，更抗极端值
print(f'标准差:     {stats.pstdev(aapl_daily):>8.4%}')  # 总体标准差（除以 N）
print(f'最大单日涨: {max(aapl_daily):>8.2%}')           # 样本内最佳单日表现
print(f'最大单日跌: {min(aapl_daily):>8.2%}')           # 样本内最差单日表现
