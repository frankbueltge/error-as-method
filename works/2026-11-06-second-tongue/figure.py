"""figure.svg: five panels, the learners' value across, each arm's account (median of six) up; rho in each title."""
import json
from pathlib import Path
HERE = Path(__file__).parent
P = json.loads((HERE / "people.json").read_text()); R = json.loads((HERE / "results.json").read_text())
names = {"A": "the machine, for itself", "D": "told who they are", "B": "told 24 true values", "S": "told them at random",
         "R": "told them reversed"}
W, H, pw, ph, m = 980, 300, 170, 170, 28
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Menlo,Consolas,monospace" font-size="11">',
     f'<rect width="{W}" height="{H}" fill="#fafbf8"/>',
     '<text x="16" y="22" font-size="13" fill="#1b1f1d">A Second Tongue: 48 English words, Spanish-speaking learners\' familiarity (across) against each machine account (up), 1-7</text>']
for i, a in enumerate("ADBSR"):
    x0, y0 = 30 + i * (pw + 25), 70
    sx = lambda v: x0 + (v - 2) / 5 * pw
    sy = lambda v: y0 + ph - (v - 2) / 5 * ph
    o.append(f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="none" stroke="#cdd3cc"/>')
    o.append(f'<line x1="{sx(2)}" y1="{sy(2)}" x2="{sx(7)}" y2="{sy(7)}" stroke="#cdd3cc" stroke-dasharray="3 4"/>')
    o.append(f'<text x="{x0}" y="{y0-22}" fill="#1b1f1d">{a}: {names[a]}</text>')
    nm = R["noticed_mine"].get(a)
    o.append(f'<text x="{x0}" y="{y0-8}" fill="#5f6862">rho {R["arms"][a]["rho_l2"]:+.2f}' + (f' | named misfit {nm}/6' if nm is not None else '') + '</text>')
    for k, v in R["accounts"][a].items():
        c = "#9a4a1f" if P[k]["tail"].startswith("L2 below") else "#2a5d8a"
        o.append(f'<circle cx="{sx(P[k]["l2"]):.1f}" cy="{sy(v):.1f}" r="3" fill="{c}" fill-opacity=".8"/>')
    o.append(f'<text x="{x0}" y="{y0+ph+16}" fill="#5f6862">2</text><text x="{x0+pw-6}" y="{y0+ph+16}" fill="#5f6862">7</text>')
o.append(f'<text x="16" y="{H-14}" fill="#5f6862">rust: words learners find less familiar than native readers do; blue: more. Sources: osf.io/rnbs5; Scott et al. 2019 (Glasgow Norms). Dashed: perfect agreement.</text></svg>')
(HERE / "figure.svg").write_text("\n".join(o))
