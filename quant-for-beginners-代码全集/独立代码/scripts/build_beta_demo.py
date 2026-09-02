#!/usr/bin/env python3
"""生成 Beta 动态演示 HTML（数据来自 AkShare 美股日线）。"""
import json
from pathlib import Path

import akshare as ak
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "interactive" / "beta-demo.html"

ALL_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "NVDA", "TSLA", "AMD", "JPM", "SPY",
]
STOCKS = [t for t in ALL_TICKERS if t != "SPY"]
MARKET = "SPY"
PERIOD_YEARS = 3
SAMPLE_DAYS = 300

start = (pd.Timestamp.today() - pd.DateOffset(years=PERIOD_YEARS, days=30)).strftime("%Y-%m-%d")


def fetch_returns(symbol: str) -> list[float]:
    df = ak.stock_us_daily(symbol=symbol, adjust="qfq")
    df["date"] = pd.to_datetime(df["date"])
    close = df.set_index("date").sort_index()["close"]
    close = close.loc[close.index >= start]
    r = close.pct_change().dropna().tail(SAMPLE_DAYS)
    return [round(x, 6) for x in r.tolist()]


print("fetching AkShare data …")
RETURNS = {t: fetch_returns(t) for t in ALL_TICKERS}
N = min(len(v) for v in RETURNS.values())
print(f"embedded {len(ALL_TICKERS)} tickers × {N} daily returns")

