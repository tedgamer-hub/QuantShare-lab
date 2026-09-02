# ========== 下载行情 → 日收益 → 年化指标与 Sharpe ==========
# 数据链：akshare → ak.stock_us_daily() → 新浪财经美股日线（联网，非模拟）

tickers = [                                      # 共 10 只：9 只个股 + 1 只大盘 ETF
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META',    # 科技巨头
    'NVDA', 'TSLA', 'AMD',  'JPM',              # 高波动成长 + 银行对照
    'SPY',                                       # 标普 500 ETF，作 Beta 基准
]
period_years = 3                                 # 回溯约 3 年
rf_annual    = 0.04                              # 无风险利率近似 4%

start_date = (                                   # 计算样本起始日
    pd.Timestamp.today()                         # 今天
    - pd.DateOffset(years=period_years, days=30) # 往前 3 年，多留 30 天缓冲
).strftime('%Y-%m-%d')                           # 格式化为 'YYYY-MM-DD'

print(f'akshare 版本: {ak.__version__}')         # 打印库版本，便于排查
print('接口: ak.stock_us_daily(symbol, adjust="qfq")  # 新浪财经 · 前复权')


def fetch_us_close(symbol: str, start: str) -> pd.Series:
    """联网拉取单只美股前复权收盘价，并按起始日裁剪。"""
    df = ak.stock_us_daily(symbol=symbol, adjust='qfq')  # 发起 HTTP 请求
    if df is None or df.empty:                     # 网络/接口异常时主动报错
        raise RuntimeError(f'{symbol} 未返回数据，请检查网络或 akshare 版本')

    df['date'] = pd.to_datetime(df['date'])        # 字符串 → 日期类型
    close = (                                      # 整理为以日期为索引的收盘价序列
        df.set_index('date')                       # 日期列设为行索引
          .sort_index()                             # 按时间升序排列
          ['close']                                 # 只保留收盘价列
          .rename(symbol)                           # Series 命名 = 股票代码
    )
    return close.loc[close.index >= start]         # 截取 start 之后的样本


print(f'\n正在下载 {len(tickers)} 只美股（约 {period_years} 年）…')
frames = {}
for t in tickers:
    frames[t] = fetch_us_close(t, start_date)
    time.sleep(1)                                # 新浪接口限速，连续请求间隔 1 秒
prices = pd.DataFrame(frames).dropna()           # 宽表：每列一只股票

returns = prices.pct_change().dropna()             # 简单日收益率 r_t = P_t/P_{t-1} − 1

api_tail = ak.stock_us_daily(symbol='AAPL', adjust='qfq').tail(1)  # 再拉一次 API 末行作核验
print('\n【核验】AAPL 接口原始末行（AkShare 直接返回）：')
display(api_tail)                                  # Notebook 内美观显示表格
print(f'样本区间：{prices.index[0].date()} → {prices.index[-1].date()}，共 {len(returns)} 个交易日')
print(f'AAPL 末收（对齐后）: {prices["AAPL"].iloc[-1]:.2f}')  # 应与 api_tail 的 close 一致

metrics = pd.DataFrame({                           # 数值版指标表（供后续作图）
    t: {                                           # 每列对应一只 ticker
        '年化收益': annualize_return(returns[t]),
        '年化波动': annualize_volatility(returns[t]),
        'Sharpe': sharpe_ratio(returns[t], rf_annual),
    }
    for t in tickers                               # 遍历全部 10 只
}).T.rename_axis('股票')                            # 转置后行 = 股票代码

summary = metrics.copy()                           # 复制一份用于格式化展示
summary['年化收益'] = summary['年化收益'].map('{:.2%}'.format)  # 收益 → 百分比字符串
summary['年化波动'] = summary['年化波动'].map('{:.2%}'.format)  # 波动 → 百分比字符串
summary['Sharpe']   = summary['Sharpe'].map('{:.2f}'.format)    # Sharpe 保留两位小数

print('\n风险收益一览（近似 Sharpe）：')
display(summary)                                   # 展示格式化后的汇总表
