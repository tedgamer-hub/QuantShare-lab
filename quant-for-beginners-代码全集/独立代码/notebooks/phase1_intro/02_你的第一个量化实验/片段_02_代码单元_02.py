# ========== 下载苹果 AAPL 最近约 1 年的日线数据 ==========
aapl = yf.download('AAPL', period='1y', progress=False, multi_level_index=False)  # 下载
aapl = aapl.dropna()  # 删掉有空值的行，保证数据完整

print('数据形状（行=交易日，列=字段）：', aapl.shape)  # 例如 (251, 5)
print('\n前 5 行：')  # 提示下方表格
display(aapl.head())  # Jupyter 里美观显示表格前几行

print('\n各列含义速查：')  # 打印列名说明
for col in aapl.columns:  # 遍历每一列的名字
    print(f'  {col}')  # 格式化打印
