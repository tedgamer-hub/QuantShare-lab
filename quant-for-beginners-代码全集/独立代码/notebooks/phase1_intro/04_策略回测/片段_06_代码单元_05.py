# ========== 三条净值曲线对比（回测高潮图）==========
fig, ax = plt.subplots(figsize=(14, 6))  # 创建子图

ax.plot(df.index, df['nav_strategy'], linewidth=2.2, color='tab:purple',  # 在子图上画折线
        label=f'双均线策略 ({TICKER})')  # 图例文字
ax.plot(df.index, df['nav_buyhold'], linewidth=1.8, color='tab:blue', alpha=0.85,  # 在子图上画折线
        label=f'买入持有 ({TICKER})')  # 图例文字
ax.plot(df.index, df['nav_market'], linewidth=1.8, color='tab:gray', linestyle='--',  # 在子图上画折线
        label=f'买入持有 ({BENCHMARK} 大盘)')  # 图例文字

ax.axhline(1.0, color='black', linewidth=0.6, linestyle=':', alpha=0.5)  # 画水平参考线
ax.set_title(f'回测净值曲线：策略 vs 标的 vs 大盘（{PERIOD}）', fontsize=14)  # 设置子图标题
ax.set_xlabel('日期')  # 设置子图横轴
ax.set_ylabel('净值（起点=1）')  # 设置子图纵轴
ax.legend(loc='upper left')  # 显示图例
ax.grid(True, alpha=0.3)  # 显示网格
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片
