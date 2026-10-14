import ast
px = ast.literal_eval(open('/tmp/claude-0/s124/mk/m03/scratch/px.txt').read().splitlines()[0])
rows = ",\n".join("[" + ",".join(str(v) for v in r) + "]" for r in px)
html = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=1100">
<title>Hours Without Order</title>
<style>
html,body{margin:0;background:#f4f1ea}
body{width:1100px;height:800px;overflow:hidden}
svg{display:block}
</style></head><body>
<svg id="w" width="1100" height="800" viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg"></svg>
<script>
// The whole of the material: the 40 x 12 greyscale pixels of record.jpg, row by row, top to bottom.
const PX = [
''' + rows + r'''
];
const W = 40, H = 12, N = 1464;
const X0 = 70, Y0 = 92, CW = 24, RH = 45;   // each source pixel becomes 24 x 45
const ns = "http://www.w3.org/2000/svg";
const svg = document.getElementById("w");
function el(t, a, p){ const e = document.createElementNS(ns, t); for (const k in a) e.setAttribute(k, a[k]); (p||svg).appendChild(e); return e; }

// 1. the picture itself, enlarged, as a faint ground
const g0 = el("g", {opacity: 0.16});
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
  const v = PX[y][x];
  el("rect", {x: X0 + x*CW, y: Y0 + y*RH, width: CW, height: RH, fill: `rgb(${v},${v},${v})`}, g0);
}

// 2. how many hours fall into each column: hour i lands in column floor(i*40/1464)
const count = new Array(W).fill(0);
for (let i = 0; i < N; i++) count[Math.floor(i*W/N)]++;

// 3. per column, read the ink as a vertical distribution and place that column's hours
//    at its quantiles. Their positions are kept roughly; their order in time is not.
const g1 = el("g", {fill: "#1d1b18"});
for (let x = 0; x < W; x++) {
  const ink = [];
  for (let y = 0; y < H; y++) ink.push(Math.max(0, 225 - PX[y][x]));
  const tot = ink.reduce((a,b)=>a+b, 0);
  const cum = [0]; for (let y = 0; y < H; y++) cum.push(cum[y] + ink[y]/tot);
  const n = count[x], cx = X0 + x*CW + CW/2;
  for (let k = 0; k < n; k++) {
    const q = (k + 0.5) / n;
    let y = 0; while (y < H-1 && cum[y+1] < q) y++;
    const f = (q - cum[y]) / Math.max(1e-9, cum[y+1] - cum[y]);
    el("circle", {cx: cx.toFixed(1), cy: (Y0 + (y + f)*RH).toFixed(1), r: 2.1}, g1);
  }
}

// 4. along the foot: the 1,464 hours in their true order, one hairline each,
//    bracketed into the columns that swallowed them.
const g2 = el("g", {stroke: "#1d1b18", "stroke-width": 0.32});
const FY = Y0 + H*RH + 30, span = W*CW;
for (let i = 0; i < N; i++) {
  const xx = X0 + (i + 0.5) * span / N;
  const tall = (i % 24 === 0) ? 14 : 7;
  el("line", {x1: xx.toFixed(2), x2: xx.toFixed(2), y1: FY, y2: FY + tall}, g2);
}
const g3 = el("g", {stroke: "#8a8478", "stroke-width": 0.8, fill: "none"});
for (let x = 0; x <= W; x++) {
  const xx = X0 + x*CW;
  el("line", {x1: xx, x2: xx, y1: FY - 8, y2: FY - 2}, g3);
}

const t = el("text", {x: X0, y: 762, fill: "#1d1b18", "font-family": "Georgia, 'Times New Roman', serif", "font-size": 19});
t.textContent = "Hours Without Order";
const s = el("text", {x: X0 + span, y: 762, fill: "#6d685f", "text-anchor": "end", "font-family": "Georgia, 'Times New Roman', serif", "font-size": 13, "font-style": "italic"});
s.textContent = "1,464 hours, 40 columns of 36 or 37; each column keeps where its hours were, not when";
</script>
</body></html>
'''
open('/tmp/claude-0/s124/mk/m03/work/index.html','w').write(html)
