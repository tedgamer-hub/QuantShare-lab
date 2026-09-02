# ========== 金叉死叉标注图 ==========
fig, ax = plt.subplots(figsize=(14, 6))  # 创建子图

ax.plot(df.index, df['Close'], color='gray', alpha=0.4, linewidth=1, label='收盘价')  # 在子图上画折线
ax.plot(df.index, df['MA5'], color='tab:orange', linewidth=1.5, label='MA5')  # 在子图上画折线
ax.plot(df.index, df['MA20'], color='tab:blue', linewidth=2, label='MA20')  # 在子图上画折线

ax.fill_between(df.index, df['MA5'], df['MA20'],  # 在子图上填充区域
                where=(df['MA5'] >= df['MA20']),  # 计算 5 日移动平均线
                interpolate=True, alpha=0.12, color='green', label='MA5 > MA20')  # 填充区域平滑过渡

ax.scatter(golden.index, golden['MA5'], marker='^', s=80, color='green',  # 在子图上画散点
           edgecolors='black', linewidths=0.5, zorder=5, label='金叉（买入参考）')  # 图层顺序（点在线上方）
ax.scatter(death.index, death['MA5'], marker='v', s=80, color='red',  # 在子图上画散点
           edgecolors='black', linewidths=0.5, zorder=5, label='死叉（卖出参考）')  # 图层顺序（点在线上方）

ax.set_title(f'{TICKER}：MA5 vs MA20 —— 金叉 ▲ 与 死叉 ▼', fontsize=14)  # 设置子图标题
ax.set_xlabel('日期')  # 设置子图横轴
ax.set_ylabel('价格')  # 设置子图纵轴
ax.legend(loc='upper left', fontsize=9)  # 显示图例
ax.grid(True, alpha=0.3)  # 显示网格
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片
