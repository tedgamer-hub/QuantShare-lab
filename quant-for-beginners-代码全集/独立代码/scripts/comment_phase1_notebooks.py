#!/usr/bin/env python3
"""为 phase1_intro 下所有 notebook 的代码行补充中文行尾注释。"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE1 = ROOT / "notebooks" / "phase1_intro"

# 整行精确替换（去掉右侧空白后匹配）
EXACT: dict[str, str] = {
    "import warnings": "import warnings                          # 导入警告控制模块",
    "import numpy as np": "import numpy as np                       # 数值计算（数组、随机数、统计）",
    "import pandas as pd": "import pandas as pd                      # 表格数据处理（像 Excel）",
    "import matplotlib.pyplot as plt": "import matplotlib.pyplot as plt            # 绘图库（折线图、柱状图等）",
    "import yfinance as yf": "import yfinance as yf                    # 从雅虎财经下载行情（需联网）",
    "import akshare as ak": "import akshare as ak                      # 从国内数据源下载 A 股行情",
    "from datetime import datetime, timedelta": "from datetime import datetime, timedelta  # 日期计算（起止日）",
    "from matplotlib.lines import Line2D": "from matplotlib.lines import Line2D  # 自定义图例线段",
    "warnings.filterwarnings('ignore')": "warnings.filterwarnings('ignore')        # 隐藏不影响学习的警告",
    "warnings.filterwarnings('ignore')  # 隐藏无关警告": "warnings.filterwarnings('ignore')        # 隐藏不影响学习的警告",
    "plt.rcParams['axes.unicode_minus'] = False": "plt.rcParams['axes.unicode_minus'] = False      # 坐标轴负号正常显示",
    "plt.tight_layout()": "plt.tight_layout()                       # 自动调整子图间距，避免标签被裁切",
    "plt.show()": "plt.show()                               # 在 Notebook 里显示图片",
    "print('环境就绪 ✓')": "print('环境就绪 ✓')                       # 提示：环境加载完成",
    "]": "]                                              # 数组拼接结束",
    "axes[1].set_title(\"三种方法的净值对比\")": "axes[1].set_title(\"三种方法的净值对比\")                  # 下图标题",
    "axes[1].legend()": "axes[1].legend()                                    # 显示下图图例",
    "raw, last_err = None, None": "raw, last_err = None, None              # 初始化：原始数据、最后一次报错",
    "raw = raw.copy()": "raw = raw.copy()                              # 复制一份，避免改到原始表",
    "if raw is None:": "if raw is None:                               # 三个数据源都失败",
    "    raise last_err": "    raise last_err                           # 抛出最后一次错误，方便排查",
    "    raise ValueError('未识别的行情格式，请检查 akshare 版本')": "    raise ValueError('未识别的行情格式，请检查 akshare 版本')  # 主动报错",
    "wins, losses = 0, 0": "wins, losses = 0, 0                   # 统计赢、输次数",
    "records = []": "records = []                          # 存放每轮买卖结果",
    "total_rounds = wins + losses": "total_rounds = wins + losses              # 完整买卖回合总数",
}

# 正则 → 注释（匹配 strip 后的行）
REGEX_RULES: list[tuple[str, str]] = [
    (r"^import warnings$", "import warnings                          # 导入警告控制模块"),
    (r"^import numpy as np$", "import numpy as np                       # 数值计算库"),
    (r"^import pandas as pd$", "import pandas as pd                      # 表格数据处理库"),
    (r"^import matplotlib\.pyplot as plt$", "import matplotlib.pyplot as plt            # 绘图库"),
    (r"^import yfinance as yf.*$", "import yfinance as yf                    # 雅虎财经行情接口"),
    (r"^import akshare as ak$", "import akshare as ak                      # A 股行情接口"),
    (r"^plt\.rcParams\['font\.sans-serif'\].*$", None),  # 通常已有注释
    (r"^np\.random\.seed\(\d+\)$", None),
    (r"^print\('环境就绪", "print('环境就绪 ✓')                       # 提示环境加载完成"),
    (r"^print\(", None),  # 下面单独处理 print
    (r"^display\(", None),
    (r"^plt\.figure\(", None),
    (r"^fig, axes = plt\.subplots\(", None),
    (r"^fig, ax = plt\.subplots\(", None),
    (r"^plt\.tight_layout\(\)$", "plt.tight_layout()                       # 自动调整布局"),
    (r"^plt\.show\(\)$", "plt.show()                               # 显示图表"),
    (r"^ax\.legend\(\)$", "ax.legend()                                    # 显示图例"),
    (r"^axes\[\d+\]\.legend\(\)$", None),
    (r"^ax\.grid\(", None),
    (r"^axes\[\d+\]\.grid\(", None),
    (r"^plt\.grid\(", None),
]

# 按关键词猜测注释
KEYWORD_HINTS: list[tuple[str, str]] = [
    ("display(", "在 Notebook 中美观显示表格"),
    ("filterwarnings", "忽略次要警告，输出更干净"),
    ("import numpy", "数值计算库"),
    ("import pandas", "表格数据处理库"),
    ("import matplotlib", "绘图库"),
    ("import yfinance", "雅虎财经行情（需联网）"),
    ("import akshare", "国内 A 股行情接口"),
    ("from datetime import", "日期与时间计算"),
    ("from matplotlib.lines", "自定义图例元素"),
    ("rcParams['font.sans-serif']", "设置中文字体"),
    ("rcParams['axes.unicode_minus']", "负号正常显示"),
    ("np.random.seed", "固定随机种子，结果可复现"),
    ("random.seed", "固定随机种子，结果可复现"),
    ("yf.download", "下载股票日线行情"),
    ("stock_zh_a_hist_tx", "腾讯证券前复权日线"),
    ("stock_zh_a_daily", "新浪财经前复权日线"),
    ("stock_zh_a_hist", "东方财富前复权日线"),
    ("pct_change", "计算日收益率（今天相对昨天）"),
    ("rolling(", "滚动窗口计算"),
    (".mean()", "求平均值"),
    (".std()", "求标准差（波动大小）"),
    (".cumprod()", "连乘得到累计净值/价格"),
    (".shift(1)", "整体下移一天，避免用到未来数据"),
    (".dropna()", "删除空值行"),
    (".copy()", "复制一份，避免链式赋值警告"),
    (".astype(int)", "转成 0/1 整数"),
    (".fillna(0)", "空值填 0"),
    (".sort_index()", "按日期索引排序"),
    (".tail(", "取最后若干行"),
    (".head()", "取最前几行"),
    (".iterrows()", "按行遍历 DataFrame"),
    (".join(", "按日期对齐合并两张表"),
    (".set_index(", "把某列设为行索引（日期）"),
    (".rename(columns=", "统一列名"),
    (".to_datetime(", "转成日期时间格式"),
    (".to_frame()", "Series 转成 DataFrame"),
    (".to_numeric(", "转成数值，无法转的变 NaN"),
    ("pd.DataFrame", "构建表格"),
    ("pd.Series", "构建一维序列"),
    ("plt.figure", "创建画布"),
    ("plt.subplots", "创建子图"),
    ("plt.plot", "画折线图"),
    ("plt.bar", "画柱状图"),
    ("plt.scatter", "画散点图"),
    ("plt.fill_between", "两线之间填充颜色"),
    ("plt.title", "设置图标题"),
    ("plt.xlabel", "设置横轴标签"),
    ("plt.ylabel", "设置纵轴标签"),
    ("plt.legend", "显示图例"),
    ("plt.grid", "显示网格线"),
    ("plt.axhline", "画水平参考线"),
    ("plt.axvline", "画垂直参考线"),
    ("plt.text", "在图上标注文字"),
    ("plt.tight_layout", "自动调整子图间距"),
    ("plt.show", "显示图片"),
    ("ax.plot", "在子图上画折线"),
    ("ax.bar", "在子图上画柱状图"),
    ("ax.scatter", "在子图上画散点"),
    ("ax.fill_between", "在子图上填充区域"),
    ("ax.set_title", "设置子图标题"),
    ("ax.set_xlabel", "设置子图横轴"),
    ("ax.set_ylabel", "设置子图纵轴"),
    ("ax.set_ylim", "设置纵轴范围"),
    ("ax.set_yticks", "设置纵轴刻度位置"),
    ("ax.set_yticklabels", "设置纵轴刻度文字"),
    ("ax.set_xticks", "设置横轴刻度位置"),
    ("ax.set_xticklabels", "设置横轴刻度文字"),
    ("ax.set_yscale", "设置纵轴刻度类型（如对数）"),
    ("ax.axhline", "画水平参考线"),
    ("ax.axvline", "画垂直参考线"),
    ("ax.axvspan", "用色块标出区间"),
    ("ax.vlines", "画竖线（高低价）"),
    ("ax.hlines", "画横线（开盘价/收盘价）"),
    ("ax.legend", "显示图例"),
    ("ax.grid", "显示网格"),
    ("axes[0].plot", "上图：画折线"),
    ("axes[1].plot", "下图：画折线"),
    ("axes[0].bar", "上图：画柱状图"),
    ("axes[1].bar", "下图：画柱状图"),
    ("axes[0].set_title", "设置上图标题"),
    ("axes[1].set_title", "设置下图标题"),
    ("axes[0].set_ylabel", "设置上图纵轴"),
    ("axes[1].set_ylabel", "设置下图纵轴"),
    ("axes[1].set_xlabel", "设置下图横轴（日期）"),
    ("axes[0].legend", "显示上图图例"),
    ("axes[1].legend", "显示下图图例"),
    ("axes[0].grid", "上图显示网格"),
    ("axes[1].grid", "下图显示网格"),
    ("axes[0].axhline", "上图画参考线"),
    ("axes[1].axhline", "下图画参考线"),
    ("axes[1].axvline", "中图画垂直参考线"),
    ("axes[1].hist", "画直方图"),
    ("axes[2].scatter", "右图：散点"),
    ("axes[2].plot", "右图：理论曲线"),
    ("axes[2].set_title", "设置右图标题"),
    ("fig.suptitle", "整张图的总标题"),
    ("display(", "在 Notebook 中美观显示表格"),
    ("print(", "打印文字结果"),
    ("for name, fetch in sources:", "依次尝试各个数据源"),
    ("for name, fetch in sources", "依次尝试各个数据源"),
    ("try:", "尝试当前数据源"),
    ("except Exception", "当前源失败则换下一个"),
    ("break", "成功拿到数据，跳出循环"),
    ("lambda:", "匿名函数，延迟到真正调用时再请求"),
    ("sources = [", "数据源列表（按稳定性排序）"),
    ("market = ", "判断上交所 sh 还是深交所 sz"),
    ("code = f'", "拼成腾讯/新浪需要的代码格式"),
    ("end_date =", "结束日期（今天）"),
    ("start_date =", "开始日期（多取一些历史）"),
    ("df['MA5']", "计算 5 日移动平均线"),
    ("df['MA20']", "计算 20 日移动平均线"),
    ("df['spread']", "短均线减长均线"),
    ("df['cross']", "符号变化：正=金叉，负=死叉"),
    ("df['signal']", "策略信号：1=持仓，0=空仓"),
    ("df['trade']", "交易标记"),
    ("df['position']", "实际持仓（信号推迟一天）"),
    ("df['ret']", "股票日收益率"),
    ("df['strategy_ret']", "策略日收益（仅持仓日计入）"),
    ("df['buyhold_ret']", "买入持有日收益"),
    ("df['market_ret']", "大盘日收益"),
    ("df['nav_", "累计净值曲线"),
    ("golden =", "筛选金叉日期"),
    ("death =", "筛选死叉日期"),
    ("buys =", "所有买入日"),
    ("sells =", "所有卖出日"),
    ("recent =", "截取最近一段样本"),
    ("buys_r =", "最近区间的买入点"),
    ("sells_r =", "最近区间的卖出点"),
    ("trades =", "所有调仓日"),
    ("vol =", "各股票波动率（标准差）"),
    ("all_rets =", "存放各股票日收益率"),
    ("tickers =", "要对比的股票列表"),
    ("rets =", "日收益率序列"),
    ("cum_return =", "累计收益率"),
    ("spy =", "下载大盘 SPY 行情"),
    ("raw =", "下载原始行情"),
    ("aapl =", "下载苹果 AAPL 行情"),
    ("sample =", "取样本数据"),
    ("dates =", "横轴日期或位置"),
    ("colors =", "各曲线颜色"),
    ("configs =", "三个子图的配置"),
    ("legend_elements =", "自定义图例项"),
    ("TICKER =", "股票代码"),
    ("PERIOD =", "下载历史长度"),
    ("SYMBOL =", "A 股 6 位代码"),
    ("DAYS =", "保留的交易日数量"),
    ("BENCHMARK =", "大盘对比基准"),
    ("period =", "下载时间范围"),
    ("winner =", "波动最大的股票"),
    ("win_rate =", "胜率"),
    ("mdd_", "最大回撤"),
    ("dd_", "每日回撤序列"),
    ("total_", "累计收益"),
    ("hold_days =", "持仓天数统计"),
    ("def max_drawdown", "定义最大回撤计算函数"),
    ("def simulate_player", "定义模拟下注函数"),
    ("peak =", "到当前为止的历史最高净值"),
    ("drawdown =", "相对峰值的跌幅"),
    ("return drawdown", "返回最大回撤和回撤序列"),
    ("all_paths =", "存放每条模拟路径"),
    ("final_prices =", "各路径终点价格"),
    ("time_points =", "选取的观察时点"),
    ("std_at_time =", "各时点的价格标准差"),
    ("sqrt_time =", "时间的平方根"),
    ("scale =", "缩放系数，对齐理论线"),
    ("kelly_fraction =", "凯利公式最优下注比例"),
    ("aggressive_fraction =", "激进玩家的固定仓位"),
    ("curves_A =", "玩家 A 的资金曲线"),
    ("curves_B =", "玩家 B 的资金曲线"),
    ("curves_C =", "玩家 C 的资金曲线"),
    ("n_stocks =", "模拟股票只数"),
    ("n_days =", "模拟交易天数"),
    ("start_price =", "起始价格"),
    ("daily_volatility =", "日波动强度"),
    ("n_rounds =", "模拟下注轮数"),
    ("n_simulations =", "重复实验次数"),
    ("initial_capital =", "初始本金"),
    ("win_prob_", "胜率参数"),
    ("payout_ratio =", "赔率"),
    ("median_curve =", "多次实验的中位数轨迹"),
    ("finals =", "每次实验的最终资金"),
    ("if row['action']", "判断买入或卖出动作"),
    ("elif row['action']", "卖出时结算本轮盈亏"),
    ("records.append", "记录本轮交易结果"),
    ("entry_price = row", "记录买入价"),
    ("pnl =", "本轮收益率"),
    ("if pnl > 0", "赚钱算赢"),
    ("else:", "亏钱算输"),
    ("if '收盘' in", "东方财富接口的列名"),
    ("elif 'close' in", "腾讯/新浪接口的列名"),
    ("if records:", "有交易记录则展示"),
    ("for col in", "遍历列名"),
    ("for symbol, name in", "逐只股票下载"),
    ("for i, (idx, row) in enumerate", "逐日画 OHLC"),
    ("for ax, (curves, title", "为每个玩家画子图"),
    ("for name, curves, color in", "打印各玩家统计"),
    ("for (name, series), c in zip", "逐只股票画曲线"),
    ("for ax, (name, series), c in zip", "逐只股票画直方图"),
    ("for i, v in enumerate", "在柱顶标注数值"),
    ("for col in [\"ret_quant\"", "遍历三种收益列"),
    ("zip(axes, configs)", "子图与配置一一对应"),
    ("o, h, l, c =", "取出开高低收四个价"),
    ("color = 'tab:red'", "收跌日用红色"),
    ("manual_r =", "手算收益率用于验证"),
    ("row_today =", "最后一行（今天）"),
    ("row_yesterday =", "倒数第二行（昨天）"),
    ("p_yesterday", "昨天价格"),
    ("r = (p_today", "手算日收益率"),
    ("data = yf.download", "下载单只股票"),
    ("all_rets[name]", "存入字典"),
    ("df.loc[df['cross']", "在金叉/死叉日标记交易"),
    ("df.loc[df['position_change']", "标记买入或卖出文字"),
    ("df['action'] = ''", "初始化动作列"),
    ("ax_price, ax_pos = axes", "上图价格、下图持仓"),
    ("gridspec_kw", "子图高度比例"),
    ("sharex=True", "子图共用横轴（日期）"),
    ("height_ratios", "上下子图高度比"),
    ("interpolate=True", "填充区域平滑过渡"),
    ("zorder=5", "图层顺序（点在线上方）"),
    ("edgecolors=", "散点边框颜色"),
    ("linewidths=", "散点边框粗细"),
    ("step='post'", "阶梯状填充（持仓状态）"),
    ("alpha=", "透明度"),
    ("linewidth=", "线宽"),
    ("fontsize=", "字号"),
    ("marker='^'", "上三角标记（买入/金叉）"),
    ("marker='v'", "下三角标记（卖出/死叉）"),
    ("figsize=", "图尺寸（宽, 高）英寸"),
    ("bins=", "直方图柱子个数"),
    ("s=80", "散点大小"),
    ("where=(", "仅在某条件成立时填充"),
    ("if len(df)", "数据不够长时的兜底"),
    ("raise ", "抛出错误"),
    ("TICKER = SYMBOL", "后续图表标题用 A 股代码"),
]

# 单元格级完整覆盖（notebook 文件名 → cell 索引 → 完整源码）
CELL_OVERRIDES: dict[str, dict[int, str]] = {}


def has_comment(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s.startswith("#"):
        return True
    if "#" in line:
        return True
    return False


def guess_comment(code: str) -> str:
    for kw, hint in KEYWORD_HINTS:
        if kw in code:
            return hint
    code_s = code.strip()
    if code_s.endswith(":"):
        if code_s.strip() == "else:":
            return "否则分支"
        return "代码块开始"
    if "+=" in code_s:
        return "累加计数"
    if re.match(r"^['\"]", code_s) or re.match(r"^\d", code_s):
        return "字典字段"
    if code_s.startswith("if "):
        return "条件判断"
    if code_s.startswith("elif "):
        return "否则如果"
    if code_s.startswith("for "):
        return "循环"
    if code_s.startswith("return "):
        return "返回结果"
    if "=" in code_s and not code_s.startswith("print"):
        left = code_s.split("=")[0].strip()
        return f"赋值：{left}"
    return "执行本行代码"


def annotate_line(line: str) -> str:
    if has_comment(line):
        return line
    stripped = line.rstrip()
    key = stripped.strip()
    if key in EXACT:
        return EXACT[key] if not line.startswith(" ") else line[: len(line) - len(line.lstrip())] + EXACT[key].lstrip()

    for pattern, replacement in REGEX_RULES:
        if replacement and re.match(pattern, key):
            indent = line[: len(line) - len(line.lstrip())]
            return indent + replacement.lstrip()

    # print / display 特殊处理
    if key.startswith("print("):
        if "环境就绪" in key:
            c = "提示环境加载完成"
        elif "前 5 行" in key:
            c = "提示下方表格"
        elif "各列含义" in key:
            c = "打印列名说明"
        elif "验证" in key or "手算" in key:
            c = "对照手算与 pandas 结果"
        elif "==" in key or "---" in key or "→" in key:
            c = "打印分隔线或结论"
        elif "交易日" in key or "样本" in key or "赢" in key or "输" in key:
            c = "打印统计结果"
        elif "起始" in key or "最终" in key or "区间" in key or "最高" in key or "最低" in key:
            c = "打印价格统计"
        elif "凯利" in key:
            c = "打印凯利公式结果"
        elif "绿色区" in key:
            c = "解读三色区域含义"
        elif "绿色区域" in key:
            c = "解读持仓色块含义"
        elif "tip" in key.lower() or "小贴士" in key:
            c = "打印小贴士"
        elif "f'" in key or 'f"' in key:
            c = "格式化打印"
        else:
            c = "打印输出"
        return f"{stripped}  # {c}"

    indent = line[: len(line) - len(line.lstrip())]
    comment = guess_comment(stripped)
    return f"{stripped}  # {comment}"


def annotate_source(source: str) -> str:
    lines = source.splitlines()
    out = [annotate_line(ln) for ln in lines]
    return "\n".join(out) + ("\n" if source.endswith("\n") else "")


def process_notebook(path: Path) -> int:
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)

    overrides = CELL_OVERRIDES.get(path.name, {})
    changed = 0
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        old = "".join(cell.get("source", []))
        if not old.strip():
            continue
        if i in overrides:
            new = overrides[i]
        else:
            new = annotate_source(old)
        if new != old:
            cell["source"] = [new]
            changed += 1

    with open(path, encoding="utf-8") as f:
        pass
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    return changed


def main() -> None:
    total = 0
    for path in sorted(PHASE1.glob("*.ipynb")):
        n = process_notebook(path)
        print(f"{path.name}: updated {n} cells")
        total += n
    print(f"done, {total} cells updated")


if __name__ == "__main__":
    main()
