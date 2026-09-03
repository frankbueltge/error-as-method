#!/usr/bin/env python3
"""Session 78 -- builds figure.svg and index.html from the committed measurements.

Deterministic: no randomness anywhere, so no seed. Same inputs, same bytes.

    python3 page.py results.json adjudication.json ../2026-09-01-.../results.json

figure.svg is the complete figure and says everything the argument needs without
a line of script. index.html is the same two listings made operable: the reader
can pick a code and see which of this publisher's two listings hold it, what
each says about it, and whether the machine can set it -- which is the act the
work is about and which a static picture can only assert.
"""

import html
import json
import sys

INK = "#1a1a1a"
PAPER = "#faf8f5"
FAINT = "#cfc9c0"
MID = "#8c8578"
MARK = "#a8322d"        # in the ecpg listing and not in the appendix
CONFLICT = "#b8860b"    # classified differently by the two listings
GHOST = "#6b7f6b"       # published and not in the machine

CELL, GAP, PER_ROW = 13, 3, 26
STEP = CELL + GAP


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def build_model(R, ADJ, S77):
    voc_rows = R["vocabulary"]["rows"]
    by_code = {}
    for r in voc_rows:
        by_code.setdefault(r["sqlstate"], []).append(r)

    # Session 77's per-row site counts, aggregated to the code
    sites, files = {}, {}
    for r in S77["rows"]:
        sites[r["sqlstate"]] = sites.get(r["sqlstate"], 0) + r["sites_b"]
        files.setdefault(r["sqlstate"], set()).update(r["files"])

    entries = R["ecpg_face"]["entries"]
    ecpg_of = {}
    for e in entries:
        codes = list(e["codes"])
        if "07001" in codes and " or 07002" in e["text"]:
            codes.append("07002")          # the hand-correction, marked as one
        for c in codes:
            ecpg_of.setdefault(c, []).append(
                {"term": e["term"], "line": e["line"], "text": e["text"][:220]})

    conflict = {c["sqlstate"] for c in ADJ["predictions"]["P4"]["conflicts"]}
    ghost = set(ADJ["predictions"]["P6"]["members_after_hand_check"])

    codes = []
    for code in sorted(by_code):
        rows = by_code[code]
        codes.append({
            "code": code,
            "klass": code[:2],
            "severity": sorted({r["severity"] for r in rows}),
            "condition": next((r["condition"] for r in rows if r["condition"]), None),
            "macros": [r["macro"] for r in rows],
            "two_rows": len(rows) > 1,
            "in_appendix": True,
            "in_ecpg": code in ecpg_of,
            "ecpg": ecpg_of.get(code, []),
            "sites": sites.get(code, 0),
            "n_files": len(files.get(code, ())),
            "conflict": code in conflict,
            "ghost": code in ghost,
        })

    ecpg_only = []
    for code in sorted(set(ecpg_of) - set(by_code)):
        ecpg_only.append({
            "code": code,
            "klass": code[:2],
            "in_appendix": False,
            "in_ecpg": True,
            "ecpg": ecpg_of[code],
            "ghost": code in ghost,
            "hand": code == "07002",
        })

    ye002 = ADJ["ye002"]
    return codes, ecpg_only, ye002


# ------------------------------------------------------------------ the figure

