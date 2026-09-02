# ========== 统计胜率：一轮「买入→卖出」算一局 ==========
wins, losses = 0, 0       # 赢、输次数
entry_price = None        # 记住买入价
records = []              # 存每轮结果

for date, row in df.iterrows():  # 按天遍历整张表
    if row['action'] == '买入':  # 遇到买入日
        entry_price = row['Close']   # 记录买入当天的收盘价
    elif row['action'] == '卖出' and entry_price is not None:  # 遇到卖出且之前买过
        pnl = row['Close'] / entry_price - 1   # 本轮收益率
        if pnl > 0:  # 赚钱算赢
            wins += 1                    # 赢局计数 +1
            outcome = '赢'                 # 标记本局结果为赢
        else:  # 亏钱算输
            losses += 1                # 输局计数 +1
            outcome = '输'                 # 标记本局结果为输
        records.append({  # 记录本轮交易结果
            '卖出日': date.strftime('%Y-%m-%d'),  # 卖出日期
            '买入价': round(entry_price, 2),  # 买入价格
            '卖出价': round(row['Close'], 2),  # 卖出价格
            '本轮收益': f'{pnl:+.2%}',  # 本轮收益率
            '结果': outcome,  # 赢或输
        })  # 执行本行代码
        entry_price = None   # 本轮结束，清空买入价

total_rounds = wins + losses              # 完整买卖回合总数
win_rate = wins / total_rounds if total_rounds > 0 else np.nan  # 胜率

print(f'完整交易回合：{total_rounds} 轮')  # 打印回合总数
print(f'  赢：{wins} 次')  # 打印赢的次数
print(f'  输：{losses} 次')  # 打印输的次数
print(f'  胜率：{win_rate:.1%}' if total_rounds > 0 else '  暂无完整买卖回合')  # 打印胜率

if records:  # 有交易记录则展示
    display(pd.DataFrame(records).tail(8))  # 在 Notebook 中美观显示表格
