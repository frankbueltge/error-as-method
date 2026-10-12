p='/tmp/claude-0/s122/mk/m10/scratch/template.html'
t=open(p).read()
rep=[
("const HW = /*HW*/;","const HW = /*HW*/;\nconst ENV = [/*ENV*/];  // fitted semidiurnal amplitude per row (M2+S2+N2), for the spring/neap marks"),
("const X0 = 96, X1 = 940, TOP = 186, BOT = 742;","const X0 = 96, X1 = 940, TOP = 200, BOT = 716;"),
("const sc = 1.55;","const sc = 2.0;"),
("""[0.25, 0.75].forEach(f => { const x = X0 + f * (X1 - X0); g.strokeStyle = FAINT; g.beginPath(); g.moveTo(x, TOP - 46); g.lineTo(x, BOT + 26); g.stroke(); });""",
 """[0.25, 0.5, 0.75].forEach(f => { const x = X0 + f * (X1 - X0); g.strokeStyle = SOFT; g.beginPath(); g.moveTo(x, BOT + 30); g.lineTo(x, BOT + 40); g.stroke(); });"""),
("g.fillText('high water', X0 + 0.25 * (X1 - X0), BOT + 38);","g.fillText('high water', X0 + 0.25 * (X1 - X0), BOT + 52);"),
("g.fillText('high water', X0 + 0.75 * (X1 - X0), BOT + 38);","g.fillText('high water', X0 + 0.75 * (X1 - X0), BOT + 52);"),
("g.fillText('low', X0 + 0.5 * (X1 - X0), BOT + 38);","g.fillText('low water', X0 + 0.5 * (X1 - X0), BOT + 52);"),
]
for a,b in rep:
  assert a in t, a[:40]; t=t.replace(a,b)
s=t.index("// spring / neap"); e=t.index("// labels for the guides")
t=t[:s]+"""// spring / neap: extremes of the fitted semidiurnal amplitude
g.textAlign = 'left';
for (let r = 1; r < ROWS - 1; r++) {
  const isMax = ENV[r] > ENV[r - 1] && ENV[r] >= ENV[r + 1], isMin = ENV[r] < ENV[r - 1] && ENV[r] <= ENV[r + 1];
  if (!isMax && !isMin) continue;
  const y = TOP + r * gap;
  g.strokeStyle = SOFT; g.lineWidth = 1; g.beginPath(); g.moveTo(X1 + 12, y); g.lineTo(X1 + 24, y); g.stroke();
  g.fillStyle = SOFT; g.font = 'italic 12px ' + SERIF;
  g.fillText(isMax ? 'springs' : 'neaps', X1 + 30, y);
}

"""+t[e:]
s=t.index("// row ranges"); e=t.index("// ---- the ridges")
t=t[:s]+t[e:]
s=t.index("// the event"); e=t.index("// ---- title block")
t=t[:s]+"""// the event
{
  const r = Math.floor((peak - t0) / L), x = xOf(peak), y = TOP + r * gap - (V[peak] - mean) * sc;
  const lx = x + 70, ly = y - 34;
  g.font = 'italic 13px ' + SERIF;
  const l1 = 'hour ' + (peak + 1).toLocaleString('en') + ' of 1,464: a single high water', l2 = 'standing far above every other';
  const w = Math.max(g.measureText(l1).width, g.measureText(l2).width);
  g.fillStyle = PAPER; g.globalAlpha = 0.92; g.fillRect(lx - 6, ly - 12, w + 12, 38); g.globalAlpha = 1;
  g.strokeStyle = RUST; g.lineWidth = 0.8; g.beginPath(); g.moveTo(x + 5, y - 3); g.lineTo(lx - 8, ly + 6); g.stroke();
  g.fillStyle = RUST; g.textAlign = 'left'; g.textBaseline = 'middle';
  g.fillText(l1, lx, ly); g.fillText(l2, lx, ly + 17);
}

"""+t[e:]
open(p,'w').write(t)
