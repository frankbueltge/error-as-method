"""figure.svg from results.json and posthoc.json (Session 179)."""
import json
r = json.load(open("results.json")); h = json.load(open("posthoc.json")); b = json.load(open("baseline.json"))
W, H = 760, 430
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, serif" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="#f7f5f0"/>',
     '<text x="20" y="30" font-size="17" fill="#1d1c1a">Already Made: what the measure said, what the reading saw</text>']
# left: materials
o.append('<text x="20" y="62" fill="#6b6760">Data sources chosen (makers of 8, first round)</text>')
mats = list(r["P3"]["makers_per_source"].items())[:5]
for i, (m, n) in enumerate(mats):
    y = 82 + i * 26
    o.append(f'<text x="20" y="{y+12}" fill="#1d1c1a">{m}</text>')
    o.append(f'<rect x="190" y="{y}" width="{n*22}" height="15" fill="#c4501b"/><text x="{196+n*22}" y="{y+12}" fill="#1d1c1a">{n}</text>')
# right: nearness
o.append('<text x="400" y="62" fill="#6b6760">Median similarity to the nearest atlas work</text>')
rows = [("atlas works to one another", b["loo_nn_median"], "#9c968a"), ("first proposals", r["P1"]["r1_nn_median"], "#c4501b"),
        ("revised (shown works removed)", r["P4"]["r2_nn_median_excluding_shown"], "#1f5fa8")]
for i, (t, v, c) in enumerate(rows):
    y = 82 + i * 26
    o.append(f'<text x="400" y="{y+12}" fill="#1d1c1a">{t}</text>')
    o.append(f'<rect x="610" y="{y}" width="{v*160-60:.0f}" height="15" fill="{c}"/><text x="{616+v*160-60:.0f}" y="{y+12}" fill="#1d1c1a">{v:.2f}</text>')
o.append('<text x="400" y="176" fill="#6b6760" font-size="11">bars start at 0.375; the measure reads the makers as far from the shelf</text>')
# bottom: theme
o.append('<text x="20" y="250" fill="#6b6760">Share whose move is about a record\'s errors, gaps, revisions, flags or withdrawals (word test)</text>')
th = [("706 works people made", h["theme_rate_atlas"], "#9c968a"), ("24 first proposals", h["theme_rate_r1"], "#c4501b"),
      ("24 revised, after being shown the world", h["theme_rate_r2"], "#1f5fa8")]
for i, (t, v, c) in enumerate(th):
    y = 270 + i * 34
    o.append(f'<text x="20" y="{y+14}" fill="#1d1c1a">{t}</text>')
    o.append(f'<rect x="290" y="{y}" width="{v*400:.0f}" height="20" fill="{c}"/><text x="{296+v*400:.0f}" y="{y+15}" fill="#1d1c1a">{v*100:.0f} %</text>')
o.append('<text x="20" y="400" fill="#6b6760" font-size="11">Every maker\'s context carried the practice\'s name, error-as-method. The theme cannot be told apart from that name tonight.</text>')
o.append('<text x="20" y="418" fill="#6b6760" font-size="11">Atlas: frankbueltge.de/atlas/werke.json, snapshot 2026-11-17. Measure: bge-small-en-v1.5 cosine on the decisive-move sentence.</text>')
o.append('</svg>')
open("figure.svg", "w").write("\n".join(o))
