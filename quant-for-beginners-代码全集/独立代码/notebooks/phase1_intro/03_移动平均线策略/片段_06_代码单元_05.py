# ========== 【大陆用户】用 AkShare 下载 A 股并计算 MA5、MA20 ==========
from datetime import datetime, timedelta  # 日期计算（起止日）

SYMBOL = '600519'   # A 股 6 位代码：600519 茅台、000001 平安银行、300750 宁德时代
DAYS = 500          # 约 2 年交易日，与上方 PERIOD='2y' 对应

# 6 位代码 → 腾讯/新浪格式（6 开头在上交所用 sh，其余用 sz）
market = 'sh' if SYMBOL.startswith('6') else 'sz'  # 判断上交所 sh 还是深交所 sz
code = f'{market}{SYMBOL}'  # 拼成腾讯/新浪需要的代码格式

end_date = datetime.now().strftime('%Y%m%d')  # 结束日期（今天）
start_date = (datetime.now() - timedelta(days=int(DAYS * 1.6))).strftime('%Y%m%d')  # 多取一些天，再 tail

# 东方财富接口常因限流断开，按稳定性依次尝试
sources = [  # 数据源列表（按稳定性排序）
    ('腾讯证券', lambda: ak.stock_zh_a_hist_tx(symbol=code, start_date=start_date, end_date=end_date, adjust='qfq')),  # 腾讯证券前复权日线
    ('新浪财经', lambda: ak.stock_zh_a_daily(symbol=code, start_date=start_date, end_date=end_date, adjust='qfq')),  # 新浪财经前复权日线
    ('东方财富', lambda: ak.stock_zh_a_hist(symbol=SYMBOL, period='daily', start_date=start_date, end_date=end_date, adjust='qfq')),  # 东方财富前复权日线
]                                              # 数组拼接结束
raw, last_err = None, None              # 初始化：原始数据、最后一次报错
for name, fetch in sources:  # 依次尝试各个数据源
    try:  # 尝试当前数据源
        raw = fetch()  # 下载原始行情
        print(f'数据来源：{name}')  # 格式化打印
        break                        # 成功拿到数据，跳出循环
    except Exception as e:  # 当前源失败则换下一个
        last_err = e  # 赋值：last_err
        print(f'{name} 暂不可用，尝试下一个…')  # 格式化打印
if raw is None:                               # 三个数据源都失败
    raise last_err  # 抛出错误

# 统一成 Close 列（不同接口列名略有差异）
raw = raw.copy()                              # 复制一份，避免改到原始表
if '收盘' in raw.columns:  # 东方财富接口的列名
    raw['日期'] = pd.to_datetime(raw['日期'])  # 转成日期时间格式
    df = raw.set_index('日期')[['收盘']].rename(columns={'收盘': 'Close'})  # 把某列设为行索引（日期）
elif 'close' in raw.columns:  # 腾讯/新浪接口的列名
    raw['date'] = pd.to_datetime(raw['date'])  # 转成日期时间格式
    df = raw.set_index('date')[['close']].rename(columns={'close': 'Close'})  # 把某列设为行索引（日期）
else:                              # 否则：本轮亏损
    raise ValueError('未识别的行情格式，请检查 akshare 版本')  # 抛出错误

df = pd.to_numeric(df['Close'], errors='coerce').to_frame().sort_index().dropna().tail(DAYS).copy()  # 删除空值行
df['MA5'] = df['Close'].rolling(5).mean()  # 滚动窗口计算
df['MA20'] = df['Close'].rolling(20).mean()  # 滚动窗口计算

TICKER = SYMBOL     # 后面图表标题会用到这个变量
print(f'{SYMBOL} 共 {len(df)} 个交易日')  # 打印统计结果
display(df.tail(8))  # 在 Notebook 中美观显示表格