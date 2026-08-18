#!/usr/bin/env python3
"""Draw the corpus on one axis: where the standard broke, and where each guarantee begins.

Deterministic — same results.json and adjudication.json, same bytes out. No randomness, no
network, stdlib only. The axis is the published order of Unicode versions, equally spaced,
because the question is which version a boundary sits at, not how many months apart they were.

Upper band: every corrigendum, drawn from the earliest version it declares defective to the
version that fixed it. Lower band: every applicability line, drawn as the half-open interval
its own notation means — Unicode N.n and all subsequent versions.

    python3 figure.py            # writes figure.svg
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

W, LEFT, RIGHT, TOP = 1180, 268, 40, 106
ROW = 21
BAND_GAP = 40

INK = "#17171a"
MUTED = "#8d8a85"
PAPER = "#f7f5f1"
BREACH = "#a3231b"
FIXED = "#b8763a"
COINC = "#9aa0a6"
RULE = "#d9d4cc"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def main():
    with open(os.path.join(HERE, "results.json"), encoding="utf-8") as fh:
        res = json.load(fh)
    with open(os.path.join(HERE, "adjudication.json"), encoding="utf-8") as fh:
        adj = json.load(fh)

    versions = [v["version"] for v in res["versions"]][::-1]      # oldest first
    years = {v["version"]: v["year"] for v in res["versions"]}
    n = len(versions)
    plot_w = W - LEFT - RIGHT
    step = plot_w / (n - 1)

    def x_of(version):
        """Position of a version string; accepts 2.0 or 2.0.0."""
        if version in versions:
            return LEFT + versions.index(version) * step
        for i, v in enumerate(versions):
            if v.startswith(version + "."):
                return LEFT + i * step
        return None

    corr = res["corrigenda"]
    verdicts = {v["clause"]: v for v in adj["verdicts"]}
    colour = {
        "minted_at_breach": BREACH,
        "boundary_at_a_fixed_defect": FIXED,
        "coincident_only": COINC,
        "undetermined": MUTED,
    }

    # ---- rows: policy clauses in the page's own order, one line per applicability
    lines = []
    for c in res["clauses"]:
        for i, ver in enumerate(c["applicable"]):
            name = c["clause"]
            if name == "Normalization Stability":
                name += " (strong form)" if ver == "4.1" else " (weaker form)"
            if name == "Alias Stability" and ver == "6.2":
                name = "Alias Reassignment"
            lines.append((name, ver))

    top_h = TOP + len(corr) * ROW
    bot_y = top_h + BAND_GAP + 26
    H = int(bot_y + len(lines) * ROW + 100)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="Iowan Old Style, Palatino, Georgia, serif">',
        f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
        f'<text x="12" y="30" font-size="17" fill="{INK}" font-weight="700">'
        f'The applicable version</text>',
        f'<text x="12" y="50" font-size="12.5" fill="{MUTED}">'
        f'Unicode&#8217;s published defects (above) and the first version from which each written '
        f'guarantee holds (below). 38 versions, 9 corrigenda, 16 applicability lines.</text>',
    ]

    # version gridlines + labels for the versions that carry something
    marked = {c["fixed_in"] for c in corr if c["fixed_in"]}
    marked |= {p for p in (x for _, x in lines)}
    labelled = set()
    for i, v in enumerate(versions):
        x = LEFT + i * step
        short = ".".join(v.split(".")[:2])
        important = v in marked or short in marked
        out.append(f'<line x1="{x:.1f}" y1="{TOP - 14}" x2="{x:.1f}" y2="{H - 62}" '
                   f'stroke="{RULE}" stroke-width="{1.1 if important else 0.5}"/>')
        # One label per boundary, at the first version carrying it: 1.1.0 and 1.1.5 are both
        # "1.1" on the policy page, and printing it twice was the first thing wrong with this
        # figure.
        if important and short not in labelled:
            labelled.add(short)
            out.append(f'<text x="{x:.1f}" y="{H - 44}" font-size="10" fill="{INK}" '
                       f'text-anchor="middle">{short}</text>')
            out.append(f'<text x="{x:.1f}" y="{H - 32}" font-size="8.5" fill="{MUTED}" '
                       f'text-anchor="middle">{years.get(v) or ""}</text>')

    # ---- upper band: the corrigenda
    out.append(f'<text x="12" y="{TOP - 16}" font-size="11" fill="{INK}" font-weight="700">'
               f'PUBLISHED DEFECTS</text>')
    for k, c in enumerate(corr):
        y = TOP + k * ROW
        pts = [p for p in c["defective_endpoints"] if x_of(p) is not None]
        x0 = min(x_of(p) for p in pts) if pts else x_of(c["fixed_in"])
        x1 = x_of(c["fixed_in"])
        is_norm = "Normalization" in c["title"] or "Canonical Mapping" in c["title"]
        col = FIXED if is_norm else MUTED
        out.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" '
                   f'stroke="{col}" stroke-width="2.4" stroke-linecap="butt"/>')
        out.append(f'<circle cx="{x1:.1f}" cy="{y:.1f}" r="3.4" fill="{col}"/>')
        label = c["title"].split(":", 1)[1].strip() if ":" in c["title"] else c["title"]
        label = label if len(label) < 44 else label[:41] + "…"
        out.append(f'<text x="{LEFT - 12}" y="{y + 3.6:.1f}" font-size="10.5" fill="{INK}" '
                   f'text-anchor="end">#{c["corrigendum"]} {esc(label)}</text>')

    # ---- lower band: the guarantees
    out.append(f'<text x="12" y="{bot_y - 16}" font-size="11" fill="{INK}" font-weight="700">'
               f'WRITTEN GUARANTEES</text>')
    for k, (name, ver) in enumerate(lines):
        y = bot_y + k * ROW
        x0 = x_of(ver)
        verdict = verdicts.get(name.split(" (")[0] if "(" not in name else name, {})
        if name.startswith("Normalization"):
            verdict = verdicts["Normalization Stability (strong form)" if ver == "4.1"
                               else "Normalization Stability (weaker form)"]
        col = colour.get(verdict.get("verdict", "undetermined"), MUTED)
        strong = verdict.get("verdict") in ("minted_at_breach", "boundary_at_a_fixed_defect")
        dash = "" if strong else ' stroke-dasharray="1.5 3"'
        out.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{W - RIGHT + 6:.1f}" y2="{y:.1f}" '
                   f'stroke="{col}" stroke-width="{2.4 if strong else 1.2}"{dash}/>')
        out.append(f'<circle cx="{x0:.1f}" cy="{y:.1f}" r="3.4" fill="{col}"/>')
        out.append(f'<text x="{LEFT - 12}" y="{y + 3.6:.1f}" font-size="10.5" '
                   f'fill="{INK if strong else MUTED}" text-anchor="end">{esc(name)}</text>')

    # the two vertical readings
    for ver, note in (("2.0", "characters last moved"), ("4.1", "normalization last broke")):
        x = x_of(ver)
        out.append(f'<line x1="{x:.1f}" y1="{TOP - 34}" x2="{x:.1f}" y2="{H - 56}" '
                   f'stroke="{BREACH}" stroke-width="0.9" stroke-dasharray="4 3"/>')
        out.append(f'<text x="{x + 5:.1f}" y="{TOP - 38}" font-size="10" fill="{BREACH}">'
                   f'{note}</text>')

    out.append(f'<text x="12" y="{H - 22}" font-size="9.5" fill="{MUTED}">'
               f'Sources: unicode.org/policies/stability_policy.html · '
               f'unicode.org/versions/corrigenda.html · unicode.org/versions/enumeratedversions.html, '
               f'all retrieved 2026-08-18.</text>')
    out.append(f'<text x="12" y="{H - 9}" font-size="9.5" fill="{MUTED}">'
               f'Solid: a defect is documented before the boundary. Dotted: undetermined, or a '
               f'coincidence rejected in adjudication.json. Versions equally spaced by publication '
               f'order, not by time.</text>')
    out.append("</svg>")

    with open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"figure.svg — {len(corr)} corrigenda, {len(lines)} guarantees, {n} versions, {H}px tall")


if __name__ == "__main__":
    main()
