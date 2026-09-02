# ========== 画收盘价 + 两条均线 ==========
plt.figure(figsize=(13, 5))  # 创建画布
plt.plot(df.index, df['Close'], label='收盘价', color='gray', alpha=0.5, linewidth=1)  # 画折线图
plt.plot(df.index, df['MA5'], label='MA5（5日均线）', color='tab:orange', linewidth=1.5)  # 画折线图
plt.plot(df.index, df['MA20'], label='MA20（20日均线）', color='tab:blue', linewidth=2)  # 画折线图
plt.title(f'{TICKER}：价格与移动平均线', fontsize=14)  # 设置图标题
plt.xlabel('日期')  # 设置横轴标签
plt.ylabel('价格')  # 设置纵轴标签
plt.legend()  # 显示图例
plt.grid(True, alpha=0.3)  # 显示网格线
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片
