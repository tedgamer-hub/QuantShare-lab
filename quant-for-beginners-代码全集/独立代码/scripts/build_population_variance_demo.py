#!/usr/bin/env python3
"""生成总体方差动态演示 HTML。"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "interactive" / "population-variance-demo.html"

PRICES = [
    180.0, 179.18, 176.29, 177.05, 177.13, 180.32,
    181.07, 179.38, 176.05, 177.45, 176.88, 176.83,
    175.64, 171.54, 173.51, 174.62, 175.19, 176.69,
    174.15, 178.37, 177.8, 178.67, 180.38, 174.59,
    178.2, 178.43, 174.9, 174.25, 180.06, 179.65,
    176.69, 176.44, 177.37, 176.15, 174.98, 177.57,
    179.45, 179.55, 179.51, 179.93, 179.1, 179.19,
    179.59, 182.88, 180.43, 182.57, 186.34, 184.54,
    185.06, 185.73, 185.48, 184.53, 182.43, 177.69,
    179.03, 172.1, 173.26, 175.26, 173.2, 174.47,
    176.07, 177.69, 176.85, 177.7, 178.24, 176.62,
    175.61, 177.08, 176.04, 177.1, 177.4, 177.01,
    177.36, 178.19, 178.46, 178.96, 180.55, 180.3,
    180.88, 180.58, 181.58, 181.45, 183.13, 185.7,
    182.72, 185.91, 188.69, 187.05, 192.56, 193.23,
    194.58, 198.69, 197.33, 194.83, 194.2, 194.73,
    195.78, 197.57, 201.73, 199.98, 197.2, 198.07,
    198.14, 198.09, 194.97, 196.67, 198.34, 197.79,
    204.36, 201.58, 204.18, 202.89, 200.93, 198.23,
    200.81, 199.47, 198.43, 197.59, 198.73, 201.67,
    202.66, 205.92, 209.48, 208.63, 209.7, 212.2,
    214.37, 214.97, 219.33, 219.04, 218.82, 220.12,
    220.04, 217.77, 220.99, 221.47, 224.45, 228.07,
    225.2, 227.16, 226.31, 227.49, 229.67, 228.2,
    226.03, 226.53, 226.18, 225.28, 226.67, 226.74,
    228.54, 230.78, 229.38, 228.44, 229.76, 230.89,
    231.84, 236.33, 241.09, 236.86, 237.46, 237.3,
    235.0, 230.98, 225.35, 224.96, 224.09, 225.01,
    224.53, 226.85, 230.17, 228.54, 227.31, 231.12,
    229.04, 233.94, 239.95, 239.24, 239.81, 241.23,
    237.92, 244.01, 238.08, 238.2, 237.43, 243.36,
    243.87, 239.92, 241.68, 242.83, 246.83, 241.94,
    245.05, 248.45, 246.74, 244.24, 242.56, 245.9,
    248.51, 247.3, 250.13, 254.2, 253.47, 257.27,
    256.23, 255.33, 255.11, 256.2, 250.05, 247.04,
    240.26, 242.24, 246.07, 250.52, 244.78, 245.08,
    241.74, 237.97, 236.47, 232.92, 238.77, 234.67,
    232.01, 231.64, 231.91, 232.09, 228.89, 229.66,
    230.52, 232.58, 232.2, 234.96, 231.01, 234.75,
    237.26, 238.3, 239.75, 242.67, 245.27, 242.31,
    245.66, 246.43, 250.0, 251.34, 248.5, 245.37,
    246.76, 250.12, 245.78, 244.9, 248.13, 247.18,
]
LOG = [round(math.log(PRICES[i] / PRICES[i - 1]), 6) for i in range(1, len(PRICES))]
arr = "\n".join(
    "      " + ", ".join(str(x) for x in LOG[i : i + 8]) + ","
    for i in range(0, len(LOG), 8)
)

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>总体方差动态演示 · Quant for Beginners</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0c0f14; --surface: #151a22; --surface2: #1c2330; --border: #2a3344;
      --text: #e8ecf4; --muted: #8b95a8; --accent: #3d9cf5; --green: #2dd4a8; --red: #f07178;
      --radius: 10px; --font: "IBM Plex Sans", system-ui, sans-serif; --mono: "IBM Plex Mono", ui-monospace, monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ height: 100%; overflow: hidden; }}
    body {{ font-family: var(--font); background: var(--bg); color: var(--text); line-height: 1.5; }}
    .app {{ height: 100vh; display: grid; grid-template-rows: auto 1fr; gap: 10px; padding: 12px 14px; max-width: 1400px; margin: 0 auto; }}
    .topbar {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }}
    .topbar h1 {{ font-size: 1.05rem; font-weight: 600; }}
    .topbar .eq {{ font-family: var(--mono); font-size: 0.78rem; color: var(--accent); margin-left: 12px; }}
    .topbar .pill {{ font-size: 0.76rem; color: var(--muted); background: var(--surface); border: 1px solid var(--border); border-radius: 999px; padding: 4px 12px; }}
    .layout {{ display: grid; grid-template-columns: 330px 1fr; gap: 12px; min-height: 0; }}
    @media (max-width: 980px) {{ html, body {{ overflow: auto; height: auto; }} .app {{ height: auto; min-height: 100vh; }} .layout {{ grid-template-columns: 1fr; }} }}
    .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }}
    .left {{ display: grid; grid-template-rows: 1fr auto auto; gap: 10px; min-height: 0; }}
    .section-title {{ padding: 8px 12px; font-size: 0.72rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid var(--border); }}
    .formula {{ padding: 12px; font-family: var(--mono); font-size: 0.76rem; line-height: 1.72; white-space: pre-line; overflow-y: auto; }}
    .formula .hl {{ color: var(--accent); }}
    .formula .result {{ font-size: 1.02rem; font-weight: 500; margin-top: 6px; }}
    .stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; padding: 0 12px 12px; }}
    .stat {{ background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 8px; text-align: center; }}
    .stat label {{ display: block; font-size: 0.62rem; color: var(--muted); text-transform: uppercase; margin-bottom: 3px; }}
    .stat span {{ font-family: var(--mono); font-size: 0.86rem; font-weight: 500; }}
    .controls {{ padding: 10px 12px; }}
    .btn-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 10px; }}
    .btn {{ font-family: var(--font); font-size: 0.76rem; font-weight: 500; padding: 7px 4px; border-radius: 7px; border: 1px solid var(--border); background: var(--surface2); color: var(--text); cursor: pointer; }}
    .btn:hover {{ border-color: var(--accent); }}
    .btn.primary {{ background: var(--accent); border-color: var(--accent); color: #0a0e12; }}
    .speed {{ display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: var(--muted); }}
    .speed input {{ flex: 1; accent-color: var(--accent); }}
    .progress {{ height: 3px; background: var(--border); margin-top: 10px; }}
    .progress-fill {{ height: 100%; background: var(--accent); width: 0%; transition: width 0.08s linear; }}
    .legend {{ padding: 8px 12px; display: flex; flex-wrap: wrap; gap: 10px 14px; font-size: 0.7rem; color: var(--muted); }}
    .legend-item {{ display: flex; align-items: center; gap: 5px; }}
    .sw {{ width: 10px; height: 10px; border-radius: 50%; }}
    .sw.line {{ width: 14px; height: 3px; border-radius: 2px; }}
    .right {{ display: grid; grid-template-rows: 1fr 1fr; gap: 10px; min-height: 0; }}
    .chart {{ display: flex; flex-direction: column; min-height: 0; }}
    .chart-wrap {{ flex: 1; min-height: 0; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div class="app">
    <header class="topbar">
      <div><h1>总体方差动态演示<span class="eq">s² = (1/N) · Σ(xⱼ-x̄)²</span></h1></div>
      <div class="pill" id="stepPill">第 1 / {len(LOG)} 个样本</div>
    </header>
    <div class="layout">
      <aside class="left">
        <div class="card">
          <div class="section-title">逐步代入公式 (2-1a)</div>
          <div class="formula" id="formulaBox">▶ 点击「播放」开始演示</div>
          <div class="stats">
            <div class="stat"><label>x̄（均值）</label><span id="meanVal">—</span></div>
            <div class="stat"><label>当前 xⱼ</label><span id="xjVal">—</span></div>
            <div class="stat"><label>Σ(xⱼ-x̄)²</label><span id="sumSqVal">—</span></div>
            <div class="stat"><label>s²（总体）</label><span id="varVal">—</span></div>
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
          <div class="legend-item"><span class="sw" style="background:#4da3ff"></span> 当前 xⱼ</div>
          <div class="legend-item"><span class="sw line" style="background:#f5a623"></span> 均值 x̄</div>
          <div class="legend-item"><span class="sw line" style="background:var(--accent)"></span> 偏差平方柱</div>
        </div>
      </aside>
      <main class="right">
        <div class="card chart">
          <div class="section-title">对数收益率 xⱼ 与均值 x̄</div>
          <div class="chart-wrap" id="wrapX"><canvas id="canvasX"></canvas></div>
        </div>
        <div class="card chart">
          <div class="section-title">偏差平方 (xⱼ-x̄)² 累加过程</div>
          <div class="chart-wrap" id="wrapSq"><canvas id="canvasSq"></canvas></div>
        </div>
      </main>
    </div>
  </div>
  <script>
    // 251 个对数收益率 xⱼ（约一年，ln(Pⱼ/Pⱼ₋₁)）
    const LOG_RETURNS = [
{arr}
    ];
    const N = LOG_RETURNS.length;

    function popStats(k) {{
      const slice = LOG_RETURNS.slice(0, k + 1);
      const n = slice.length;
      const mean = slice.reduce((a, b) => a + b, 0) / n;
      const sq = slice.map(x => (x - mean) * (x - mean));
      const sumSq = sq.reduce((a, b) => a + b, 0);
      const varPop = sumSq / n;
      return {{ slice, mean, sq, sumSq, varPop, n }};
    }}

    let frame = 0, playing = false, timer = null;
    const cX = document.getElementById('canvasX');
    const cSq = document.getElementById('canvasSq');
    const xCtx = cX.getContext('2d');
    const sCtx = cSq.getContext('2d');
    const formulaBox = document.getElementById('formulaBox');
    const stepPill = document.getElementById('stepPill');
    const progress = document.getElementById('progress');
    const meanVal = document.getElementById('meanVal');
    const xjVal = document.getElementById('xjVal');
    const sumSqVal = document.getElementById('sumSqVal');
    const varVal = document.getElementById('varVal');

    function pad() {{ return {{ left: 48, right: 14, top: 14, bottom: 30 }}; }}
    function xPos(i, span, p, w) {{ return p.left + (i / Math.max(1, span - 1)) * (w - p.left - p.right); }}

    function resize() {{
      [['wrapX', cX, xCtx], ['wrapSq', cSq, sCtx]].forEach(([id, canvas, ctx]) => {{
        const wrap = document.getElementById(id);
        const dpr = window.devicePixelRatio || 1;
        const w = wrap.clientWidth, h = wrap.clientHeight;
        canvas.width = Math.max(1, w * dpr);
        canvas.height = Math.max(1, h * dpr);
        canvas.style.width = w + 'px';
        canvas.style.height = h + 'px';
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      }});
      draw(frame);
    }}

    function drawGrid(ctx, w, h, p) {{
      ctx.strokeStyle = '#232a38';
      ctx.lineWidth = 1;
      for (let i = 0; i <= 4; i++) {{
        const y = p.top + (i / 4) * (h - p.top - p.bottom);
        ctx.beginPath(); ctx.moveTo(p.left, y); ctx.lineTo(w - p.right, y); ctx.stroke();
      }}
    }}

    function drawReturns(k) {{
      const w = cX.width / (window.devicePixelRatio || 1);
      const h = cX.height / (window.devicePixelRatio || 1);
      const p = pad();
      const {{ slice, mean }} = popStats(k);
      const span = slice.length;
      xCtx.clearRect(0, 0, w, h);
      drawGrid(xCtx, w, h, p);
      const minV = Math.min(-0.04, ...slice, mean) * 1.08;
      const maxV = Math.max(0.035, ...slice, mean) * 1.08;
      const y = v => p.top + (1 - (v - minV) / (maxV - minV)) * (h - p.top - p.bottom);
      const yMean = y(mean);
      xCtx.strokeStyle = '#f5a623';
      xCtx.lineWidth = 1.8;
      xCtx.beginPath(); xCtx.moveTo(p.left, yMean); xCtx.lineTo(w - p.right, yMean); xCtx.stroke();
      xCtx.fillStyle = '#f5a623';
      xCtx.font = '10px IBM Plex Sans, sans-serif';
      xCtx.fillText(`x̄=${{(mean * 100).toFixed(2)}}%`, p.left + 4, yMean - 6);
      xCtx.strokeStyle = '#4da3ff';
      xCtx.lineWidth = 1.6;
      xCtx.beginPath();
      for (let i = 0; i <= k; i++) {{
        const x = xPos(i, span, p, w), yy = y(LOG_RETURNS[i]);
        i === 0 ? xCtx.moveTo(x, yy) : xCtx.lineTo(x, yy);
      }}
      xCtx.stroke();
      const x = xPos(k, span, p, w), yk = y(LOG_RETURNS[k]);
      xCtx.fillStyle = '#4da3ff';
      xCtx.beginPath(); xCtx.arc(x, yk, 5, 0, Math.PI * 2); xCtx.fill();
      xCtx.strokeStyle = 'rgba(77,163,255,0.35)';
      xCtx.setLineDash([3, 3]);
      xCtx.beginPath(); xCtx.moveTo(x, yMean); xCtx.lineTo(x, yk); xCtx.stroke();
      xCtx.setLineDash([]);
    }}

    function drawSquares(k) {{
      const w = cSq.width / (window.devicePixelRatio || 1);
      const h = cSq.height / (window.devicePixelRatio || 1);
      const p = pad();
      const {{ sq, sumSq, n }} = popStats(k);
      sCtx.clearRect(0, 0, w, h);
      drawGrid(sCtx, w, h, p);
      const maxSq = Math.max(0.0015, ...sq) * 1.1;
      const y = v => p.top + (1 - v / maxSq) * (h - p.top - p.bottom);
      const y0 = y(0);
      const barW = Math.max(2, Math.min(10, (w - p.left - p.right) / n * 0.72));
      for (let i = 0; i <= k; i++) {{
        const x = xPos(i, n, p, w), yy = y(sq[i]);
        sCtx.fillStyle = i === k ? '#4da3ff' : 'rgba(61,156,245,0.55)';
        sCtx.fillRect(x - barW / 2, yy, barW, Math.max(1, y0 - yy));
      }}
      sCtx.fillStyle = '#8b95a8';
      sCtx.font = '10px IBM Plex Sans, sans-serif';
      sCtx.fillText(`Σ(xⱼ-x̄)² = ${{sumSq.toFixed(6)}}`, p.left + 2, p.top + 12);
    }}

    function updateUI(k) {{
      const {{ mean, sumSq, varPop, n }} = popStats(k);
      const xj = LOG_RETURNS[k];
      const dev = xj - mean;
      stepPill.textContent = `第 ${{n}} / ${{N}} 个样本`;
      progress.style.width = `${{(n / N) * 100}}%`;
      meanVal.textContent = `${{(mean * 100).toFixed(2)}}%`;
      xjVal.textContent = `${{(xj * 100).toFixed(2)}}%`;
      sumSqVal.textContent = sumSq.toFixed(6);
      varVal.textContent = varPop.toExponential(3);
      formulaBox.innerHTML =
        `当前样本：j = <span class="hl">${{n}}</span>\\n` +
        `xⱼ = ${{(xj * 100).toFixed(2)}}% ,  x̄ = ${{(mean * 100).toFixed(2)}}%\\n` +
        `(xⱼ-x̄)² = (${{xj.toFixed(4)}} - ${{mean.toFixed(4)}})² = ${{(dev * dev).toFixed(6)}}\\n` +
        `Σ(xⱼ-x̄)²(前${{n}}项) = ${{sumSq.toFixed(6)}}\\n` +
        `<span class="result">s² = ${{sumSq.toFixed(6)}} / ${{n}} = ${{varPop.toExponential(3)}}</span>\\n` +
        `<span class="hl">（注意：除以 N，不是 N-1）</span>`;
    }}

    function draw(k) {{ frame = k; drawReturns(k); drawSquares(k); updateUI(k); }}
    function step() {{ if (frame < N - 1) draw(frame + 1); else pause(); }}
    function play() {{ if (frame >= N - 1) draw(0); playing = true; document.getElementById('btnPlay').textContent = '▶ 播放中'; schedule(); }}
    function pause() {{ playing = false; clearTimeout(timer); document.getElementById('btnPlay').textContent = '▶ 播放'; }}
    function schedule() {{
      clearTimeout(timer); if (!playing) return;
      const ms = 1150 - Number(document.getElementById('speed').value) * 95;
      timer = setTimeout(() => {{ if (frame < N - 1) {{ draw(frame + 1); schedule(); }} else pause(); }}, ms);
    }}
    function reset() {{ pause(); draw(0); }}

    document.getElementById('btnPlay').addEventListener('click', () => playing ? pause() : play());
    document.getElementById('btnPause').addEventListener('click', pause);
    document.getElementById('btnStep').addEventListener('click', () => {{ pause(); step(); }});
    document.getElementById('btnReset').addEventListener('click', reset);
    document.getElementById('speed').addEventListener('input', () => {{ if (playing) schedule(); }});
    window.addEventListener('resize', resize);
    resize(); draw(0);
  </script>
</body>
</html>
"""

OUT.write_text(HTML, encoding="utf-8")
print(f"wrote {OUT}")
