#!/usr/bin/env python3
"""page.py -- build index.html: all 120 verdicts, with their sentences and their reasons.

Self-contained, static, no script, no external load.  The point of it is that disagreeing with this
night costs a reader nothing but reading: every row carries what was read at stage 1, what was read
at stage 2, what the adjudicator said and why, and the mechanical distance to the nearest party term
so a reader can see where the judgement and the scan part company.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

CSS = """
:root { color-scheme: light dark; }
body { margin:0; background:#faf7f1; color:#1c1a17;
  font-family:"Iowan Old Style","Palatino Linotype",Palatino,Charter,Georgia,serif;
  line-height:1.55; }
.wrap { max-width:1080px; margin:0 auto; padding:40px 20px 80px; }
h1 { font-size:2.1rem; margin:0 0 .2em; font-weight:600; letter-spacing:-.01em; }
h2 { font-size:1.15rem; margin:2.4em 0 .7em; font-weight:600;
  letter-spacing:.08em; text-transform:uppercase; color:#6d685f; }
p { max-width:74ch; }
.lede { color:#6d685f; }
table { border-collapse:collapse; width:100%; font-size:.87rem; margin-top:.6em; }
th { text-align:left; font-weight:600; font-size:.72rem; letter-spacing:.09em;
  text-transform:uppercase; color:#6d685f; border-bottom:1px solid #1c1a17;
  padding:6px 8px; vertical-align:bottom; }
td { border-bottom:1px solid #e4ded2; padding:9px 8px; vertical-align:top; }
td.id { font-variant-numeric:tabular-nums; white-space:nowrap; color:#6d685f; }
td.num { text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }
.v { font-size:.7rem; letter-spacing:.07em; font-weight:600; white-space:nowrap;
  padding:2px 6px; border:1px solid currentColor; }
.NAMED { color:#1c1a17; background:#e4ded2; }
.UNNAMED { color:#6d685f; }
.NOACTOR { color:#8a8377; }
.sent { font-size:.93rem; }
.why { color:#6d685f; font-size:.82rem; margin-top:4px; }
.moved td { background:#f2ece0; }
.summary td, .summary th { border-bottom:1px solid #e4ded2; }
footer { margin-top:3em; color:#6d685f; font-size:.85rem; border-top:1px solid #c9c2b6;
  padding-top:1em; }
a { color:inherit; }
@media (prefers-color-scheme: dark) {
  body { background:#16150f; color:#ece6da; }
  h2, .lede, .why, td.id, .UNNAMED { color:#a49d90; }
  .NOACTOR { color:#8a8377; }
  th { color:#a49d90; border-bottom-color:#ece6da; }
  td { border-bottom-color:#33302a; }
  .NAMED { color:#ece6da; background:#33302a; }
  .moved td { background:#22201a; }
  footer { border-top-color:#33302a; }
}
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def cls(v):
    return "NOACTOR" if v == "NO-ACTOR" else v


def main():
    s1 = {r["id"]: r for r in json.load(open(HERE / "stage1-verdicts.json"))["rows"]}
    s2 = {r["id"]: r for r in json.load(open(HERE / "stage2-verdicts.json"))["rows"]}
    res = json.load(open(HERE / "results.json"))
    pop = json.load(open(HERE / "population-curve.json"))
    near = res["mechanical_ceiling"]["per_row_nearest_party_term_whole_document"]
    ids = sorted(s1, key=lambda s: int(s[1:]))

    o = []
    o.append('<div class="wrap">')
    o.append("<h1>Adjacent Text &#8212; the 120 verdicts</h1>")
    o.append('<p class="lede">Session 88, 2026-09-12. Sixty agentless obligations drawn with '
             '<code>random.Random(88)</code> from the 1,190 in 22 WHATWG living standards, each read '
             'twice: once as the sentence alone, once with the enclosing heading chain and the five '
             'preceding blocks. One question both times &#8212; <em>can a reader name the party that '
             'must perform the action this sentence requires?</em> One adjudicator, who wrote the '
             'predictions. Every verdict is here so that disagreeing costs nothing but reading.</p>')

    o.append("<h2>What the two readings gave</h2>")
    o.append('<table class="summary"><tr><th>reading</th><th>NAMED</th><th>UNNAMED</th>'
             '<th>NO-ACTOR</th></tr>')
    for lab, c in (("the sentence alone", res["stage1"]), ("with the fixed context", res["stage2"])):
        o.append("<tr><td>%s</td><td class='num'>%d</td><td class='num'>%d</td>"
                 "<td class='num'>%d</td></tr>"
                 % (lab, c.get("NAMED", 0), c.get("UNNAMED", 0), c.get("NO-ACTOR", 0)))
    o.append("</table>")

    o.append("<h2>And what the mechanical scan says a reader could possibly have found</h2>")
    o.append('<p class="lede">The share of all 1,190 obligations with a term for a party '
             '&#8212; <em>user agent, browser, author, implementation, implementer, markup generator, '
             'conformance checker, parser, server, client, validator, editor</em> &#8212; within reach, '
             'by how far back the reader may look. A term in reach is a ceiling on naming, never '
             'naming itself.</p>')
    steps = [0, 1, 2, 3, 5, 8, 13, 20, 35, 50, 100, 200]
    o.append("<table><tr><th>blocks back</th>" +
             "".join("<th style='text-align:right'>%d</th>" % w for w in steps) +
             "<th style='text-align:right'>whole doc</th></tr><tr><td>a party term is in reach</td>" +
             "".join("<td class='num'>%.1f%%</td>" % (100.0 * pop["curve"][str(w)] / pop["population"])
                     for w in steps) +
             "<td class='num'>%.1f%%</td></tr></table>"
             % (100.0 * pop["whole_document"] / pop["population"]))

    o.append("<h2>The sixty</h2>")
    o.append('<p class="lede">Shaded rows are the nine the context recovered. '
             '<strong>d</strong> is the distance in blocks at which the naming evidence stands; '
             '<strong>nearest</strong> is the mechanical distance to the nearest party term anywhere '
             'earlier in the document, which is a fact about the corpus and not a judgement.</p>')
    o.append("<table><tr><th>id</th><th>standard</th><th>the sentence, and the two readings</th>"
             "<th>alone</th><th>in&nbsp;context</th><th>d</th><th>nearest</th></tr>")
    for i in ids:
        a, b = s1[i], s2[i]
        moved = b["stage2"] == "NAMED" and a["stage1"] != "NAMED"
        n = near.get(i)
        o.append("<tr%s>" % (' class="moved"' if moved else ""))
        o.append('<td class="id">%s</td><td class="id">%s</td>' % (i, esc(b["doc"])))
        o.append('<td><div class="sent">%s</div>'
                 '<div class="why"><strong>alone:</strong> %s</div>'
                 '<div class="why"><strong>in context:</strong> %s</div></td>'
                 % (esc(a["sentence"]), esc(a["stage1_reason"]), esc(b["stage2_reason"])))
        o.append('<td><span class="v %s">%s</span></td>' % (cls(a["stage1"]), a["stage1"]))
        o.append('<td><span class="v %s">%s</span></td>' % (cls(b["stage2"]), b["stage2"]))
        o.append('<td class="num">%s</td>' % ("&#8212;" if b["distance"] is None else b["distance"]))
        o.append('<td class="num">%s</td>' % ("none" if n is None else n))
        o.append("</tr>")
    o.append("</table>")

    o.append("<footer>Ulysses (the nightly line) &#183; Error as Method &#183; Session 88, "
             "2026-09-12. The corpus is 22 WHATWG living standards, CC BY 4.0, harvested by this "
             "line on 2026-09-11 and asserted byte-identical here before anything was measured. "
             "Code, pre-registration and source manifest are in the work&#8217;s directory. "
             "The paper whose hypothesis this night borrowed &#8212; Krisch &amp; Houdek (2015) "
             "&#8212; is paywalled and was not read; everything said about it comes from two "
             "secondary reports that were.</footer>")
    o.append("</div>")

    html = ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>Adjacent Text &#8212; the 120 verdicts</title>"
            "<style>%s</style></head><body>\n%s\n</body></html>\n" % (CSS, "\n".join(o)))
    (HERE / "index.html").write_text(html)
    print("index.html  %d bytes" % len(html))


if __name__ == "__main__":
    main()
