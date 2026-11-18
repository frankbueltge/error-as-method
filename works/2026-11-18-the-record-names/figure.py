"""figure.svg: what the record could check in round 1, and what became of it in round 2. Reads results.json."""
import json, pathlib
H = pathlib.Path(__file__).parent
r = json.loads((H / "results.json").read_text())
p, m = r["P2"]["R+"], r["P2"]["R-"]
n = r["counts"]["claims_r1"]; z = n - p - m
k, zk = r["P4"]["kept"], r["P4"]["of"]
W, X0, BW = 760, 20, 720
def bar(y, parts, total):
    out, x = [], X0
    for v, col in parts:
        w = BW * v / total
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="34" fill="{col}"/>')
        x += w
    return "".join(out)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 300" font-family="Helvetica, Arial, sans-serif" font-size="14">
<rect width="{W}" height="300" fill="#f4f1ea"/>
<text x="{X0}" y="28" font-size="16" fill="#1d1b18">24 wall labels written from a photograph alone: {n} claims, held against the museum's record</text>
{bar(44, [(p, "#2f7d4f"), (m, "#b3261e"), (z, "#8a8478")], n)}
<text x="{X0}" y="98" fill="#1d1b18">{p} confirmed · {m} contradicted · {z} the record cannot check</text>
<text x="{X0}" y="150" font-size="16" fill="#1d1b18">Sent the record: all {m} contradicted claims corrected. Of the {zk} the makers brought from their own knowledge:</text>
{bar(166, [(k, "#1d1b18"), (zk - k, "#d9d3c5")], zk)}
<text x="{X0}" y="220" fill="#1d1b18">{k} kept beside the record · {zk - k} dropped · the revised labels carry {r["P5"]["round2_KNOWN_tagged"]} claims of the makers' own</text>
<text x="{X0}" y="262" font-size="12" fill="#6b665c">The Met Open Access (CC0), twelve objects, two makers each; coding by the conductor, rules committed first (predictions.md).</text>
</svg>'''
(H / "figure.svg").write_text(svg)
