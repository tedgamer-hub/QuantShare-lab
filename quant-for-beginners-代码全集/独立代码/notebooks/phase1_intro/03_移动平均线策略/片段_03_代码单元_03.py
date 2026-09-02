# ========== 对比「乱的价格」和「平滑的均线」==========
demo = pd.DataFrame({'Close': price})           # 用上面模拟的价格
demo['MA20'] = demo['Close'].rolling(20).mean()  # 20日移动平均

fig, ax = plt.subplots(figsize=(13, 5))  # 创建子图
ax.plot(demo['Close'], label='原始收盘价（很乱）', color='lightgray', linewidth=1.5)  # 在子图上画折线
ax.plot(demo['MA20'], label='20日移动平均线（更平滑）', color='tab:blue', linewidth=2)  # 在子图上画折线
ax.set_title('为什么需要平均？—— 磨平噪声，看清趋势', fontsize=14)  # 设置子图标题
ax.set_xlabel('交易日（示意）')  # 设置子图横轴
ax.set_ylabel('价格')  # 设置子图纵轴
ax.legend()                                    # 显示图例
ax.grid(True, alpha=0.3)  # 显示网格
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片
