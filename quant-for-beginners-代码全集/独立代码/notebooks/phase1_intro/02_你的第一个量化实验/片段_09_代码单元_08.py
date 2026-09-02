# ========== 累计收益率曲线 ==========
cum_return = (1 + rets).cumprod() - 1  # 每天 (1+r) 连乘，再减1得到累计涨跌

plt.figure(figsize=(12, 4))  # 创建画布
plt.plot(cum_return.index, cum_return.values * 100, color='tab:purple', linewidth=1.5)  # 画折线图
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # 画水平参考线
plt.title('苹果 AAPL：累计收益率曲线（%）', fontsize=14)  # 设置图标题
plt.xlabel('日期')  # 设置横轴标签
plt.ylabel('累计收益率 (%)')  # 设置纵轴标签
plt.grid(True, alpha=0.3)  # 显示网格线
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片

print(f'这段区间累计涨跌: {cum_return.iloc[-1]:.2%}')  # 打印价格统计
