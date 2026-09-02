# ========== 模拟三种市场状态并分区上色 ==========
np.random.seed(7)              # 固定随机数，图可复现
n_up, n_down, n_noise = 60, 50, 70  # 上涨段、下跌段、横盘段各多少天

ret_up = np.random.normal(0.004, 0.008, n_up)        # 上涨段：平均日收益偏正
ret_down = np.random.normal(-0.005, 0.010, n_down)   # 下跌段：平均日收益偏负
ret_noise = np.random.normal(0.0, 0.015, n_noise)    # 横盘：均值约0，波动大

price = 100 * np.cumprod(1 + np.r_[ret_up, ret_down, ret_noise])  # 拼成价格
x = np.arange(len(price))  # 横轴：第几个交易日

fig, ax = plt.subplots(figsize=(13, 5))  # 创建子图
ax.plot(x, price, color='black', linewidth=1.2, label='价格')  # 在子图上画折线

ax.axvspan(0, n_up, alpha=0.15, color='green', label='上涨趋势')  # 用色块标出区间
ax.axvspan(n_up, n_up + n_down, alpha=0.15, color='red', label='下跌趋势')  # 用色块标出区间
ax.axvspan(n_up + n_down, len(price), alpha=0.15, color='gray', label='噪声/横盘')  # 用色块标出区间

ax.set_title('三种市场状态（模拟）：趋势 vs 噪声', fontsize=14)  # 设置子图标题
ax.set_xlabel('交易日（示意）')  # 设置子图横轴
ax.set_ylabel('价格')  # 设置子图纵轴
ax.legend(loc='upper left')  # 显示图例
ax.grid(True, alpha=0.3)  # 显示网格
plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切
plt.show()                               # 在 Notebook 里显示图片

print('绿色区：整体向上 | 红色区：整体向下 | 灰色区：方向不明显、抖动大')  # 解读三色区域含义
