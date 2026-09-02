# ========== 策略信号大图：价格+买卖点+持仓条 ==========
buys = df[df['trade'] == 1]    # 所有买入日
sells = df[df['trade'] == -1]  # 所有卖出日

fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True,  # 创建子图
                         gridspec_kw={'height_ratios': [3, 1]})  # 子图高度比例
ax_price, ax_pos = axes  # 上图价格、下图持仓

ax_price.plot(df.index, df['Close'], color='gray', alpha=0.45, linewidth=1, label='收盘价')  # 透明度
ax_price.plot(df.index, df['MA5'], color='tab:orange', linewidth=1.5, label='MA5')  # 计算 5 日移动平均线
ax_price.plot(df.index, df['MA20'], color='tab:blue', linewidth=2, label='MA20')  # 计算 20 日移动平均线

ax_price.scatter(buys.index, buys['Close'], marker='^', s=120, color='limegreen',  # 上三角标记（买入/金叉）
                 edgecolors='darkgreen', linewidths=1, zorder=6, label='买入 ▲')  # 散点边框颜色
ax_price.scatter(sells.index, sells['Close'], marker='v', s=120, color='salmon',  # 下三角标记（卖出/死叉）
                 edgecolors='darkred', linewidths=1, zorder=6, label='卖出 ▼')  # 散点边框颜色

ax_price.set_title(f'{TICKER} 双均线策略：均线 + 买卖点', fontsize=14)  # 上图标题
ax_price.set_ylabel('价格')                                          # 上图纵轴：价格
ax_price.legend(loc='upper left')                                    # 显示图例
ax_price.grid(True, alpha=0.3)                                       # 显示网格

ax_pos.fill_between(df.index, 0, df['signal'], step='post', alpha=0.35, color='steelblue')  # 策略信号：1=持仓，0=空仓
ax_pos.set_ylim(-0.1, 1.2)  # 执行本行代码
ax_pos.set_yticks([0, 1])  # 执行本行代码
ax_pos.set_yticklabels(['空仓 (0)', '持仓 (1)'])  # 执行本行代码
ax_pos.set_xlabel('日期')  # 执行本行代码
ax_pos.set_ylabel('信号')  # 执行本行代码
ax_pos.set_title('策略持仓状态：MA5 > MA20 时持有', fontsize=12)  # 字号
ax_pos.grid(True, alpha=0.3)  # 透明度

plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片
