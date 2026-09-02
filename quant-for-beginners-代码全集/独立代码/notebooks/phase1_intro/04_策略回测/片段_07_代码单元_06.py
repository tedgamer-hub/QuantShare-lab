# ========== 近12个月局部放大 ==========
recent = df.last('12M') if len(df) > 200 else df.tail(200)  # 取最后若干行

plt.figure(figsize=(14, 5))  # 创建画布
plt.plot(recent.index, recent['nav_strategy'], linewidth=2, label='双均线策略')  # 画折线图
plt.plot(recent.index, recent['nav_buyhold'], linewidth=1.6, label=f'买入持有 {TICKER}')  # 画折线图
plt.plot(recent.index, recent['nav_market'], linewidth=1.6, linestyle='--', label=f'买入持有 {BENCHMARK}')  # 画折线图
plt.title('近 12 个月：策略 vs 基准（局部）', fontsize=14)  # 设置图标题
plt.xlabel('日期')  # 设置横轴标签
plt.ylabel('净值')  # 设置纵轴标签
plt.legend()  # 显示图例
plt.grid(True, alpha=0.3)  # 显示网格线
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片