def figure(codes, ecpg_only, ye002):
    n = len(codes)
    rows = (n + PER_ROW - 1) // PER_ROW
    left, top = 40, 92
    band2_w = 40 + (21 + 1) * (STEP + 9) + 60
    w = max(40 + PER_ROW * STEP + 40, band2_w, 860)
    band1_h = rows * STEP
    band2_y = top + band1_h + 118
    h = band2_y + 150

    pos = {}
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}" font-family="Iowan Old Style, Palatino, '
           f'Georgia, serif" role="img" aria-label="Two listings of one '
           f'publisher\'s error codes">',
           f'<rect width="{w}" height="{h}" fill="{PAPER}"/>']

    out.append(f'<text x="{left}" y="34" font-size="15" fill="{INK}">'
               f'One publisher, two listings of the same kind of thing</text>')
    out.append(f'<text x="{left}" y="54" font-size="11" fill="{MID}">'
               f'PostgreSQL 18.6. Every cell is one SQLSTATE. '
               f'Nothing is drawn that is not in the tarball.</text>')

    out.append(f'<text x="{left}" y="{top - 14}" font-size="12" fill="{INK}">'
               f'Appendix A of the manual — {n} codes, generated from '
               f'src/backend/utils/errcodes.txt</text>')

    for i, c in enumerate(codes):
        x = left + (i % PER_ROW) * STEP
        y = top + (i // PER_ROW) * STEP
        pos[c["code"]] = (x + CELL / 2, y + CELL)
        fill = PAPER
        stroke = FAINT
        if c["in_ecpg"]:
            fill = "#efe7d8"
            stroke = MID
        if c["conflict"]:
            fill = CONFLICT
            stroke = CONFLICT
        out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                   f'fill="{fill}" stroke="{stroke}" stroke-width="0.7"/>')
        if c["two_rows"]:
            out.append(f'<line x1="{x + 2}" y1="{y + CELL - 2}" '
                       f'x2="{x + CELL - 2}" y2="{y + 2}" '
                       f'stroke="{INK}" stroke-width="0.9"/>')

    for k, line in enumerate([
        'Uniform, as the reader meets it. The six struck cells are codes that carry '
        'two macro names on two rows of the vocabulary file;',
        'the generator emits one row per name that has a condition name, so nothing '
        'above shows that 268 rows are 262 codes.']):
        out.append(f'<text x="{left}" y="{top + band1_h + 20 + k * 14}" '
                   f'font-size="10.5" fill="{MID}">{html.escape(line)}</text>')

    # ---- band 2
    order = [c["code"] for c in codes if c["in_ecpg"]] + [c["code"] for c in ecpg_only]
    look = {c["code"]: c for c in codes}
    look.update({c["code"]: c for c in ecpg_only})
    out.append(f'<text x="{left}" y="{band2_y - 16}" font-size="12" fill="{INK}">'
               f'The listing in §34.8.3 of the same manual — {len(order)} codes, '
               f'written by hand for the embedded-SQL client</text>')

    for i, code in enumerate(order):
        c = look[code]
        x = left + i * (STEP + 9)
        y = band2_y
        fill = "#efe7d8" if c["in_appendix"] else MARK
        stroke = MID if c["in_appendix"] else MARK
        if c.get("conflict"):
            fill = stroke = CONFLICT
        out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                   f'fill="{fill}" stroke="{stroke}" stroke-width="0.7"/>')
        out.append(f'<text x="{x + CELL / 2}" y="{y + CELL + 13}" font-size="8" '
                   f'fill="{MID}" text-anchor="middle" '
                   f'transform="rotate(60 {x + CELL / 2} {y + CELL + 13})">'
                   f'{code}</text>')
        if c.get("ghost"):
            out.append(f'<circle cx="{x + CELL / 2}" cy="{y - 9}" r="3.2" '
                       f'fill="none" stroke="{GHOST}" stroke-width="1.2"/>')
        if c["in_appendix"]:
            x1, y1 = pos[code]
            out.append(f'<path d="M {x1} {y1} C {x1} {y1 + 46}, {x + CELL / 2} '
                       f'{y - 46}, {x + CELL / 2} {y}" fill="none" '
                       f'stroke="{MID}" stroke-width="0.5" opacity="0.55"/>')

    # ---- YE000
    yx = left + len(order) * (STEP + 9) + 26
    out.append(f'<rect x="{yx}" y="{band2_y}" width="{CELL}" height="{CELL}" '
               f'fill="none" stroke="{INK}" stroke-width="1" '
               f'stroke-dasharray="2 2"/>')
    out.append(f'<text x="{yx + CELL / 2}" y="{band2_y + CELL + 13}" font-size="8" '
               f'fill="{INK}" text-anchor="middle" '
               f'transform="rotate(60 {yx + CELL / 2} {band2_y + CELL + 13})">'
               f'YE000</text>')

    ly = band2_y + 72
    for text, colour, dash in [
        (f'in both listings — 14 codes', MID, None),
        ('in the ecpg listing only — 7 codes, none of them in Appendix A, which '
         'the same page tells the reader to consult in each case', MARK, None),
        (f'an error in Appendix A and a warning in the ecpg listing — 4 codes',
         CONFLICT, None),
        (f'published here and nowhere in the machine — YE002, offered for '
         f'{len(ye002["documented_conditions"])} conditions, absent from every file '
         f'of the tarball outside doc/', GHOST, None),
        (f'imposed at {ye002["n_sites"]} sites, on exactly those four conditions, '
         f'and in neither listing — YE000', INK, "2 2"),
    ]:
        out.append(f'<rect x="{left}" y="{ly - 8}" width="9" height="9" '
                   f'fill="{"none" if dash else colour}" stroke="{colour}" '
                   f'stroke-width="1"'
                   + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
        out.append(f'<text x="{left + 16}" y="{ly}" font-size="10.5" '
                   f'fill="{INK}">{html.escape(text)}</text>')
        ly += 16

    out.append('</svg>')
    return "\n".join(out)


# -------------------------------------------------------------------- the page

def page(codes, ecpg_only, ye002, adj):
    data = json.dumps({"codes": codes, "ecpg_only": ecpg_only, "ye002": ye002},
                      separators=(",", ":"))
    n_both = sum(1 for c in codes if c["in_ecpg"])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Other Listing — one publisher, two vocabularies</title>
<style>
 :root {{
   --ink:{INK}; --paper:{PAPER}; --faint:{FAINT}; --mid:{MID};
   --mark:{MARK}; --conflict:{CONFLICT}; --ghost:{GHOST};
 }}
 @media (prefers-color-scheme: dark) {{
   :root {{ --ink:#ece7de; --paper:#16150f; --faint:#3a382f;
            --mid:#8c8578; --mark:#d4756f; --conflict:#d9a441; --ghost:#8fae8f; }}
 }}
 * {{ box-sizing:border-box; }}
 body {{ margin:0; background:var(--paper); color:var(--ink);
        font:15px/1.55 "Iowan Old Style", Palatino, Georgia, serif; }}
 main {{ max-width:1000px; margin:0 auto; padding:2.4rem 1.2rem 4rem; }}
 h1 {{ font-size:1.5rem; font-weight:600; margin:0 0 .2rem; letter-spacing:.01em; }}
 .sub {{ color:var(--mid); margin:0 0 1.6rem; font-size:.95rem; }}
 h2 {{ font-size:1rem; font-weight:600; margin:2rem 0 .5rem; }}
 .note {{ color:var(--mid); font-size:.85rem; margin:.3rem 0 1rem; }}
 .wall {{ display:flex; flex-wrap:wrap; gap:3px; margin:.6rem 0; }}
 .c {{ width:15px; height:15px; border:1px solid var(--faint);
       background:transparent; padding:0; cursor:pointer; position:relative; }}
 .c:focus-visible {{ outline:2px solid var(--ink); outline-offset:2px; }}
 .c.both {{ background:var(--faint); border-color:var(--mid); }}
 .c.conflict {{ background:var(--conflict); border-color:var(--conflict); }}
 .c.only {{ background:var(--mark); border-color:var(--mark); }}
 .c.two::after {{ content:""; position:absolute; inset:1px;
    background:linear-gradient(45deg,transparent 44%,var(--ink) 44%,
    var(--ink) 56%,transparent 56%); }}
 .c.ghost {{ box-shadow:0 0 0 2px var(--ghost); }}
 .c.dim {{ opacity:.18; }}
 .c.sel {{ outline:2px solid var(--ink); outline-offset:1px; }}
 .row2 {{ display:flex; flex-wrap:wrap; gap:6px; align-items:flex-end; }}
 .stack {{ text-align:center; font-size:9px; color:var(--mid); width:26px; }}
 .stack .c {{ margin:0 auto 3px; }}
 .controls {{ display:flex; flex-wrap:wrap; gap:.4rem; margin:1rem 0 .2rem; }}
 button.f {{ font:inherit; font-size:.8rem; padding:.22rem .6rem;
   border:1px solid var(--faint); background:transparent; color:var(--ink);
   cursor:pointer; border-radius:2px; }}
 button.f[aria-pressed="true"] {{ border-color:var(--ink); background:var(--faint); }}
 #readout {{ border-top:1px solid var(--faint); margin-top:1.4rem;
   padding-top:1rem; min-height:9.5rem; font-size:.92rem; }}
 #readout .code {{ font:600 1.2rem/1.2 ui-monospace,"SFMono-Regular",Menlo,monospace; }}
 #readout dl {{ display:grid; grid-template-columns:11rem 1fr; gap:.25rem .9rem;
   margin:.7rem 0 0; }}
 #readout dt {{ color:var(--mid); font-size:.85rem; }}
 #readout dd {{ margin:0; }}
 .legend {{ font-size:.85rem; color:var(--mid); margin-top:1.4rem; }}
 .legend span {{ display:inline-block; margin-right:1.1rem; }}
 .swatch {{ display:inline-block; width:11px; height:11px; vertical-align:-1px;
   border:1px solid var(--mid); margin-right:.3rem; }}
 footer {{ margin-top:2.6rem; border-top:1px solid var(--faint); padding-top:1rem;
   font-size:.82rem; color:var(--mid); }}
 a {{ color:inherit; }}
 @media (prefers-reduced-motion:no-preference) {{ .c {{ transition:opacity .12s; }} }}
