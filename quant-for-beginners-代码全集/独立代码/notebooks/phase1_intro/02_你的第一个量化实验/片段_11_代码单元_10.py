# ========== 三只股票收益率对比图 ==========
fig, axes = plt.subplots(1, 2, figsize=(14, 5))  # 创建子图
colors = ['tab:blue', 'tab:orange', 'tab:green']  # 各曲线颜色

for (name, series), c in zip(all_rets.items(), colors):  # 逐只股票画曲线
    axes[0].plot(series.index, series.values, label=name, alpha=0.75, linewidth=0.8)  # 上图：画折线
axes[0].axhline(0, color='black', linestyle='--', linewidth=0.6)  # 上图画参考线
axes[0].set_title('日收益率对比', fontsize=13)  # 设置上图标题
axes[0].set_xlabel('日期')  # 执行本行代码
axes[0].set_ylabel('日收益率')  # 设置上图纵轴
axes[0].legend()  # 显示上图图例
axes[0].grid(True, alpha=0.3)  # 上图显示网格

axes[1].bar(vol.index, vol.values * 100, color=colors[: len(vol)], edgecolor='white')  # 下图：画柱状图
axes[1].set_title('波动大小对比（标准差 %）', fontsize=13)  # 设置下图标题
axes[1].set_ylabel('标准差 (%)')  # 设置下图纵轴
axes[1].grid(True, axis='y', alpha=0.3)  # 下图显示网格
for i, v in enumerate(vol.values):  # 在柱顶标注数值
    axes[1].text(i, v * 100 + 0.02, f'{v:.2%}', ha='center', fontsize=11)  # 字号

plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片

winner = vol.index[0]  # 波动最大的股票
print(f'\n在本实验设定下（{period} 日线），波动最大的是：{winner}')  # 格式化打印
