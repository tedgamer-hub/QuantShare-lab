# ========== 5.6 同收益、不同波动：净值路径模拟 ==========
rng = np.random.default_rng(42)
n = TRADING_DAYS
target_annual = 0.20
daily_mu = (1 + target_annual) ** (1 / n) - 1   # 换算成「日均」目标收益

vol_a, vol_b = 0.10, 0.60
sigma_a = vol_a / np.sqrt(n)
sigma_b = vol_b / np.sqrt(n)

rets_a = rng.normal(daily_mu, sigma_a, n)
rets_b = rng.normal(daily_mu, sigma_b, n)

nav_a = np.cumprod(1 + rets_a)
nav_b = np.cumprod(1 + rets_b)

def max_drawdown(nav):
    peak = np.maximum.accumulate(nav)
    return float((nav / peak - 1).min())

fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                         gridspec_kw={'height_ratios': [2, 1]})

axes[0].plot(nav_a, color='#007AFF', linewidth=1.5, label=f'投资者 A · 波动率 {vol_a:.0%}')
axes[0].plot(nav_b, color='#E82127', linewidth=1.5, label=f'投资者 B · 波动率 {vol_b:.0%}')
axes[0].axhline(1.20, color='gray', linestyle='--', alpha=0.6, label='目标 +20% 参考线')
axes[0].set_ylabel('净值（起点=1）')
axes[0].set_title('同样追求 ~20% 收益：持有过程天差地别', fontsize=14)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

dd_a = nav_a / np.maximum.accumulate(nav_a) - 1
dd_b = nav_b / np.maximum.accumulate(nav_b) - 1
axes[1].fill_between(range(n), dd_a, 0, alpha=0.4, color='#007AFF', label='A 回撤')
axes[1].fill_between(range(n), dd_b, 0, alpha=0.4, color='#E82127', label='B 回撤')
axes[1].set_ylabel('回撤')
axes[1].set_xlabel('交易日')
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"投资者 A  最终净值: {nav_a[-1]:.2f}  |  最大回撤: {max_drawdown(nav_a):.1%}")
print(f"投资者 B  最终净值: {nav_b[-1]:.2f}  |  最大回撤: {max_drawdown(nav_b):.1%}")
print('\n👉 想一想：B 的中途回撤，你会不会在某个低点「受不了」而卖出？')