#!/usr/bin/env python3
"""生成夏普比率动态演示 HTML（数据来自 AkShare 美股日线）。"""
import json
from pathlib import Path

import akshare as ak
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "interactive" / "sharpe-ratio-demo.html"

TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "NVDA", "TSLA", "AMD", "JPM", "SPY",
]
PERIOD_YEARS = 3
SAMPLE_DAYS = 300                              # 演示用最近 300 个交易日
RF_ANNUAL = 0.04
TRADING_DAYS = 252

start = (pd.Timestamp.today() - pd.DateOffset(years=PERIOD_YEARS, days=30)).strftime("%Y-%m-%d")


def fetch_returns(symbol: str) -> list[float]:
    df = ak.stock_us_daily(symbol=symbol, adjust="qfq")
    df["date"] = pd.to_datetime(df["date"])
    close = df.set_index("date").sort_index()["close"]
    close = close.loc[close.index >= start]
    r = close.pct_change().dropna().tail(SAMPLE_DAYS)  # 只保留最近 300 个交易日
    return [round(x, 6) for x in r.tolist()]


print("fetching AkShare data …")
RETURNS = {t: fetch_returns(t) for t in TICKERS}
N = min(len(v) for v in RETURNS.values())
print(f"embedded {len(TICKERS)} tickers × {N} daily returns")

