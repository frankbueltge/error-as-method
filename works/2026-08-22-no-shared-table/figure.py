#!/usr/bin/env python3
"""figure.svg — three fields, and the one that decides the night is the empty one.

Drawn from results.json only; no value is typed in here by hand. Deterministic,
headless, no libraries. House palette kept; the form is a grid rather than the
tick rows of the previous night, because what is being shown is a relation
between parties and not a population.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))

PAPER, INK, MUTE, RULE = "#f7f4ee", "#2b2b2b", "#9a9488", "#e3ddd1"
FILL, SELF, ACCENT = "#cec7b8", "#b9b1a0", "#8c3a2b"
SERIF = "Iowan Old Style, Palatino, 'Palatino Linotype', Georgia, serif"
MONO = "'DejaVu Sans Mono', 'Courier New', monospace"

RT = ["python", "node", "ruby", "php", "perl"]
W, H = 1020, 768
o = []


def t(x, y, s, size=13, fill=INK, fam=None, anchor="start", weight=None):
    f = ' font-family="%s"' % fam if fam else ""
    a = ' text-anchor="%s"' % anchor if anchor != "start" else ""
    w = ' font-weight="%s"' % weight if weight else ""
    o.append('<text x="%s" y="%s" font-size="%s" fill="%s"%s%s%s>%s</text>'
             % (x, y, size, fill, f, a, w, s))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
         'viewBox="0 0 %d %d" font-family="%s">' % (W, H, W, H, SERIF))
o.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))

iop = R["interop"]
t(62, 52, "No shared table", 21)
t(62, 76, "Five runtimes with separate lineages are asked the same questions. Where they disagree,", 13, MUTE)
t(62, 94, "who could have seen the error alone &#8212; and what is left that needed both of them.", 13, MUTE)
t(62, 116, " &#183; ".join("%s %s" % (k, v) for k, v in R["runtimes"].items()), 12, MUTE, MONO)

# ---------------- field 1: the 5x5 grid ----------------
gx, gy, cw, ch = 150, 176, 96, 44
t(62, gy - 18, "1 &#8212; round-trip failures, of 512 doubles: rows render, columns parse", 13.5)
for j, parser in enumerate(RT):
    t(gx + j * cw + cw / 2, gy - 2, parser, 11.5, MUTE, MONO, "middle")
for i, producer in enumerate(RT):
    y = gy + i * ch
    t(gx - 12, y + ch / 2 + 4, producer, 11.5, MUTE, MONO, "end")
    for j, parser in enumerate(RT):
        x = gx + j * cw
        if i == j:
            n = iop["self_roundtrip_failures"][producer]["count"]
            diag = True
        else:
            n = iop["cross_pair_failures_by_pair"]["%s->%s" % (producer, parser)]
            diag = False
        # shade by share of the 512, so the eye reads the block, not the number
        share = n / 512.0
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" '
                 'fill-opacity="%.3f" stroke="%s" stroke-width="%s"/>'
                 % (x, y, cw - 4, ch - 4, FILL, 0.18 + 0.82 * share,
                    ACCENT if diag else RULE, "1.4" if diag else "1"))
        t(x + (cw - 4) / 2, y + ch / 2 + 4, str(n), 13,
          INK if share > 0.5 else MUTE, MONO, "middle")
t(gx + 5 * cw + 8, gy + 20, "outlined cells are the diagonal:", 11.5, MUTE)
t(gx + 5 * cw + 8, gy + 36, "a runtime parsing back its own", 11.5, MUTE)
t(gx + 5 * cw + 8, gy + 52, "default rendering. Everything a", 11.5, MUTE)
t(gx + 5 * cw + 8, gy + 68, "pair can show is already on it.", 11.5, MUTE)

# ---------------- field 2: the empty one ----------------
fy = gy + 5 * ch + 44
t(62, fy - 12, "2 &#8212; of the %s cross-pair failures, those invisible to BOTH parties alone"
  % f"{iop['cross_pair_failures']:,}", 13.5)
o.append('<rect x="62" y="%d" width="%d" height="70" fill="none" stroke="%s" '
         'stroke-width="1" stroke-dasharray="3 4"/>' % (fy, W - 124, RULE))
t(W / 2, fy + 44, str(iop["decisive_failures"]), 34, ACCENT, MONO, "middle")
t(W - 62, fy + 88, "%s ordered pairs &#215; %s doubles = %s cross cells examined"
  % (iop["ordered_pairs"], iop["seeds"], f"{iop['ordered_pairs'] * iop['seeds']:,}"),
  11.5, MUTE, MONO, "end")

# ---------------- field 3: the probe strip ----------------
py = fy + 132
t(62, py - 12, "3 &#8212; the 25 probes: filled where all five agree, open where they do not", 13.5)
rows = [("S", "one shared upstream file"), ("I", "no shared artefact")]
bw = 34
for k, (fam, caption) in enumerate(rows):
    y = py + k * 54
    probes = sorted((p for p in R["probes"] if p["family"] == fam),
                    key=lambda p: int(p["probe"][1:]))
    t(62, y + 20, fam, 15, INK, MONO)
    for idx, p in enumerate(probes):
        x = 92 + idx * (bw + 6)
        if p["unanimous"]:
            o.append('<rect x="%d" y="%d" width="%d" height="28" fill="%s" stroke="%s"/>'
                     % (x, y, bw, FILL, RULE))
        else:
            o.append('<rect x="%d" y="%d" width="%d" height="28" fill="none" stroke="%s" '
                     'stroke-width="1.4"/>' % (x, y, bw, ACCENT))
        t(x + bw / 2, y + 19, p["probe"], 10.5,
          INK if p["unanimous"] else ACCENT, MONO, "middle")
    fa = R["family_agreement"][fam]
    t(92 + len(probes) * (bw + 6) + 10, y + 19,
      "%d of %d unanimous &#8212; %s" % (fa["unanimous"], fa["probes"], caption), 12, MUTE)

t(62, H - 46, "The single open cell in row S is the lowercasing of a word-final sigma. Perl ships the "
              "Unicode file that states the rule", 11.5, MUTE)
t(62, H - 30, "(SpecialCasing.txt, byte-identical to the published 15.0.0 copy, sha256 %s&#8230;) and does "
              "not apply it." % R["shipped_rule"]["shipped_sha256"][:16], 11.5, MUTE)
t(62, H - 14, "Ulysses (the nightly line) &#183; Session 67 &#183; 2026-08-22 &#183; drawn from results.json",
  11, MUTE, MONO)

o.append("</svg>")
open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(o))
print("figure.svg written:", os.path.getsize(os.path.join(HERE, "figure.svg")), "bytes")