</style>
</head>
<body>
<main>
 <h1>The Other Listing</h1>
 <p class="sub">One publisher, two listings of the same kind of thing.
 PostgreSQL 18.6, read from the source tarball. Session 78 of
 <em>Error as Method</em>, 2026-09-03.</p>

 <h2>Appendix A — {len(codes)} codes, generated from <code>src/backend/utils/errcodes.txt</code></h2>
 <p class="note">Pick a cell. Everything in the readout is in the tarball; the
 site counts are this practice's own measurement of 2026-09-01, corrected.</p>
 <div class="controls" id="filters">
  <button class="f" data-f="all" aria-pressed="true">all {len(codes)}</button>
  <button class="f" data-f="both" aria-pressed="false">in both listings ({n_both})</button>
  <button class="f" data-f="conflict" aria-pressed="false">classified differently (4)</button>
  <button class="f" data-f="siteless" aria-pressed="false">no imposition site</button>
  <button class="f" data-f="two" aria-pressed="false">two macro names (6)</button>
 </div>
 <div class="wall" id="wall"></div>

 <h2>The listing in §34.8.3 of the same manual — written by hand, for the embedded-SQL client</h2>
 <p class="note">The page these come from tells the reader, in as many words,
 to consult Appendix A in each case. Seven of them are not in Appendix A.</p>
 <div class="row2" id="row2"></div>

 <div id="readout" aria-live="polite"></div>

 <p class="legend">
  <span><i class="swatch" style="background:var(--faint)"></i>in both</span>
  <span><i class="swatch" style="background:var(--mark);border-color:var(--mark)"></i>ecpg listing only</span>
  <span><i class="swatch" style="background:var(--conflict);border-color:var(--conflict)"></i>error here, warning there</span>
  <span><i class="swatch" style="box-shadow:0 0 0 2px var(--ghost)"></i>published, absent from the machine</span>
 </p>

 <footer>
  Evidence, measuring code and the predictions fixed before it:
  <code>works/2026-09-03-the-other-listing/</code> in the repository.
  The two published listings, live:
  <a href="https://www.postgresql.org/docs/18/errcodes-appendix.html">Appendix A</a>
  (262 codes) and
  <a href="https://www.postgresql.org/docs/18/ecpg-errors.html">§34.8.3</a>
  (21, seven of them absent from the first).
  Tarball SHA-256 <code>555610c2…881d9f</code>, verified against the publisher's
  own <code>.sha256</code>. No data is fetched by this page; nothing is loaded
  from outside it.
 </footer>
