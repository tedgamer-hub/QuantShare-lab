# ========== 价格+均线 + 持仓时间条 ==========
fig, axes = plt.subplots(2, 1, figsize=(14, 7), sharex=True,  # 创建子图
                         gridspec_kw={'height_ratios': [2.5, 1]})  # 子图高度比例

axes[0].plot(df.index, df['Close'], color='gray', linewidth=1, label='收盘价')  # 上图：画折线
axes[0].plot(df.index, df['MA5'], color='tab:orange', linewidth=1.2, label='MA5')  # 上图：画折线
axes[0].plot(df.index, df['MA20'], color='tab:blue', linewidth=1.5, label='MA20')  # 上图：画折线
axes[0].set_ylabel('价格')  # 设置上图纵轴
axes[0].set_title(f'{TICKER}：双均线策略 —— 什么时候持仓？', fontsize=14)  # 设置上图标题
axes[0].legend(loc='upper left')  # 显示上图图例
axes[0].grid(True, alpha=0.3)  # 上图显示网格

axes[1].fill_between(df.index, 0, df['position'], step='post', alpha=0.4, color='green')  # 实际持仓（信号推迟一天）
axes[1].set_ylim(-0.1, 1.2)  # 执行本行代码
axes[1].set_yticks([0, 1])  # 执行本行代码
axes[1].set_yticklabels(['空仓', '持仓'])  # 执行本行代码
axes[1].set_xlabel('日期')  # 设置下图横轴（日期）
axes[1].set_ylabel('仓位')  # 设置下图纵轴
axes[1].grid(True, alpha=0.3)  # 下图显示网格

plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片

print('绿色区域 = 持仓（买入后、卖出前）| 空白 = 空仓')  # 解读三色区域含义
