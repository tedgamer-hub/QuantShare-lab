# ========== 最大回撤：从历史最高点最多跌了多少 ==========
def max_drawdown(nav_series):  # 定义最大回撤计算函数
    """输入净值序列，返回 (最大回撤比例, 每日回撤序列)。"""  # 字典字段
    peak = nav_series.cummax()           # 到每一天为止的历史最高净值
    drawdown = nav_series / peak - 1     # 当前净值相对峰值的跌幅
    return drawdown.min(), drawdown  # 返回最大回撤和回撤序列

mdd_strategy, dd_strategy = max_drawdown(df['nav_strategy'])  # 累计净值曲线
mdd_buyhold, dd_buyhold = max_drawdown(df['nav_buyhold'])  # 累计净值曲线

print('=== 最大回撤（样本期内最深一次「从山顶滑落」）===')  # 打印分隔线或结论
print(f'  双均线策略: {mdd_strategy:.2%}')  # 格式化打印
print(f'  买入持有 ({TICKER}): {mdd_buyhold:.2%}')  # 格式化打印

fig, ax = plt.subplots(figsize=(14, 5))  # 创建子图
ax.fill_between(df.index, dd_strategy * 100, 0, alpha=0.35, color='tab:purple', label='策略回撤 %')  # 在子图上填充区域
ax.plot(df.index, dd_strategy * 100, color='tab:purple', linewidth=1)  # 在子图上画折线
ax.set_title(f'策略回撤示意图（最大回撤 = {mdd_strategy:.2%}）', fontsize=14)  # 设置子图标题
ax.set_xlabel('日期')  # 设置子图横轴
ax.set_ylabel('相对历史高点的跌幅 (%)')  # 设置子图纵轴
ax.legend()                                    # 显示图例
ax.grid(True, alpha=0.3)  # 显示网格
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片