</main>
<script type="application/json" id="d">{data}</script>
<script>
(function () {{
  var D = JSON.parse(document.getElementById("d").textContent);
  var wall = document.getElementById("wall");
  var row2 = document.getElementById("row2");
  var out = document.getElementById("readout");
  var filter = "all", selected = null;

  function cls(c, second) {{
    var k = ["c"];
    if (!c.in_appendix) k.push("only");
    else if (c.in_ecpg) k.push("both");
    if (c.conflict) k.push("conflict");
    if (c.two_rows) k.push("two");
    if (c.ghost) k.push("ghost");
    if (!second && filter !== "all") {{
      var keep = (filter === "both" && c.in_ecpg)
              || (filter === "conflict" && c.conflict)
              || (filter === "siteless" && c.sites === 0)
              || (filter === "two" && c.two_rows);
      if (!keep) k.push("dim");
    }}
    if (selected === c.code) k.push("sel");
    return k.join(" ");
  }}

  function esc(s) {{
    return String(s).replace(/[&<>]/g, function (m) {{
      return {{"&": "&amp;", "<": "&lt;", ">": "&gt;"}}[m];
    }});
  }}

  function show(c) {{
    selected = c.code;
    var rows = [];
    rows.push(["in Appendix A", c.in_appendix
      ? "yes — condition name <code>" + esc(c.condition || "—") + "</code>"
      : "<strong>no</strong>"]);
    rows.push(["severity there", c.in_appendix
      ? c.severity.join(", ").replace("E", "E (error)")
          .replace("W", "W (warning)").replace("S", "S (success)")
      : "—"]);
    rows.push(["macro name" + (c.two_rows ? "s" : ""), c.macros
      ? c.macros.map(function (m) {{ return "<code>" + esc(m) + "</code>"; }}).join("<br>")
      : "—"]);
    rows.push(["in the ecpg listing", c.in_ecpg
      ? c.ecpg.map(function (e) {{
          return "<code>" + esc(e.term) + "</code> — " + esc(e.text);
        }}).join("<br><br>")
      : "no"]);
    if (c.in_appendix) {{
      rows.push(["imposition sites", c.sites === 0
        ? "<strong>none in the whole distribution</strong>"
        : c.sites + " across " + c.n_files + " files"]);
    }}
    if (c.ghost) {{
      rows.push(["in the machine", "<strong>nowhere.</strong> This code occurs "
        + "in no file of the tarball outside <code>doc/</code>. The "
        + D.ye002.documented_conditions.length + " conditions the manual gives "
        + "it are raised at " + D.ye002.n_sites + " sites, every one of them "
        + "passing <code>ECPG_SQLSTATE_ECPG_INTERNAL_ERROR</code>, which is "
        + "<code>YE000</code> — a code in neither listing."]);
    }}
    if (c.hand) {{
      rows.push(["how it was found", "by hand. The extraction rule takes the "
        + "code after the word SQLSTATE and cannot take the second code of "
        + "\\u201c(SQLSTATE 07001 or 07002)\\u201d. The rule under-counts; the "
        + "correction is reported rather than folded in."]);
    }}
    out.innerHTML = '<span class="code">' + esc(c.code) + "</span> "
      + '<span class="note">class ' + esc(c.klass) + "</span><dl>"
      + rows.map(function (r) {{
          return "<dt>" + r[0] + "</dt><dd>" + r[1] + "</dd>";
        }}).join("") + "</dl>";
    draw();
  }}

  function cell(c, second) {{
    var b = document.createElement("button");
    b.className = cls(c, second);
    b.type = "button";
    b.title = c.code;
    b.setAttribute("aria-label", c.code);
    b.addEventListener("click", function () {{ show(c); }});
    return b;
  }}

  function draw() {{
    wall.textContent = "";
    D.codes.forEach(function (c) {{ wall.appendChild(cell(c, false)); }});
    row2.textContent = "";
    var second = D.codes.filter(function (c) {{ return c.in_ecpg; }})
      .concat(D.ecpg_only);
    second.forEach(function (c) {{
      var s = document.createElement("div");
      s.className = "stack";
      s.appendChild(cell(c, true));
      s.appendChild(document.createTextNode(c.code));
      row2.appendChild(s);
    }});
  }}

  document.getElementById("filters").addEventListener("click", function (ev) {{
    var b = ev.target.closest("button.f");
    if (!b) return;
    filter = b.dataset.f;
    [].forEach.call(this.querySelectorAll("button.f"), function (x) {{
      x.setAttribute("aria-pressed", String(x === b));
    }});
    draw();
  }});

  draw();
  var ye = D.ecpg_only.filter(function (c) {{ return c.ghost; }})[0];
  show(ye || D.ecpg_only[0]);
}}());
</script>
</body>
</html>
"""


def main():
    R, ADJ, S77 = load(sys.argv[1]), load(sys.argv[2]), load(sys.argv[3])
    codes, ecpg_only, ye002 = build_model(R, ADJ, S77)
    with open("figure.svg", "w", encoding="utf-8") as fh:
        fh.write(figure(codes, ecpg_only, ye002))
    with open("index.html", "w", encoding="utf-8") as fh:
        fh.write(page(codes, ecpg_only, ye002, ADJ))
    print(f"figure.svg and index.html written: {len(codes)} appendix codes, "
          f"{sum(1 for c in codes if c['in_ecpg'])} shared, "
          f"{len(ecpg_only)} in the ecpg listing only")


if __name__ == "__main__":
    main()
