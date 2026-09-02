# ========== 日收益率曲线 + 直方图 ==========
rets = df['日收益率'].dropna()  # 去掉第一天的 NaN

fig, axes = plt.subplots(1, 2, figsize=(14, 5))  # 1行2列

axes[0].plot(rets.index, rets.values, color='steelblue', linewidth=0.9, alpha=0.85)  # 上图：画折线
axes[0].axhline(0, color='black', linewidth=0.8, linestyle='--')  # 零轴参考线
axes[0].set_title('苹果 AAPL：日收益率曲线', fontsize=13)  # 设置上图标题
axes[0].set_xlabel('日期')  # 执行本行代码
axes[0].set_ylabel('日收益率')  # 设置上图纵轴
axes[0].grid(True, alpha=0.3)  # 上图显示网格

axes[1].hist(rets.values, bins=40, color='steelblue', edgecolor='white', alpha=0.85)  # 画直方图
axes[1].axvline(0, color='black', linewidth=0.8, linestyle='--')  # 中图画垂直参考线
axes[1].axvline(rets.mean(), color='orange', linewidth=2, label=f'平均值 {rets.mean():.2%}')  # 求平均值
axes[1].set_title('日收益率分布（Histogram）', fontsize=13)  # 设置下图标题
axes[1].set_xlabel('日收益率')  # 设置下图横轴（日期）
axes[1].set_ylabel('天数')  # 设置下图纵轴
axes[1].legend()                                    # 显示下图图例
axes[1].grid(True, alpha=0.3)  # 下图显示网格

plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片

print(f'样本天数: {len(rets)}')  # 打印统计结果
print(f'平均日收益率: {rets.mean():.3%}（正=整体偏多涨）')  # 格式化打印
print(f'日收益率标准差: {rets.std():.3%}（越大=波动越剧烈）')  # 格式化打印
