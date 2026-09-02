# ========== 验证 100元→110元 的收益率例子 ==========
p_yesterday, p_today = 100, 110   # 昨天价、今天价
r = (p_today - p_yesterday) / p_yesterday  # 收益率公式
print(f'昨天: {p_yesterday} 元, 今天: {p_today} 元')  # 格式化打印
print(f'日收益率 r = {r:.2%}')  # :.2% 表示格式化为百分比，保留2位小数
