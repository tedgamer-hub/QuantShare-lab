# ========== 相关性矩阵：谁和谁「同涨同跌」？==========
corr = returns.corr()                                  # Pearson 相关系数 ρ，对称矩阵

print('日收益率相关系数（ρ ∈ [-1, 1]）：')              # 标题说明
display(corr.round(2))                                 # 保留两位小数，Notebook 美观显示

mask = np.triu(np.ones(corr.shape, dtype=bool), k=1)   # 上三角掩码（k=1 排除对角线 1.0）
pairs = corr.where(mask).stack().sort_values()         # 展平为 MultiIndex Series 并升序
low_pair = pairs.index[0]                              # 最低相关的 (股票A, 股票B) 元组
low_rho  = pairs.iloc[0]                               # 对应的相关系数值
print(f'\n最低相关一对: {low_pair[0]} ↔ {low_pair[1]}，ρ = {low_rho:.2f}')  # 输出结论
