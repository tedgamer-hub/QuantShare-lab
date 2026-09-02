# ========== 三只股票 Histogram 并排对比 ==========
fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)  # 创建子图

for ax, (name, series), c in zip(axes, all_rets.items(), colors):  # 逐只股票画直方图
    ax.hist(series.values, bins=35, color=c, alpha=0.75, edgecolor='white')  # 透明度
    ax.axvline(0, color='black', linestyle='--', linewidth=0.6)  # 画垂直参考线
    ax.set_title(f'{name}\nσ = {series.std():.2%}')  # 求标准差（波动大小）
    ax.set_xlabel('日收益率')  # 设置子图横轴

axes[0].set_ylabel('天数')  # 设置上图纵轴
fig.suptitle('三只股票：日收益率 Histogram 对比', fontsize=14, y=1.02)  # 整张图的总标题
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片
