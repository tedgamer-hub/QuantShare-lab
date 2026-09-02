# ========== 放大最近6个月，看清买卖细节 ==========
recent = df.last('6M') if len(df) > 120 else df.tail(120)  # 取最近约6个月
buys_r = recent[recent['trade'] == 1]  # 最近区间的买入点
sells_r = recent[recent['trade'] == -1]  # 最近区间的卖出点

fig, ax = plt.subplots(figsize=(14, 5))  # 创建子图
ax.plot(recent.index, recent['Close'], color='gray', alpha=0.5, linewidth=1, label='收盘价')  # 在子图上画折线
ax.plot(recent.index, recent['MA5'], color='tab:orange', linewidth=1.8, label='MA5')  # 在子图上画折线
ax.plot(recent.index, recent['MA20'], color='tab:blue', linewidth=2.2, label='MA20')  # 在子图上画折线
ax.scatter(buys_r.index, buys_r['Close'], marker='^', s=140, color='limegreen',  # 在子图上画散点
           edgecolors='darkgreen', linewidths=1, zorder=6, label='买入')  # 散点边框颜色
ax.scatter(sells_r.index, sells_r['Close'], marker='v', s=140, color='salmon',  # 在子图上画散点
           edgecolors='darkred', linewidths=1, zorder=6, label='卖出')  # 散点边框颜色
ax.set_title(f'{TICKER} 近 6 个月：金叉买入 / 死叉卖出（局部放大）', fontsize=14)  # 设置子图标题
ax.set_xlabel('日期')  # 设置子图横轴
ax.set_ylabel('价格')  # 设置子图纵轴
ax.legend()                                    # 显示图例
ax.grid(True, alpha=0.3)  # 显示网格
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片