returns_js = json.dumps(RETURNS, ensure_ascii=False, indent=2)

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>夏普比率动态演示 · Quant for Beginners</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0c0f14; --surface: #151a22; --surface2: #1c2330; --border: #2a3344;
      --text: #e8ecf4; --muted: #8b95a8; --accent: #3d9cf5; --green: #2dd4a8; --red: #f07178; --orange: #f5a623;
      --radius: 10px; --font: "IBM Plex Sans", system-ui, sans-serif; --mono: "IBM Plex Mono", ui-monospace, monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ height: 100%; overflow: hidden; }}
    body {{ font-family: var(--font); background: var(--bg); color: var(--text); line-height: 1.5; }}
    .app {{ height: 100vh; display: grid; grid-template-rows: auto auto 1fr; gap: 8px; padding: 10px 14px; max-width: 1400px; margin: 0 auto; }}
    .topbar {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }}
    .topbar h1 {{ font-size: 1rem; font-weight: 600; }}
    .topbar .eq {{ font-family: var(--mono); font-size: 0.74rem; color: var(--accent); margin-left: 10px; }}
    .pill {{ font-size: 0.74rem; color: var(--muted); background: var(--surface); border: 1px solid var(--border); border-radius: 999px; padding: 4px 12px; white-space: nowrap; }}
    .tickers {{ display: flex; flex-wrap: wrap; gap: 5px; }}
    .tbtn {{ font-family: var(--font); font-size: 0.68rem; padding: 4px 10px; border-radius: 7px; border: 1px solid var(--border); background: var(--surface); color: var(--muted); cursor: pointer; }}
    .tbtn:hover {{ border-color: var(--accent); color: var(--text); }}
    .tbtn.active {{ background: var(--accent); border-color: var(--accent); color: #0a0e12; font-weight: 600; }}
    .layout {{ display: grid; grid-template-columns: 320px 1fr; gap: 10px; min-height: 0; }}
    @media (max-width: 980px) {{ html, body {{ overflow: auto; height: auto; }} .app {{ height: auto; min-height: 100vh; }} .layout {{ grid-template-columns: 1fr; }} }}
    .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }}
    .left {{ display: grid; grid-template-rows: 1fr auto auto; gap: 8px; min-height: 0; }}
    .section-title {{ padding: 7px 12px; font-size: 0.68rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid var(--border); }}
    .formula {{ padding: 10px 12px; font-family: var(--mono); font-size: 0.72rem; line-height: 1.68; white-space: pre-line; overflow-y: auto; max-height: 240px; }}
    .formula .hl {{ color: var(--accent); }}
    .formula .result {{ font-size: 0.95rem; font-weight: 500; margin-top: 4px; color: var(--green); }}
    .stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 5px; padding: 0 10px 10px; }}
    .stat {{ background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 7px; text-align: center; }}
    .stat label {{ display: block; font-size: 0.58rem; color: var(--muted); text-transform: uppercase; margin-bottom: 2px; }}
    .stat span {{ font-family: var(--mono); font-size: 0.8rem; font-weight: 500; }}
    .controls {{ padding: 9px 12px; }}
    .btn-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; margin-bottom: 8px; }}
    .btn {{ font-family: var(--font); font-size: 0.72rem; font-weight: 500; padding: 6px 3px; border-radius: 7px; border: 1px solid var(--border); background: var(--surface2); color: var(--text); cursor: pointer; }}
    .btn:hover {{ border-color: var(--accent); }}
    .btn.primary {{ background: var(--accent); border-color: var(--accent); color: #0a0e12; }}
    .speed {{ display: flex; align-items: center; gap: 8px; font-size: 0.72rem; color: var(--muted); }}
    .speed input {{ flex: 1; accent-color: var(--accent); }}
    .progress {{ height: 3px; background: var(--border); margin-top: 8px; }}
    .progress-fill {{ height: 100%; background: var(--accent); width: 0%; transition: width 0.08s linear; }}
    .legend {{ padding: 7px 12px; display: flex; flex-wrap: wrap; gap: 8px 12px; font-size: 0.66rem; color: var(--muted); }}
    .legend-item {{ display: flex; align-items: center; gap: 4px; }}
    .sw {{ width: 9px; height: 9px; border-radius: 50%; }}
    .sw.line {{ width: 12px; height: 3px; border-radius: 2px; }}
    .right {{ display: grid; grid-template-rows: 1fr 1fr; gap: 8px; min-height: 0; }}
    .chart {{ display: flex; flex-direction: column; min-height: 0; }}
    .chart-wrap {{ flex: 1; min-height: 0; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div class="app">
    <header class="topbar">
      <div>
        <h1>夏普比率动态演示<span class="eq">Sharpe ≈ (年化收益 − r_f) / 年化波动</span></h1>
      </div>
      <div class="pill" id="stepPill">—</div>
    </header>
    <nav class="tickers" id="tickerNav"></nav>
    <div class="layout">
      <aside class="left">
        <div class="card">
          <div class="section-title">逐步代入公式 · r_f = {RF_ANNUAL:.0%}</div>
          <div class="formula" id="formulaBox">▶ 选择股票后点击「播放」</div>
          <div class="stats">
            <div class="stat"><label>年化收益</label><span id="annRetVal">—</span></div>
            <div class="stat"><label>年化波动</label><span id="annVolVal">—</span></div>
            <div class="stat"><label>超额收益</label><span id="excessVal">—</span></div>
            <div class="stat"><label>Sharpe</label><span id="sharpeVal">—</span></div>
          </div>
        </div>
        <div class="card controls">
          <div class="btn-row">
            <button class="btn primary" id="btnPlay">▶ 播放</button>
            <button class="btn" id="btnPause">⏸ 暂停</button>
            <button class="btn" id="btnStep">⏭ 单步</button>
            <button class="btn" id="btnReset">↺ 重置</button>
          </div>
          <div class="speed"><span>速度</span><input type="range" id="speed" min="1" max="10" value="9" /></div>
          <div class="progress"><div class="progress-fill" id="progress"></div></div>
        </div>
        <div class="card legend">
          <div class="legend-item"><span class="sw" style="background:#4da3ff"></span> 日收益 r_t</div>
          <div class="legend-item"><span class="sw line" style="background:var(--green)"></span> 年化收益（左轴）</div>
          <div class="legend-item"><span class="sw line" style="background:var(--orange)"></span> 年化波动（左轴）</div>
          <div class="legend-item"><span class="sw line" style="background:var(--accent)"></span> Sharpe（右轴）</div>
        </div>
      </aside>
      <main class="right">
        <div class="card chart">
          <div class="section-title">日收益率 r_t</div>
          <div class="chart-wrap" id="wrapR"><canvas id="canvasR"></canvas></div>
        </div>
        <div class="card chart">
          <div class="section-title">年化指标与 Sharpe 的演化</div>
          <div class="chart-wrap" id="wrapM"><canvas id="canvasM"></canvas></div>
        </div>
      </main>
    </div>
  </div>
  <script>
    const RETURNS = {returns_js};
    const TICKERS = {json.dumps(TICKERS)};
    const RF = {RF_ANNUAL};
    const TD = {TRADING_DAYS};
    const N = {N};
    const RUN_WINDOW = 60;
    const MIN_METRIC_DAYS = 20;                    // 前 20 日样本过少，年化指标不稳定，不入图

    let ticker = TICKERS[0];
    let frame = 0, playing = false, timer = null;

    const cR = document.getElementById('canvasR');
    const cM = document.getElementById('canvasM');
    const rCtx = cR.getContext('2d');
    const mCtx = cM.getContext('2d');

    function series() {{ return RETURNS[ticker]; }}

    function sharpeStats(k) {{
      const slice = series().slice(0, k + 1);
      const n = slice.length;
      const mean = slice.reduce((a, b) => a + b, 0) / n;
      const annRet = Math.pow(1 + mean, TD) - 1;
      const variance = slice.reduce((a, r) => a + (r - mean) ** 2, 0) / Math.max(1, n - 1);
      const annVol = Math.sqrt(variance) * Math.sqrt(TD);
      const excess = annRet - RF;
      const sharpe = n >= 2 && annVol > 0 ? excess / annVol : NaN;
      return {{ slice, n, annRet, annVol, excess, sharpe }};
    }}

    function pad() {{ return {{ left: 48, right: 14, top: 16, bottom: 32 }}; }}
    function xPos(i, span, p, w) {{ return p.left + (i / Math.max(1, span - 1)) * (w - p.left - p.right); }}

    function setupCanvas(wrapId, canvas) {{
      const wrap = document.getElementById(wrapId);
      const dpr = window.devicePixelRatio || 1;
      const w = wrap.clientWidth, h = wrap.clientHeight;
      canvas.width = Math.max(1, w * dpr);
      canvas.height = Math.max(1, h * dpr);
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      const ctx = canvas.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return {{ w, h, ctx }};
    }}

    function drawGrid(ctx, w, h, p) {{
      ctx.strokeStyle = '#232a38'; ctx.lineWidth = 1;
      for (let i = 0; i <= 4; i++) {{
        const y = p.top + (i / 4) * (h - p.top - p.bottom);
        ctx.beginPath(); ctx.moveTo(p.left, y); ctx.lineTo(w - p.right, y); ctx.stroke();
      }}
    }}

    function drawReturns(k) {{
      const {{ w, h, ctx }} = setupCanvas('wrapR', cR);
      const p = pad();
      const {{ slice, n }} = sharpeStats(k);
      ctx.clearRect(0, 0, w, h);
      drawGrid(ctx, w, h, p);
      const minV = Math.min(-0.06, ...slice) * 1.1;
      const maxV = Math.max(0.06, ...slice) * 1.1;
      const y = v => p.top + (1 - (v - minV) / (maxV - minV)) * (h - p.top - p.bottom);
      const y0 = y(0);
      ctx.strokeStyle = '#3a4458'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(p.left, y0); ctx.lineTo(w - p.right, y0); ctx.stroke();
      ctx.strokeStyle = '#4da3ff'; ctx.lineWidth = 1.5; ctx.beginPath();
      for (let i = 0; i <= k; i++) {{
        const x = xPos(i, n, p, w), yy = y(slice[i]);
        i === 0 ? ctx.moveTo(x, yy) : ctx.lineTo(x, yy);
      }}
      ctx.stroke();
      const x = xPos(k, n, p, w);
      ctx.fillStyle = '#4da3ff';
      ctx.beginPath(); ctx.arc(x, y(slice[k]), 5, 0, Math.PI * 2); ctx.fill();
    }}

    function drawMetrics(k) {{
      const {{ w, h, ctx }} = setupCanvas('wrapM', cM);
      const p = {{ left: 48, right: 52, top: 16, bottom: 32 }};
      const atEnd = k >= N - 1;
      ctx.clearRect(0, 0, w, h);
      drawGrid(ctx, w, h, p);

      const iEnd = k + 1;
      if (iEnd <= MIN_METRIC_DAYS) {{
        ctx.fillStyle = '#8b95a8';
        ctx.font = '11px IBM Plex Sans,sans-serif';
        ctx.fillText(`样本 n < ${{MIN_METRIC_DAYS}}：年化指标尚不稳定，继续播放…`, p.left + 4, h / 2);
        return;
      }}

      const hist = [];
      for (let i = MIN_METRIC_DAYS; i <= iEnd; i++) {{
        const st = sharpeStats(i - 1);
        hist.push({{ n: i, annRet: st.annRet, annVol: st.annVol, sharpe: st.sharpe }});
      }}

      const iStart = atEnd ? 0 : Math.max(0, hist.length - RUN_WINDOW);
      const win = hist.slice(iStart);

      const pctVals = win.flatMap(h => [h.annRet, h.annVol]);
      const minPct = Math.min(...pctVals, 0);
      const maxPct = Math.max(...pctVals, 0.15);
      const padPct = Math.max(0.02, (maxPct - minPct) * 0.12);

      const shVals = win.map(h => h.sharpe).filter(v => !Number.isNaN(v));
      const minSh = shVals.length ? Math.min(...shVals, 0) : 0;
      const maxSh = shVals.length ? Math.max(...shVals, 1) : 2;
      const padSh = Math.max(0.15, (maxSh - minSh) * 0.12);

      const yPct = v => p.top + (1 - (v - minPct + padPct) / (maxPct - minPct + 2 * padPct)) * (h - p.top - p.bottom);
      const ySh  = v => p.top + (1 - (v - minSh + padSh) / (maxSh - minSh + 2 * padSh)) * (h - p.top - p.bottom);
      const xFor = j => atEnd
        ? xPos(j, Math.max(1, win.length - 1), p, w)
        : p.left + (j / Math.max(1, win.length - 1)) * (w - p.left - p.right);

      function drawSeries(key, yFn, color) {{
        ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.beginPath();
        let started = false;
        win.forEach((row, j) => {{
          const v = row[key];
          if (Number.isNaN(v)) return;
          const x = xFor(j), yy = yFn(v);
          if (!started) {{ ctx.moveTo(x, yy); started = true; }} else ctx.lineTo(x, yy);
        }});
        if (started) ctx.stroke();
      }}

      drawSeries('annRet', yPct, '#2dd4a8');
      drawSeries('annVol', yPct, '#f5a623');
      if (shVals.length) drawSeries('sharpe', ySh, '#3d9cf5');

      if (RF >= minPct - padPct && RF <= maxPct + padPct) {{
        ctx.strokeStyle = 'rgba(245,166,35,0.45)'; ctx.setLineDash([4, 4]); ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(p.left, yPct(RF)); ctx.lineTo(w - p.right, yPct(RF)); ctx.stroke();
        ctx.setLineDash([]);
      }}

      ctx.fillStyle = '#8b95a8'; ctx.font = '10px IBM Plex Sans,sans-serif';
      ctx.fillText(`左轴：年化 %  ·  右轴：Sharpe  ·  n=${{iEnd}}`, p.left + 2, p.top + 12);
      ctx.textAlign = 'right';
      ctx.fillText(`${{(maxSh + padSh).toFixed(1)}}`, w - p.right + 40, p.top + 4);
      ctx.fillText(`${{(minSh - padSh).toFixed(1)}}`, w - p.right + 40, h - p.bottom + 4);
      ctx.textAlign = 'left';
      ctx.fillText(`${{((maxPct + padPct) * 100).toFixed(0)}}%`, p.left - 2, p.top + 4);
      ctx.fillText(`${{((minPct - padPct) * 100).toFixed(0)}}%`, p.left - 2, h - p.bottom + 4);
    }}

    function updateUI(k) {{
      const {{ n, annRet, annVol, excess, sharpe }} = sharpeStats(k);
      document.getElementById('stepPill').textContent = `${{ticker}} · 第 ${{n}} / ${{N}} 日`;
      document.getElementById('progress').style.width = `${{(n / N) * 100}}%`;
      document.getElementById('annRetVal').textContent = `${{(annRet * 100).toFixed(2)}}%`;
      document.getElementById('annVolVal').textContent = `${{(annVol * 100).toFixed(2)}}%`;
      document.getElementById('excessVal').textContent = `${{(excess * 100).toFixed(2)}}%`;
      document.getElementById('sharpeVal').textContent = Number.isNaN(sharpe) ? '—' : sharpe.toFixed(2);
      const sh = Number.isNaN(sharpe) ? '—' : sharpe.toFixed(2);
      document.getElementById('formulaBox').innerHTML =
        `标的：<span class="hl">${{ticker}}</span>  样本 n = <span class="hl">${{n}}</span>\\n` +
        `年化收益 = (1+r̄)^252−1 = <span class="hl">${{(annRet * 100).toFixed(2)}}%</span>\\n` +
        `年化波动 = σ·√252 = <span class="hl">${{(annVol * 100).toFixed(2)}}%</span>\\n` +
        `超额 = 年化收益 − r_f = ${{(annRet * 100).toFixed(2)}}% − ${{(RF * 100).toFixed(0)}}% = ${{(excess * 100).toFixed(2)}}%\\n` +
        (n >= 2
          ? `<span class="result">Sharpe = ${{(excess * 100).toFixed(2)}}% / ${{(annVol * 100).toFixed(2)}}% = ${{sh}}</span>`
          : `<span class="hl">至少需要 2 个交易日</span>`);
    }}

    function draw(k) {{ frame = k; drawReturns(k); drawMetrics(k); updateUI(k); }}

    function pause() {{ playing = false; clearTimeout(timer); document.getElementById('btnPlay').textContent = '▶ 播放'; }}
    function schedule() {{
      clearTimeout(timer); if (!playing) return;
      const ms = 1150 - Number(document.getElementById('speed').value) * 95;
      timer = setTimeout(() => {{
        if (frame < N - 1) {{ draw(frame + 1); schedule(); }} else pause();
      }}, ms);
    }}
    function play() {{
      if (frame >= N - 1) draw(0);
      playing = true;
      document.getElementById('btnPlay').textContent = '▶ 播放中';
      schedule();
    }}
    function step() {{ if (frame < N - 1) draw(frame + 1); else pause(); }}
    function reset() {{ pause(); draw(0); }}

    document.getElementById('btnPlay').addEventListener('click', () => playing ? pause() : play());
    document.getElementById('btnPause').addEventListener('click', pause);
    document.getElementById('btnStep').addEventListener('click', () => {{ pause(); step(); }});
    document.getElementById('btnReset').addEventListener('click', reset);
    document.getElementById('speed').addEventListener('input', () => {{ if (playing) schedule(); }});

    const nav = document.getElementById('tickerNav');
    TICKERS.forEach(t => {{
      const b = document.createElement('button');
      b.className = 'tbtn' + (t === ticker ? ' active' : '');
      b.textContent = t;
      b.addEventListener('click', () => {{
        ticker = t;
        nav.querySelectorAll('.tbtn').forEach(x => x.classList.toggle('active', x.textContent === t));
        pause(); draw(0);
      }});
      nav.appendChild(b);
    }});

    window.addEventListener('resize', () => draw(frame));
    draw(0);
  </script>
</body>
</html>
"""

OUT.write_text(HTML, encoding="utf-8")
print(f"wrote {OUT}")
