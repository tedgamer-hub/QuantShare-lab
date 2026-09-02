#!/usr/bin/env python3
"""生成方差修正四种公式合一的动态演示 HTML。"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "interactive" / "variance-formulas-demo.html"

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
N = len(LOG)

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>方差修正四种公式 · 动态演示</title>
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
    .topbar .sub {{ font-size: 0.72rem; color: var(--muted); margin-top: 2px; }}
    .pill {{ font-size: 0.74rem; color: var(--muted); background: var(--surface); border: 1px solid var(--border); border-radius: 999px; padding: 4px 12px; white-space: nowrap; }}
    .tabs {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .tab {{ font-family: var(--font); font-size: 0.72rem; padding: 6px 12px; border-radius: 8px; border: 1px solid var(--border); background: var(--surface); color: var(--muted); cursor: pointer; }}
    .tab:hover {{ border-color: var(--accent); color: var(--text); }}
    .tab.active {{ background: var(--accent); border-color: var(--accent); color: #0a0e12; font-weight: 600; }}
    .scene {{ display: none; grid-template-columns: 320px 1fr; gap: 10px; min-height: 0; }}
    .scene.active {{ display: grid; }}
    @media (max-width: 980px) {{ html, body {{ overflow: auto; height: auto; }} .app {{ height: auto; min-height: 100vh; }} .scene.active {{ grid-template-columns: 1fr; }} }}
    .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }}
    .left {{ display: grid; grid-template-rows: 1fr auto auto; gap: 8px; min-height: 0; }}
    .section-title {{ padding: 7px 12px; font-size: 0.68rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid var(--border); }}
    .formula {{ padding: 10px 12px; font-family: var(--mono); font-size: 0.72rem; line-height: 1.68; white-space: pre-line; overflow-y: auto; max-height: 220px; }}
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
    .right.single {{ grid-template-rows: 1fr; }}
    .chart {{ display: flex; flex-direction: column; min-height: 0; }}
    .chart-wrap {{ flex: 1; min-height: 0; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div class="app">
    <header class="topbar">
      <div>
        <h1 id="sceneTitle">方差修正 · 动态演示</h1>
        <div class="sub" id="sceneEq">四种公式合一 · 点击标签切换</div>
      </div>
      <div class="pill" id="stepPill">—</div>
    </header>
    <nav class="tabs">
      <button class="tab active" data-scene="2-1b">(2-1b) 忽略均值</button>
      <button class="tab" data-scene="2-2">(2-2)(2-3) 无偏估计</button>
      <button class="tab" data-scene="jensen">詹森不等式</button>
      <button class="tab" data-scene="2-4">(2-4) s 的分布</button>
    </nav>

    <!-- Scene 1: 2-1b -->
    <div class="scene active" id="scene-2-1b">
      <aside class="left">
        <div class="card">
          <div class="section-title">逐步代入 (2-1b) · 假设 x̄≈0</div>
          <div class="formula" id="f1">▶ 点击「播放」</div>
          <div class="stats">
            <div class="stat"><label>当前 xⱼ</label><span id="s1xj">—</span></div>
            <div class="stat"><label>xⱼ²</label><span id="s1sq">—</span></div>
            <div class="stat"><label>Σxⱼ²</label><span id="s1sum">—</span></div>
            <div class="stat"><label>s²</label><span id="s1var">—</span></div>
          </div>
        </div>
        <div class="card controls" data-ctrl="step">
          <div class="btn-row">
            <button class="btn primary play">▶ 播放</button>
            <button class="btn pause">⏸ 暂停</button>
            <button class="btn step">⏭ 单步</button>
            <button class="btn reset">↺ 重置</button>
          </div>
          <div class="speed"><span>速度</span><input type="range" class="speed-range" min="1" max="10" value="9" /></div>
          <div class="progress"><div class="progress-fill prog"></div></div>
        </div>
        <div class="card legend">
          <div class="legend-item"><span class="sw" style="background:#4da3ff"></span> xⱼ</div>
          <div class="legend-item"><span class="sw line" style="background:var(--orange)"></span> 零线（μ=0）</div>
        </div>
      </aside>
      <main class="right">
        <div class="card chart"><div class="section-title">对数收益率 xⱼ（均值为 0 假设）</div><div class="chart-wrap" id="w1a"><canvas id="c1a"></canvas></div></div>
        <div class="card chart"><div class="section-title">xⱼ² 累加 → s² = (1/N)Σxⱼ²</div><div class="chart-wrap" id="w1b"><canvas id="c1b"></canvas></div></div>
      </main>
    </div>

    <!-- Scene 2: 2-2 / 2-3 -->
    <div class="scene" id="scene-2-2">
      <aside class="left">
        <div class="card">
          <div class="section-title">无偏修正 (2-2) 与直接公式 (2-3)</div>
          <div class="formula" id="f2">▶ 点击「播放」</div>
          <div class="stats">
            <div class="stat"><label>s²(÷N)</label><span id="s2pop">—</span></div>
            <div class="stat"><label>N/(N-1)</label><span id="s2fac">—</span></div>
            <div class="stat"><label>σ̂² (2-2)</label><span id="s2hat">—</span></div>
            <div class="stat"><label>s²(÷N-1)</label><span id="s2unb">—</span></div>
          </div>
        </div>
        <div class="card controls" data-ctrl="step">
          <div class="btn-row">
            <button class="btn primary play">▶ 播放</button>
            <button class="btn pause">⏸ 暂停</button>
            <button class="btn step">⏭ 单步</button>
            <button class="btn reset">↺ 重置</button>
          </div>
          <div class="speed"><span>速度</span><input type="range" class="speed-range" min="1" max="10" value="9" /></div>
          <div class="progress"><div class="progress-fill prog"></div></div>
        </div>
        <div class="card legend">
          <div class="legend-item"><span class="sw line" style="background:var(--red)"></span> 有偏 ÷N</div>
          <div class="legend-item"><span class="sw line" style="background:var(--green)"></span> 无偏 ÷N-1</div>
        </div>
      </aside>
      <main class="right">
        <div class="card chart"><div class="section-title">两种分母下的方差估计对比</div><div class="chart-wrap" id="w2a"><canvas id="c2a"></canvas></div></div>
        <div class="card chart"><div class="section-title">(xⱼ-x̄)² 累加过程</div><div class="chart-wrap" id="w2b"><canvas id="c2b"></canvas></div></div>
      </main>
    </div>

    <!-- Scene 3: Jensen -->
    <div class="scene" id="scene-jensen">
      <aside class="left">
        <div class="card">
          <div class="section-title">E(s) &lt; σ · 詹森不等式</div>
          <div class="formula" id="f3">▶ 点击「播放」：蒙特卡洛重复抽样</div>
          <div class="stats">
            <div class="stat"><label>真实 σ</label><span id="s3sig">—</span></div>
            <div class="stat"><label>样本量 n</label><span id="s3n">—</span></div>
            <div class="stat"><label>E(s) 估计</label><span id="s3es">—</span></div>
            <div class="stat"><label>低估幅度</label><span id="s3bias">—</span></div>
          </div>
        </div>
        <div class="card controls" data-ctrl="jensen">
          <div class="btn-row">
            <button class="btn primary play">▶ 播放</button>
            <button class="btn pause">⏸ 暂停</button>
            <button class="btn step">⏭ +500次</button>
            <button class="btn reset">↺ 重置</button>
          </div>
          <div class="speed"><span>速度</span><input type="range" class="speed-range" min="1" max="10" value="7" /></div>
          <div class="progress"><div class="progress-fill prog"></div></div>
        </div>
        <div class="card legend">
          <div class="legend-item"><span class="sw line" style="background:var(--green)"></span> 真实 σ</div>
          <div class="legend-item"><span class="sw line" style="background:var(--orange)"></span> E(s)</div>
        </div>
      </aside>
      <main class="right">
        <div class="card chart"><div class="section-title">√ 函数的凹性：E(√s²) &lt; √(E(s²))</div><div class="chart-wrap" id="w3a"><canvas id="c3a"></canvas></div></div>
        <div class="card chart"><div class="section-title">重复抽样得到的样本标准差 s 的分布</div><div class="chart-wrap" id="w3b"><canvas id="c3b"></canvas></div></div>
      </main>
    </div>

    <!-- Scene 4: 2-4 PDF -->
    <div class="scene" id="scene-2-4">
      <aside class="left">
        <div class="card">
          <div class="section-title">正态假设下 f_N(s) · 公式 (2-4)</div>
          <div class="formula" id="f4">▶ 点击「播放」：观察 N 增大时 PDF 形态</div>
          <div class="stats">
            <div class="stat"><label>样本量 N</label><span id="s4N">—</span></div>
            <div class="stat"><label>总体 σ</label><span id="s4sig">—</span></div>
            <div class="stat"><label>PDF 峰值 s*</label><span id="s4peak">—</span></div>
            <div class="stat"><label>峰值→σ</label><span id="s4note">—</span></div>
          </div>
        </div>
        <div class="card controls" data-ctrl="pdf">
          <div class="btn-row">
            <button class="btn primary play">▶ 播放</button>
            <button class="btn pause">⏸ 暂停</button>
            <button class="btn step">⏭ N+1</button>
            <button class="btn reset">↺ 重置</button>
          </div>
          <div class="speed"><span>速度</span><input type="range" class="speed-range" min="1" max="10" value="6" /></div>
          <div class="progress"><div class="progress-fill prog"></div></div>
          <div class="speed" style="margin-top:8px"><span>N</span><input type="range" id="nSlider" min="3" max="120" value="3" /></div>
        </div>
        <div class="card legend">
          <div class="legend-item"><span class="sw line" style="background:var(--accent)"></span> f_N(s)</div>
          <div class="legend-item"><span class="sw line" style="background:var(--green)"></span> σ</div>
        </div>
      </aside>
      <main class="right single">
        <div class="card chart"><div class="section-title">样本标准差 s 的概率密度 f_N(s)</div><div class="chart-wrap" id="w4"><canvas id="c4"></canvas></div></div>
      </main>
    </div>
  </div>

  <script>
    const LOG = [
{arr}
    ];
    const DATA_N = LOG.length;

    const META = {{
      '2-1b': {{ title: '(2-1b) 忽略均值的简化方差', eq: 's² = (1/N) · Σxⱼ²' }},
      '2-2': {{ title: '(2-2)(2-3) 总体方差无偏估计', eq: 'σ̂² = N/(N-1)·s²  ≡  Σ(xⱼ-x̄)²/(N-1)' }},
      'jensen': {{ title: '詹森不等式与波动率偏差', eq: 'E(s) = E(√s²) < √σ² = σ' }},
      '2-4': {{ title: '(2-4) 样本标准差分布', eq: 'f_N(s) · 正态假设' }},
    }};

    let activeScene = '2-1b';
    let frame = 0, playing = false, timer = null;

    // --- shared canvas helpers ---
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

    // --- Scene routing ---
    function switchScene(id) {{
      activeScene = id;
      document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.scene === id));
      document.querySelectorAll('.scene').forEach(s => s.classList.toggle('active', s.id === 'scene-' + id));
      document.getElementById('sceneTitle').textContent = META[id].title;
      document.getElementById('sceneEq').textContent = META[id].eq;
      pauseAll();
      resetActive();
      drawActive();
    }}
    document.querySelectorAll('.tab').forEach(t => t.addEventListener('click', () => switchScene(t.dataset.scene)));
    window.addEventListener('hashchange', applyHash);
    function applyHash() {{
      const h = (location.hash || '#2-1b').slice(1);
      if (META[h]) switchScene(h);
    }}

    // --- Step-through scenes (1 & 2) ---
    function zeroMeanStats(k) {{
      const slice = LOG.slice(0, k + 1);
      const n = slice.length;
      const sq = slice.map(x => x * x);
      const sumSq = sq.reduce((a, b) => a + b, 0);
      return {{ slice, sq, sumSq, var0: sumSq / n, n }};
    }}
    function devStats(k) {{
      const slice = LOG.slice(0, k + 1);
      const n = slice.length;
      const mean = slice.reduce((a, b) => a + b, 0) / n;
      const sq = slice.map(x => (x - mean) ** 2);
      const sumSq = sq.reduce((a, b) => a + b, 0);
      const pop = sumSq / n;
      const fac = n > 1 ? n / (n - 1) : NaN;
      const hat = n > 1 ? pop * fac : NaN;
      const unb = n > 1 ? sumSq / (n - 1) : NaN;
      return {{ slice, mean, sq, sumSq, pop, fac, hat, unb, n }};
    }}

    const c1a = document.getElementById('c1a'), c1b = document.getElementById('c1b');
    const c2a = document.getElementById('c2a'), c2b = document.getElementById('c2b');
    const c3a = document.getElementById('c3a'), c3b = document.getElementById('c3b');
    const c4 = document.getElementById('c4');

    function drawScene1(k) {{
      const {{ w: w1, h: h1, ctx }} = setupCanvas('w1a', c1a);
      const {{ w: w2, h: h2, ctx: ctx2 }} = setupCanvas('w1b', c1b);
      const p = pad();
      const {{ slice, sq, sumSq, var0, n }} = zeroMeanStats(k);
      const xj = LOG[k];

      ctx.clearRect(0, 0, w1, h1);
      drawGrid(ctx, w1, h1, p);
      const minV = Math.min(-0.04, ...slice) * 1.1;
      const maxV = Math.max(0.035, ...slice) * 1.1;
      const y = v => p.top + (1 - (v - minV) / (maxV - minV)) * (h1 - p.top - p.bottom);
      const y0 = y(0);
      ctx.strokeStyle = '#f5a623'; ctx.lineWidth = 1.8;
      ctx.beginPath(); ctx.moveTo(p.left, y0); ctx.lineTo(w1 - p.right, y0); ctx.stroke();
      ctx.fillStyle = '#f5a623'; ctx.font = '10px IBM Plex Sans,sans-serif';
      ctx.fillText('μ=0', p.left + 4, y0 - 6);
      ctx.strokeStyle = '#4da3ff'; ctx.lineWidth = 1.6; ctx.beginPath();
      for (let i = 0; i <= k; i++) {{
        const x = xPos(i, n, p, w1), yy = y(LOG[i]);
        i === 0 ? ctx.moveTo(x, yy) : ctx.lineTo(x, yy);
      }}
      ctx.stroke();
      const x = xPos(k, n, p, w1);
      ctx.fillStyle = '#4da3ff';
      ctx.beginPath(); ctx.arc(x, y(xj), 5, 0, Math.PI * 2); ctx.fill();

      ctx2.clearRect(0, 0, w2, h2);
      drawGrid(ctx2, w2, h2, p);
      const maxSq = Math.max(0.0008, ...sq) * 1.15;
      const y2 = v => p.top + (1 - v / maxSq) * (h2 - p.top - p.bottom);
      const yb = y2(0);
      const barW = Math.max(2, Math.min(10, (w2 - p.left - p.right) / n * 0.72));
      for (let i = 0; i <= k; i++) {{
        const xx = xPos(i, n, p, w2), yy = y2(sq[i]);
        ctx2.fillStyle = i === k ? '#4da3ff' : 'rgba(61,156,245,0.55)';
        ctx2.fillRect(xx - barW / 2, yy, barW, Math.max(1, yb - yy));
      }}

      document.getElementById('stepPill').textContent = `第 ${{n}} / ${{DATA_N}} 个样本`;
      document.getElementById('s1xj').textContent = `${{(xj * 100).toFixed(2)}}%`;
      document.getElementById('s1sq').textContent = sq[k].toExponential(3);
      document.getElementById('s1sum').textContent = sumSq.toExponential(3);
      document.getElementById('s1var').textContent = var0.toExponential(3);
      document.getElementById('f1').innerHTML =
        `j = <span class="hl">${{n}}</span>\\n` +
        `xⱼ² = (${{xj.toFixed(4)}})² = ${{sq[k].toExponential(3)}}\\n` +
        `Σxⱼ² = ${{sumSq.toExponential(3)}}\\n` +
        `<span class="result">s² = ${{sumSq.toExponential(3)}} / ${{n}} = ${{var0.toExponential(3)}}</span>`;
      setProg(document.querySelector('#scene-2-1b .prog'), n / DATA_N);
    }}

    function drawScene2(k) {{
      const {{ w: w1, h: h1, ctx }} = setupCanvas('w2a', c2a);
      const {{ w: w2, h: h2, ctx: ctx2 }} = setupCanvas('w2b', c2b);
      const p = pad();
      const st = devStats(k);
      const {{ sq, sumSq, pop, fac, hat, unb, n, mean }} = st;
      const atEnd = k >= DATA_N - 1;
      const RUN_WINDOW = 42;

      ctx.clearRect(0, 0, w1, h1);
      drawGrid(ctx, w1, h1, p);
      if (n >= 2) {{
        const iEnd = k;
        const iStart = atEnd ? 1 : Math.max(1, k - RUN_WINDOW + 1);
        const vals = [];
        for (let i = iStart; i <= iEnd; i++) vals.push(devStats(i).pop, devStats(i).unb);
        let minV, maxV;
        if (atEnd) {{
          for (let i = 1; i <= k; i++) vals.push(devStats(i).pop, devStats(i).unb);
          minV = Math.min(...vals) * 0.85;
          maxV = Math.max(...vals) * 1.15;
        }} else {{
          const curPop = devStats(k).pop;
          const curUnb = devStats(k).unb;
          const gap = Math.max(curUnb - curPop, curPop * 0.02);
          const mid = (curPop + curUnb) / 2;
          minV = Math.min(...vals, mid - gap * 3);
          maxV = Math.max(...vals, mid + gap * 3);
          const margin = (maxV - minV) * 0.18 || gap;
          minV -= margin;
          maxV += margin;
        }}
        const y = v => p.top + (1 - (v - minV) / (maxV - minV)) * (h1 - p.top - p.bottom);
        const xFor = i => atEnd
          ? xPos(i - 1, DATA_N, p, w1)
          : p.left + ((i - iStart) / Math.max(1, iEnd - iStart)) * (w1 - p.left - p.right);

        ctx.strokeStyle = '#f07178'; ctx.lineWidth = 2; ctx.beginPath();
        for (let i = iStart; i <= iEnd; i++) {{
          const x = xFor(i), yy = y(devStats(i).pop);
          i === iStart ? ctx.moveTo(x, yy) : ctx.lineTo(x, yy);
        }}
        ctx.stroke();
        ctx.strokeStyle = '#2dd4a8'; ctx.lineWidth = 2; ctx.beginPath();
        for (let i = iStart; i <= iEnd; i++) {{
          const x = xFor(i), yy = y(devStats(i).unb);
          i === iStart ? ctx.moveTo(x, yy) : ctx.lineTo(x, yy);
        }}
        ctx.stroke();

        if (!atEnd) {{
          const xCur = xFor(k);
          const yPop = y(pop), yUnb = y(unb);
          ctx.fillStyle = '#f07178';
          ctx.beginPath(); ctx.arc(xCur, yPop, 5, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#2dd4a8';
          ctx.beginPath(); ctx.arc(xCur, yUnb, 5, 0, Math.PI * 2); ctx.fill();
          ctx.strokeStyle = 'rgba(139,149,168,0.45)'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(xCur, yPop); ctx.lineTo(xCur, yUnb); ctx.stroke();
        }}

        ctx.fillStyle = '#8b95a8'; ctx.font = '10px IBM Plex Sans,sans-serif';
        ctx.fillText(
          atEnd ? '全貌：N 增大后 ÷N 与 ÷N-1 两线趋同' : `跟随前沿 N=${{n}} · 红=÷N  绿=÷N-1`,
          p.left + 2, p.top + 12
        );
      }}

      ctx2.clearRect(0, 0, w2, h2);
      drawGrid(ctx2, w2, h2, p);
      const maxSq = Math.max(0.0015, ...sq) * 1.1;
      const y2 = v => p.top + (1 - v / maxSq) * (h2 - p.top - p.bottom);
      const yb = y2(0);
      const barW = Math.max(2, Math.min(10, (w2 - p.left - p.right) / n * 0.72));
      for (let i = 0; i <= k; i++) {{
        const xx = xPos(i, n, p, w2), yy = y2(sq[i]);
        ctx2.fillStyle = i === k ? '#4da3ff' : 'rgba(61,156,245,0.55)';
        ctx2.fillRect(xx - barW / 2, yy, barW, Math.max(1, yb - yy));
      }}

      document.getElementById('stepPill').textContent = `第 ${{n}} / ${{DATA_N}} 个样本`;
      document.getElementById('s2pop').textContent = n >= 1 ? pop.toExponential(3) : '—';
      document.getElementById('s2fac').textContent = n >= 2 ? fac.toFixed(4) : '—';
      document.getElementById('s2hat').textContent = n >= 2 ? hat.toExponential(3) : '—';
      document.getElementById('s2unb').textContent = n >= 2 ? unb.toExponential(3) : '—';
      const eq = n >= 2
        ? `<span class="result">σ̂² = (${{n}}/${{n-1}})×${{pop.toExponential(3)}} = ${{hat.toExponential(3)}}</span>\\n` +
          `<span class="result">s² = ${{sumSq.toExponential(3)}}/(${{n}}-1) = ${{unb.toExponential(3)}}</span>\\n` +
          `<span class="hl">两式相等 ✓</span>`
        : `<span class="hl">至少需要 2 个样本</span>`;
      document.getElementById('f2').innerHTML =
        `N=${{n}},  Σ(xⱼ-x̄)²=${{sumSq.toExponential(3)}}\\n` +
        `有偏: s²=${{sumSq.toExponential(3)}}/${{n}}=${{pop.toExponential(3)}}\\n` + eq;
      setProg(document.querySelector('#scene-2-2 .prog'), n / DATA_N);
    }}

    // --- Scene 3: Jensen Monte Carlo ---
    const SIG_TRUE = 0.015;
    const JENSEN_N = 30;
    let jensenSamples = [];
    let jensenTarget = 8000;

    function randn() {{
      let u = 0, v = 0;
      while (u === 0) u = Math.random();
      while (v === 0) v = Math.random();
      return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    }}
    function sampleStd(arr) {{
      const n = arr.length;
      const m = arr.reduce((a, b) => a + b, 0) / n;
      const ss = arr.reduce((a, x) => a + (x - m) ** 2, 0);
      return Math.sqrt(ss / (n - 1));
    }}
    function addJensenBatch(batch) {{
      for (let b = 0; b < batch; b++) {{
        const draw = Array.from({{ length: JENSEN_N }}, () => randn() * SIG_TRUE);
        jensenSamples.push(sampleStd(draw));
      }}
    }}

    function drawScene3() {{
      const {{ w: w1, h: h1, ctx }} = setupCanvas('w3a', c3a);
      const {{ w: w2, h: h2, ctx: ctx2 }} = setupCanvas('w3b', c3b);
      const p = pad();

      ctx.clearRect(0, 0, w1, h1);
      drawGrid(ctx, w1, h1, p);
      const xMin = 0, xMax = 0.0012;
      const yMin = 0, yMax = 0.038;
      const tx = v => p.left + (v - xMin) / (xMax - xMin) * (w1 - p.left - p.right);
      const ty = v => p.top + (1 - (v - yMin) / (yMax - yMin)) * (h1 - p.top - p.bottom);
      ctx.strokeStyle = '#3d9cf5'; ctx.lineWidth = 2; ctx.beginPath();
      for (let i = 0; i <= 200; i++) {{
        const v = xMin + (xMax - xMin) * i / 200;
        const yy = Math.sqrt(v);
        const x = tx(v), y = ty(yy);
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }}
      ctx.stroke();
      if (jensenSamples.length > 0) {{
        const last = jensenSamples[jensenSamples.length - 1];
        const v2 = last * last;
        ctx.fillStyle = '#4da3ff';
        ctx.beginPath(); ctx.arc(tx(v2), ty(last), 4, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = 'rgba(245,166,35,0.6)'; ctx.setLineDash([4, 4]);
        ctx.beginPath(); ctx.moveTo(tx(v2), ty(Math.sqrt(v2))); ctx.lineTo(tx(v2), ty(Math.sqrt(xMax)));
        ctx.stroke(); ctx.setLineDash([]);
      }}
      ctx.fillStyle = '#8b95a8'; ctx.font = '10px IBM Plex Sans,sans-serif';
      ctx.fillText('y=√x（凹函数）', p.left + 4, p.top + 14);

      ctx2.clearRect(0, 0, w2, h2);
      drawGrid(ctx2, w2, h2, p);
      const m = jensenSamples.length;
      if (m > 0) {{
        const bins = 40;
        const lo = 0.005, hi = 0.025;
        const hist = new Array(bins).fill(0);
        jensenSamples.forEach(s => {{
          const b = Math.min(bins - 1, Math.max(0, Math.floor((s - lo) / (hi - lo) * bins)));
          hist[b]++;
        }});
        const maxC = Math.max(...hist);
        const bw = (w2 - p.left - p.right) / bins;
        hist.forEach((c, i) => {{
          const bh = (c / maxC) * (h2 - p.top - p.bottom) * 0.9;
          ctx2.fillStyle = 'rgba(61,156,245,0.65)';
          ctx2.fillRect(p.left + i * bw, h2 - p.bottom - bh, bw - 1, bh);
        }});
        const meanS = jensenSamples.reduce((a, b) => a + b, 0) / m;
        const xSig = p.left + (SIG_TRUE - lo) / (hi - lo) * (w2 - p.left - p.right);
        const xEs = p.left + (meanS - lo) / (hi - lo) * (w2 - p.left - p.right);
        ctx2.strokeStyle = '#2dd4a8'; ctx2.lineWidth = 2;
        ctx2.beginPath(); ctx2.moveTo(xSig, p.top); ctx2.lineTo(xSig, h2 - p.bottom); ctx2.stroke();
        ctx2.strokeStyle = '#f5a623'; ctx2.beginPath(); ctx2.moveTo(xEs, p.top); ctx2.lineTo(xEs, h2 - p.bottom); ctx2.stroke();
        document.getElementById('s3es').textContent = `${{(meanS * 100).toFixed(3)}}%`;
        document.getElementById('s3bias').textContent = `${{((SIG_TRUE - meanS) * 100).toFixed(3)}}%`;
        document.getElementById('f3').innerHTML =
          `已模拟 <span class="hl">${{m}}</span> 次（每次 n=${{JENSEN_N}}）\\n` +
          `σ = ${{SIG_TRUE.toFixed(4)}}\\n` +
          `E(s) ≈ ${{(meanS * 100).toFixed(3)}}% < σ = ${{(SIG_TRUE * 100).toFixed(2)}}%\\n` +
          `<span class="result">E(√s²) < √E(s²) = σ</span>`;
      }}
      document.getElementById('stepPill').textContent = `${{jensenSamples.length}} / ${{jensenTarget}} 次模拟`;
      document.getElementById('s3sig').textContent = `${{(SIG_TRUE * 100).toFixed(2)}}%`;
      document.getElementById('s3n').textContent = String(JENSEN_N);
      setProg(document.querySelector('#scene-jensen .prog'), jensenSamples.length / jensenTarget);
    }}

    // --- Scene 4: PDF ---
    let pdfN = 3;
    const PDF_SIG = SIG_TRUE;
    const PDF_N_MAX = 120;

    function lnGamma(z) {{
      const g = 7;
      const c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
        771.32342877765313, -176.61502916214059, 12.507343278686905,
        -0.13857109526572012, 9.984369578019571e-6, 1.5056327351493116e-7];
      if (z < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * z)) - lnGamma(1 - z);
      z -= 1;
      let x = c[0];
      for (let i = 1; i < g + 2; i++) x += c[i] / (z + i);
      const t = z + g + 0.5;
      return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
    }}
    function pdfStd(s, N, sigma) {{
      if (s <= 0 || N < 2) return 0;
      const a = (N - 1) / 2;
      const logF = Math.log(2) - lnGamma(a) + a * Math.log(N / (2 * sigma * sigma))
        - (N * s * s) / (2 * sigma * sigma) + (N - 2) * Math.log(s);
      return Math.exp(logF);
    }}

    function drawScene4() {{
      const {{ w, h, ctx }} = setupCanvas('w4', c4);
      const p = pad();
      ctx.clearRect(0, 0, w, h);
      drawGrid(ctx, w, h, p);
      const N = pdfN;
      const lo = 0.002, hi = PDF_SIG * 2.2;
      const pts = [];
      let peak = 0, peakS = 0;
      for (let i = 0; i <= 300; i++) {{
        const s = lo + (hi - lo) * i / 300;
        const f = pdfStd(s, N, PDF_SIG);
        pts.push([s, f]);
        if (f > peak) {{ peak = f; peakS = s; }}
      }}
      const maxF = peak * 1.08;
      const tx = s => p.left + (s - lo) / (hi - lo) * (w - p.left - p.right);
      const ty = f => p.top + (1 - f / maxF) * (h - p.top - p.bottom);
      ctx.strokeStyle = '#3d9cf5'; ctx.lineWidth = 2.2; ctx.beginPath();
      pts.forEach(([s, f], i) => {{ i === 0 ? ctx.moveTo(tx(s), ty(f)) : ctx.lineTo(tx(s), ty(f)); }});
      ctx.stroke();
      const xSig = tx(PDF_SIG);
      ctx.strokeStyle = '#2dd4a8'; ctx.lineWidth = 2; ctx.setLineDash([5, 4]);
      ctx.beginPath(); ctx.moveTo(xSig, p.top); ctx.lineTo(xSig, h - p.bottom); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#8b95a8'; ctx.font = '10px IBM Plex Sans,sans-serif';
      ctx.fillText(`N=${{N}}`, p.left + 4, p.top + 14);
      ctx.fillText(`σ=${{(PDF_SIG * 100).toFixed(1)}}%`, xSig + 4, p.top + 14);

      document.getElementById('stepPill').textContent = `N = ${{N}}`;
      document.getElementById('s4N').textContent = String(N);
      document.getElementById('s4sig').textContent = `${{(PDF_SIG * 100).toFixed(2)}}%`;
      document.getElementById('s4peak').textContent = `${{(peakS * 100).toFixed(2)}}%`;
      document.getElementById('s4note').textContent = N >= 20 ? '趋近 σ' : '左偏';
      document.getElementById('nSlider').value = N;
      document.getElementById('f4').innerHTML =
        `f_${{N}}(s) = 2/Γ(${{((N-1)/2).toFixed(1)}}) · (N/2σ²)^(${{((N-1)/2).toFixed(1)}})\\n` +
        `· exp(-Ns²/2σ²) · s^${{N-2}}\\n` +
        `<span class="result">N 越大，分布越集中在 σ 附近</span>`;
      setProg(document.querySelector('#scene-2-4 .prog'), (N - 3) / (PDF_N_MAX - 3));
    }}

    function setProg(el, r) {{ if (el) el.style.width = `${{Math.min(100, r * 100)}}%`; }}

    function drawActive() {{
      if (activeScene === '2-1b') drawScene1(frame);
      else if (activeScene === '2-2') drawScene2(frame);
      else if (activeScene === 'jensen') drawScene3();
      else if (activeScene === '2-4') drawScene4();
    }}

    function pauseAll() {{ playing = false; clearTimeout(timer); document.querySelectorAll('.play').forEach(b => b.textContent = '▶ 播放'); }}
    function pause() {{ pauseAll(); }}

    function getSpeedMs(sceneEl) {{
      const v = Number(sceneEl.querySelector('.speed-range').value);
      return 1150 - v * 95;
    }}

    function resetActive() {{
      if (activeScene === '2-1b' || activeScene === '2-2') frame = 0;
      else if (activeScene === 'jensen') {{ jensenSamples = []; }}
      else if (activeScene === '2-4') {{ pdfN = 3; }}
    }}

    function stepActive() {{
      if (activeScene === '2-1b' || activeScene === '2-2') {{
        if (frame < DATA_N - 1) {{ frame++; drawActive(); }}
        else pause();
      }} else if (activeScene === 'jensen') {{
        addJensenBatch(500);
        drawActive();
        if (jensenSamples.length >= jensenTarget) pause();
      }} else if (activeScene === '2-4') {{
        if (pdfN < PDF_N_MAX) {{ pdfN++; drawActive(); }}
        else pause();
      }}
    }}

    function schedule() {{
      clearTimeout(timer);
      if (!playing) return;
      const sceneEl = document.getElementById('scene-' + activeScene);
      const ms = getSpeedMs(sceneEl);
      timer = setTimeout(() => {{
        if (activeScene === '2-1b' || activeScene === '2-2') {{
          if (frame < DATA_N - 1) {{ frame++; drawActive(); schedule(); }}
          else pause();
        }} else if (activeScene === 'jensen') {{
          addJensenBatch(200);
          drawActive();
          if (jensenSamples.length >= jensenTarget) pause();
          else schedule();
        }} else if (activeScene === '2-4') {{
          if (pdfN < PDF_N_MAX) {{ pdfN++; drawActive(); schedule(); }}
          else pause();
        }}
      }}, ms);
    }}

    function playActive() {{
      const sceneEl = document.getElementById('scene-' + activeScene);
      if (activeScene === '2-1b' || activeScene === '2-2') {{
        if (frame >= DATA_N - 1) {{ frame = 0; drawActive(); }}
      }} else if (activeScene === 'jensen') {{
        if (jensenSamples.length >= jensenTarget) {{ jensenSamples = []; drawActive(); }}
      }} else if (activeScene === '2-4') {{
        if (pdfN >= PDF_N_MAX) {{ pdfN = 3; drawActive(); }}
      }}
      playing = true;
      sceneEl.querySelector('.play').textContent = '▶ 播放中';
      schedule();
    }}

    document.querySelectorAll('.scene').forEach(scene => {{
      const ctrl = scene.querySelector('.controls');
      ctrl.querySelector('.play').addEventListener('click', () => {{
        if (document.getElementById('scene-' + activeScene) !== scene) return;
        playing ? pause() : playActive();
      }});
      ctrl.querySelector('.pause').addEventListener('click', () => {{
        if (document.getElementById('scene-' + activeScene) === scene) pause();
      }});
      ctrl.querySelector('.step').addEventListener('click', () => {{
        if (document.getElementById('scene-' + activeScene) === scene) {{ pause(); stepActive(); }}
      }});
      ctrl.querySelector('.reset').addEventListener('click', () => {{
        if (document.getElementById('scene-' + activeScene) === scene) {{ pause(); resetActive(); drawActive(); }}
      }});
      ctrl.querySelector('.speed-range').addEventListener('input', () => {{ if (playing) schedule(); }});
    }});

    document.getElementById('nSlider').addEventListener('input', e => {{
      pdfN = Number(e.target.value);
      pause();
      drawActive();
    }});

    window.addEventListener('resize', drawActive);
    applyHash();
    if (!location.hash) drawActive();
  </script>
</body>
</html>
"""

OUT.write_text(HTML, encoding="utf-8")
print(f"wrote {OUT} ({N} log returns)")
