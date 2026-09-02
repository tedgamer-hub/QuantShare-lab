# ========== 5.1 两种路径，同一终点 ==========
days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
x = np.arange(len(days))
stock_a = [100, 105, 110, 115, 120]
stock_b = [100, 80, 130, 70, 120]

path_table = pd.DataFrame({'股票A': stock_a, '股票B': stock_b}, index=days)
print('价格路径对照：')
display(path_table)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, stock_a, 'o-', color='#007AFF', linewidth=2.5, markersize=9, label='股票 A · 平稳上涨')
ax.plot(x, stock_b, 's-', color='#E82127', linewidth=2.5, markersize=9, label='股票 B · 大起大落')
ax.axhline(120, color='gray', linestyle='--', alpha=0.5, label='终点都是 120')
ax.set_xticks(x)
ax.set_xticklabels(days)
ax.set_ylabel('价格')
ax.set_title('收益相同，路径不同：你更愿意持有哪一只？', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

ret_a = stock_a[-1] / stock_a[0] - 1
ret_b = stock_b[-1] / stock_b[0] - 1
print(f'股票 A 总涨幅: {ret_a:.0%}')
print(f'股票 B 总涨幅: {ret_b:.0%}')