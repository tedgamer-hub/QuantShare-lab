# ========== 相关性热力图（matplotlib 纯实现）==========
labels = list(corr.columns)                            # 轴标签，顺序与 corr 行列一致
n = len(labels)                                        # 标的数量

fig, ax = plt.subplots(figsize=(8.5, 6.5))             # 创建画布与子图
fig.patch.set_facecolor('#FAFAFA')                   # 画布浅灰背景
ax.set_facecolor('#FFFFFF')                          # 绘图区白色背景

im = ax.imshow(corr.values, cmap='RdBu_r', vmin=-1, vmax=1)  # 矩阵 → 颜色（红正蓝负）

ax.set_xticks(range(n))                                # 横轴刻度：0 … n-1
ax.set_yticks(range(n))                                # 纵轴刻度
ax.set_xticklabels(labels)                             # 横轴标签 = 股票代码
ax.set_yticklabels(labels)                             # 纵轴标签
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')  # x 标签旋转 45° 防重叠

for i in range(n):                                     # 遍历矩阵行
    for j in range(n):                                 # 遍历矩阵列
        rho = corr.iloc[i, j]                          # 第 (i,j) 格的相关系数
        text_color = 'white' if abs(rho) > 0.55 else 'black'  # 深色背景用白字
        ax.text(                                       # 在格子中心写数值
            j, i, f'{rho:.2f}',                        # 坐标 (列, 行) + 两位小数文本
            ha='center', va='center',                    # 水平/垂直居中对齐
            color=text_color, fontsize=10, fontweight='bold',  # 字体颜色、大小、加粗
        )                                              # text 调用结束

ax.set_title('多标的日收益率相关性热力图（AkShare · 约 3 年）', fontsize=14, pad=12)  # 图标题
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)    # 右侧颜色条（-1 到 1）
plt.tight_layout()                                     # 自动调整边距
plt.show()                                             # 在 Notebook 中显示
