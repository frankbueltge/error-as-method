"""Writes figure.svg: where the choosing went. Read from results.json."""
import json, html
r = json.load(open("results.json"))
col = {"M": "#2f6b5a", "R": "#8a2b0e", "H": "#b5651d", "L": "#8a8274", "E": "#555"}
W, rows = 900, []
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 420" font-family="Georgia,serif" font-size="14">',
     f'<rect width="{W}" height="420" fill="#f4f1ea"/>',
     '<text x="20" y="34" font-size="18" fill="#1d1b18">The Draw: one choice taken away, and where the choosing went</text>',
     '<g fill="#1d1b18"><text x="20" y="80" text-decoration="line-through">choosing the material</text>',
     '<text x="20" y="100" font-size="12" fill="#8a8274">replaced by a draw from the commit hash</text></g>']
leaks = [("the urn: one catalogue, chosen", "R"), ("rule (b): what counts as a domain", "R"), ("the parser: 329 datasets walked past (F-172)", "E")]
for i, (t, k) in enumerate(leaks):
    y = 150 + i * 34
    o.append(f'<rect x="20" y="{y-16}" width="14" height="20" fill="{col[k]}"/><text x="44" y="{y}" fill="#1d1b18">{html.escape(t)}</text>')
o.append('<text x="20" y="128" font-size="12" fill="#8a8274">before the data: three leaks</text>')
o.append('<text x="470" y="80" font-size="12" fill="#8a8274">inside the data: five selections, as tagged at the time</text>')
for i, c in enumerate([c for c in r["changes"] if c["select"]]):
    y = 110 + i * 52
    txt = c["text"].split(" — ")[0].split(" (")[0].replace("`", "")
    txt = txt if len(txt) < 58 else txt[:56] + "…"
    o.append(f'<rect x="470" y="{y-16}" width="22" height="22" fill="{col[c["source"]]}"/><text x="481" y="{y}" fill="#fff" font-family="Courier New,monospace" text-anchor="middle">{c["source"]}</text>')
    o.append(f'<text x="502" y="{y}" fill="#1d1b18">{html.escape(txt)}</text><text x="502" y="{y+18}" font-size="12" fill="#8a8274">for iteration {c["for"]}</text>')
o.append('<path d="M250 86 C 360 86, 380 100, 460 104" stroke="#8a8274" fill="none"/>')
s = r["selections_by_source"]
o.append(f'<text x="20" y="300" fill="#1d1b18">{s["R"] + s["H"]} of {r["selections"]} selections steered by what the practice already held</text>')
o.append(f'<text x="20" y="322" fill="#1d1b18">({s["R"]} its expectation or rule, {s["H"]} its habit), {s["M"]} by what it met.</text>')
o.append('<g font-size="12" fill="#8a8274"><text x="20" y="390">M material · R expectation, rule, line · H house habit · E my error</text>'
         '<text x="20" y="408">Material: Destatis 45211-0013 (Data licence by-2-0). Session 107.</text></g></svg>')
open("figure.svg", "w").write("\n".join(o)); print("figure.svg")
