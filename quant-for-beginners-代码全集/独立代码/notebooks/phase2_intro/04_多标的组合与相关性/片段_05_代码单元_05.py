# ========== 等权组合波动 vs 单票 ==========
PORT_TICKERS = ['AAPL', 'MSFT', 'JPM', 'XLE']          # 组合成分（不含 SPY 基准）
port_returns = equal_weight_returns(returns, PORT_TICKERS)  # 等权组合日收益序列

comparison = {}                                        # 空字典，收集年化波动
for t in PORT_TICKERS:                                 # 遍历每只成分股
    comparison[t] = annualize_volatility(returns[t])   # 单票年化波动 σ·√252
comparison['等权组合'] = annualize_volatility(port_returns)  # 组合年化波动

comp = pd.Series(comparison).sort_values()           # 转为 Series 并按波动升序

print('年化波动率对比：')                               # 输出标题
display(comp.map('{:.2%}'.format))                     # 格式化为百分比字符串

fig, ax = plt.subplots(figsize=(8, 4.8))             # 横向柱状图画布
fig.patch.set_facecolor('#FAFAFA')                   # 画布背景
ax.set_facecolor('#FFFFFF')                          # 绘图区背景

colors = [                                             # 为每根柱子分配颜色
    '#34C759' if idx == '等权组合' else '#007AFF'    # 组合绿色，单票蓝色
    for idx in comp.index                              # 按 comp 索引顺序生成颜色列表
]                                                      # 列表推导结束
comp.plot(kind='barh', ax=ax, color=colors, alpha=0.88)  # 水平柱状图

ax.set_xlabel('年化波动率')                            # 横轴标签
ax.set_title('单票 vs 等权组合：波动对比', fontsize=14)  # 图标题
ax.grid(True, axis='x', linestyle='--', alpha=0.35)  # 竖向虚线网格
plt.tight_layout()                                     # 调整边距
plt.show()                                             # 显示图表