returns_js = json.dumps(RETURNS, ensure_ascii=False, indent=2)
stocks_js = json.dumps(STOCKS, ensure_ascii=False)

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Beta 动态演示 · Quant for Beginners</title>
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
    .app {{ height: 100vh; display: grid; grid-template-rows: auto auto 1fr;gap: 8px; padding: 10px 14px; max-width: 1400px; margin: 0 auto; }}
    .topbar {{ display: flex; align-items: center; justify-content: space-between;gap: 12px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }}
    .topbar h1 {{ font-size: 1rem; font-weight: 600; }}
    .topbar .eq {{ font-family: var(--mono); font-size: 0.74rem; color: var(--accent); margin-left: 10px; }}
    .pill {{ font-size: 0.74rem; color: var(--muted); background: var(--surface); border: 1px solid var(--border); border-radius: 999px; padding: 4px 12px; white-space: nowrap; }}
    .tickers {{ display: flex; flex-wrap: wrap;gap: 5px; }}
    .tbtn {{ font-family: var(--font); font-size: 0.68rem; padding: 4px 10px; border-radius: 7px; border: 1px solid var(--border); background: var(--surface); color: var(--muted); cursor: pointer; }}
    .tbtn:hover {{ border-color: var(--accent); color: var(--text); }}
    .tbtn.active {{ background: var(--accent); border-color: var(--accent); color: #0a0e12; font-weight: 600; }}
    .layout {{ display: grid; grid-template-columns: 320px 1fr;gap: 10px; min-height: 0; }}
    @media (max-width: 980px) {{ html, body {{ overflow: auto; height: auto; }} .app {{ height: auto; min-height: 100vh; }} .layout {{ grid-template-columns: 1fr; }} }}
    .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }}
    .left {{ display: grid; grid-template-rows: 1fr auto auto;gap: 8px; min-height: 0; }}
    .section-title {{ padding: 7px 12px; font-size: 0.68rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid var(--border); }}
    .formula {{ padding: 10px 12px; font-family: var(--mono); font-size: 0.72rem; line-height: 1.68; white-space: pre-line; overflow-y: auto; max-height: 240px; }}
    .formula .hl {{ color: var(--accent); }}
    .formula .result {{ font-size: 0.95rem; font-weight: 500; margin-top: 4px; color: var(--green); }}
    .stats {{ display: grid; grid-template-columns: repeat(2, 1fr);gap: 5px; padding: 0 10px 10px; }}
    .stat {{ background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 7px; text-align: center; }}
    .stat label {{ display: block; font-size: 0.58rem; color: var(--muted); text-transform: uppercase; margin-bottom: 2px; }}
    .stat span {{ font-family: var(--mono); font-size: 0.8rem; font-weight: 500; }}
    .controls {{ padding: 9px 12px; }}
    .btn-row {{ display: grid; grid-template-columns: repeat(4, 1fr);gap: 5px; margin-bottom: 8px; }}
    .btn {{ font-family: var(--font); font-size: 0.72rem; font-weight: 500; padding: 6px 3px; border-radius: 7px; border: 1px solid var(--border); background: var(--surface2); color: var(--text); cursor: pointer; }}
    .btn:hover {{ border-color: var(--accent); }}
    .btn.primary {{ background: var(--accent); border-color: var(--accent); color: #0a0e12; }}
    .speed {{ display: flex; align-items: center;gap: 8px; font-size: 0.72rem; color: var(--muted); }}
    .speed input {{ flex: 1; accent-color: var(--accent); }}
    .progress {{ height: 3px; background: var(--border); margin-top: 8px; }}
    .progress-fill {{ height: 100%; background: var(--accent); width: 0%; transition: width 0.08s linear; }}
    .legend {{ padding: 7px 12px; display: flex; flex-wrap: wrap;gap: 8px 12px; font-size: 0.66rem; color: var(--muted); }}
    .legend-item {{ display: flex; align-items: center;gap: 4px; }}
    .sw {{ width: 9px; height: 9px; border-radius: 50%; }}
    .sw.line {{ width: 12px; height: 3px; border-radius: 2px; }}
    .right {{ display: grid; grid-template-rows: 1fr 1fr;gap: 8px; min-height: 0; }}
    .chart {{ display: flex; flex-direction: column; min-height: 0; }}
    .chart-wrap {{ flex: 1; min-height: 0; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div class="app">
    <header class="topbar">
      <div>
        <h1>Beta 动态演示<span class="eq">β = Cov(R股, R市) / Var(R市)</span></h1>
      </div>
      <div class="pill" id="stepPill">—</div>
    </header>
    <nav class="tickers" id="tickerNav"></nav>
    <div class="layout">
      <aside class="left">
        <div class="card">
          <div class="section-title">逐步代入 · 大盘 = SPY</div>
          <div class="formula" id="formulaBox">▶ 选择个股后点击「播放」</div>
          <div class="stats">
            <div class="stat"><label>Cov(股,市)</label><span id="covVal">—</span></div>
            <div class="stat"><label>Var(市)</label><span id="varVal">—</span></div>
            <div class="stat"><label>β(numpy)</label><span id="betaNpVal">—</span></div>
            <div class="stat"><label>β(pandas)</label><span id="betaPdVal">—</span></div>
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
          <div class="legend-item"><span class="sw line" style="background:#4da3ff"></span> 个股 R</div>
          <div class="legend-item"><span class="sw line" style="background:var(--orange)"></span> 大盘 SPY</div>
          <div class="legend-item"><span class="sw line" style="background:var(--accent)"></span> β 演化</div>
          <div class="legend-item"><span class="sw line" style="background:var(--muted)"></span> β = 1 参考线</div>
        </div>
      </aside>
      <main class="right">
        <div class="card chart">
          <div class="section-title">日收益率：个股 vs SPY</div>
          <div class="chart-wrap" id="wrapR"><canvas id="canvasR"></canvas></div>
        </div>
        <div class="card chart">
          <div class="section-title">Beta 的演化</div>
          <div class="chart-wrap" id="wrapB"><canvas id="canvasB"></canvas></div>
        </div>
      </main>
    </div>
  </div>
  <script>
    const RETURNS = {returns_js};
    const STOCKS = {stocks_js};
    const MARKET = "{MARKET}";
    const N = {N};
    const RUN_WINDOW = 60;
    const MIN_DAYS = 20;

    let ticker = STOCKS[0];
    let frame = 0, playing = false, timer = null;

    const cR = document.getElementById('canvasR');
    const cB = document.getElementById('canvasB');

    function stockR() {{ return RETURNS[ticker]; }}
    function mktR() {{ return RETURNS[MARKET]; }}

    function betaStats(k) {{
      const s = stockR().slice(0, k + 1);
      const m = mktR().slice(0, k + 1);
      const n = s.length;
      const meanS = s.reduce((a, b) => a + b, 0) / n;
      const meanM = m.reduce((a, b) => a + b, 0) / n;
      let sumCov = 0, sumVarM = 0, sumVarS = 0;
      for (let i = 0; i < n; i++) {{
        const ds = s[i] - meanS, dm = m[i] - meanM;
        sumCov += ds * dm;
        sumVarM += dm * dm;
        sumVarS += ds * ds;
      }}
      const denom = Math.max(1, n - 1);
      const covSM = sumCov / denom;
      const varM = sumVarM / denom;
      const varS = sumVarS / denom;
      const betaNp = n >= 2 && varM > 0 ? covSM / varM : NaN;
      const betaPd = betaNp;
      return {{ s, m, n, covSM, varM, varS, betaNp, betaPd }};
    }}

    function pad() {{ return {{ left: 48, right: 14, top: 16, bottom: 32 }}; }}
    function xPos(i, span, p, w) {{ return p.l + (i / Math.max(1, span - 1)) * (w - p.l - p.r); }}

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
        const y = p.t + (i / 4) * (h - p.t - p.b);
        ctx.beginPath(); ctx.moveTo(p.l, y); ctx.lineTo(w - p.r, y); ctx.stroke();
      }}
    }}

    function drawReturns(k) {{
      const {{ w, h, ctx }} = setupCanvas('wrapR', cR);
      const p = {{ l: 48, r: 14, t: 16, b: 32 }};
      const {{ s, m, n }} = betaStats(k);
      ctx.clearRect(0, 0, w, h);
      drawGrid(ctx, w, h, p);
      const all = [...s, ...m];
      const minV = Math.min(-0.06, ...all) * 1.1;
      const maxV = Math.max(0.06, ...all) * 1.1;
      const y = v => p.t + (1 - (v - minV) / (maxV - minV)) * (h - p.t - p.b);
      const y0 = y(0);
      ctx.strokeStyle = '#3a4458'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(p.l, y0); ctx.lineTo(w - p.r, y0); ctx.stroke();

      function line(data, color) {{
        ctx.strokeStyle = color; ctx.lineWidth = 1.5; ctx.beginPath();
        for (let i = 0; i <= k; i++) {{
          const x = xPos(i, n, p, w), yy = y(data[i]);
          i === 0 ? ctx.moveTo(x, yy) : ctx.lineTo(x, yy);
        }}
        ctx.stroke();
        const x = xPos(k, n, p, w);
        ctx.fillStyle = color;
        ctx.beginPath(); ctx.arc(x, y(data[k]), 4, 0, Math.PI * 2); ctx.fill();
      }}
      line(s, '#4da3ff');
      line(m, '#f5a623');
    }}

    function drawBeta(k) {{
      const {{ w, h, ctx }} = setupCanvas('wrapB', cB);
      const p = {{ l: 48, r: 48, t: 16, b: 32 }};
      const atEnd = k >= N - 1;
      ctx.clearRect(0, 0, w, h);
      drawGrid(ctx, w, h, p);

      if (k + 1 < MIN_DAYS) {{
        ctx.fillStyle = '#8b95a8'; ctx.font = '11px IBM Plex Sans,sans-serif';
        ctx.fillText(`样本 n < ${{MIN_DAYS}}：Cov/Var 尚不稳定，继续播放…`, p.l + 4, h / 2);
        return;
      }}

      const hist = [];
      for (let i = MIN_DAYS; i <= k + 1; i++) {{
        const st = betaStats(i - 1);
        hist.push({{ n: i, beta: st.betaNp }});
      }}
      const win = atEnd ? hist : hist.slice(Math.max(0, hist.length - RUN_WINDOW));

      const betas = win.map(h => h.beta).filter(v => !Number.isNaN(v));
      if (!betas.length) return;

      const minB = Math.min(...betas, 0);
      const maxB = Math.max(...betas, 2);
      const padB = Math.max(0.2, (maxB - minB) * 0.15);
      const yB = v => p.t + (1 - (v - minB + padB) / (maxB - minB + 2 * padB)) * (h - p.t - p.b);
      const xFor = j => atEnd
        ? xPos(j, Math.max(1, win.length - 1), p, w)
        : p.l + (j / Math.max(1, win.length - 1)) * (w - p.l - p.r);

      if (1 >= minB - padB && 1 <= maxB + padB) {{
        ctx.strokeStyle = 'rgba(139,149,168,0.5)'; ctx.setLineDash([5, 4]); ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(p.l, yB(1)); ctx.lineTo(w - p.r, yB(1)); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#8b95a8'; ctx.font = '9px IBM Plex Sans,sans-serif';
        ctx.fillText('β=1', w - p.r - 28, yB(1) - 4);
      }}

      ctx.strokeStyle = '#3d9cf5'; ctx.lineWidth = 2.2; ctx.beginPath();
      let started = false;
      win.forEach((row, j) => {{
        if (Number.isNaN(row.beta)) return;
        const x = xFor(j), yy = yB(row.beta);
        if (!started) {{ ctx.moveTo(x, yy); started = true; }} else ctx.lineTo(x, yy);
      }});
      if (started) ctx.stroke();

      ctx.fillStyle = '#8b95a8'; ctx.font = '10px IBM Plex Sans,sans-serif';
      ctx.fillText(`${{ticker}} vs SPY  ·  n=${{k + 1}}`, p.l + 2, p.t + 12);
      ctx.textAlign = 'right';
      ctx.fillText(maxB.toFixed(1), w - p.r + 38, p.t + 4);
      ctx.fillText(minB.toFixed(1), w - p.r + 38, h - p.b + 4);
      ctx.textAlign = 'left';
    }}

    function updateUI(k) {{
      const {{ n, covSM, varM, betaNp, betaPd }} = betaStats(k);
      document.getElementById('stepPill').textContent = `${{ticker}} vs SPY · 第 ${{n}} / ${{N}} 日`;
      document.getElementById('progress').style.width = `${{(n / N) * 100}}%`;
      document.getElementById('covVal').textContent = n >= 2 ? covSM.toExponential(3) : '—';
      document.getElementById('varVal').textContent = n >= 2 ? varM.toExponential(3) : '—';
      document.getElementById('betaNpVal').textContent = Number.isNaN(betaNp) ? '—' : betaNp.toFixed(2);
      document.getElementById('betaPdVal').textContent = Number.isNaN(betaPd) ? '—' : betaPd.toFixed(2);
      const b = Number.isNaN(betaNp) ? '—' : betaNp.toFixed(2);
      const tag = Number.isNaN(betaNp) ? '' : betaNp > 1.05 ? '（比大盘更冲）' : betaNp < 0.95 ? '（比大盘更稳）' : '（接近大盘）';
      document.getElementById('formulaBox').innerHTML =
        `个股：<span class="hl">${{ticker}}</span>  大盘：<span class="hl">SPY</span>  n=<span class="hl">${{n}}</span>\\n` +
        (n >= 2
          ? `Cov(R_股,R_市) = <span class="hl">${{covSM.toExponential(3)}}</span>\\n` +
            `Var(R_市) = <span class="hl">${{varM.toExponential(3)}}</span>\\n` +
            `<span class="result">β = ${{covSM.toExponential(3)}} / ${{varM.toExponential(3)}} = ${{b}} ${{tag}}</span>`
          : `<span class="hl">至少需要 2 个交易日</span>`);
    }}

    function draw(k) {{ frame = k; drawReturns(k); drawBeta(k); updateUI(k); }}

    function pause() {{ playing = false; clearTimeout(timer); document.getElementById('btnPlay').textContent = '▶ 播放'; }}
    function schedule() {{
      clearTimeout(timer); if (!playing) return;
      const ms = 1150 - Number(document.getElementById('speed').value) * 95;
      timer = setTimeout(() => {{ if (frame < N - 1) {{ draw(frame + 1); schedule(); }} else pause(); }}, ms);
    }}
    function play() {{ if (frame >= N - 1) draw(0); playing = true; document.getElementById('btnPlay').textContent = '▶ 播放中'; schedule(); }}
    function step() {{ if (frame < N - 1) draw(frame + 1); else pause(); }}
    function reset() {{ pause(); draw(0); }}

    document.getElementById('btnPlay').addEventListener('click', () => playing ? pause() : play());
    document.getElementById('btnPause').addEventListener('click', pause);
    document.getElementById('btnStep').addEventListener('click', () => {{ pause(); step(); }});
    document.getElementById('btnReset').addEventListener('click', reset);
    document.getElementById('speed').addEventListener('input', () => {{ if (playing) schedule(); }});

    const nav = document.getElementById('tickerNav');
    STOCKS.forEach(t => {{
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

OUT.write_text(HTML,encoding="utf-8")
print(f"wrote {OUT}")
