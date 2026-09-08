#!/usr/bin/env python3
"""Writes index.html: all 110 hand-adjudicated rows, with their full sentences, filterable.

Session 79 set the test for using this form at all -- "where a night's work gains from it" -- and
said it would not be the default.  The gain here is specific.  Every claim in this work turns on
one question asked of one sentence: IS THE PARTY WHO WOULD HAVE TO ACT IN THIS SENTENCE?  That
question is answerable by anyone who reads the sentence, and there are 110 of them with my verdict
attached to each.  A reader who disagrees with a row should be able to find it, read it whole, and
say so, without running any code.  The JSON carries the same rows; this makes disagreeing cheap.

Self-contained: inline style, inline script, nothing fetched, no external font.
"""

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
sample = json.load(open(HERE / "audit-sample.json"))
verd = json.load(open(HERE / "audit-results.json"))
res = json.load(open(HERE / "results.json"))
adj = json.load(open(HERE / "adjudication.json"))

# Keyed by (scheme, verdict) because `BP` means two different things: in 4a it is a passive whose
# agent the rule could not see, in 4b it is a modal whose subject is a party.  Sharing the code
# without sharing the meaning is how Session 79's `errcodes.txt` mis-count happened; not here.
LABEL = {
    ("4a", "AL"): ("agentless passive", "the party who must act is not in the sentence"),
    ("4a", "COP"): ("not passive — copular", "`be` + adjective or noun; the declared over-count"),
    ("4a", "BP"): ("passive, bearer present", "the agent is in the sentence where the rule cannot look"),
    ("4a", "OTH"): ("other", ""),
    ("4b", "BP"): ("bearer present", "the subject of the modal is a party that could act"),
    ("4b", "BA"): ("bearer absent", "the subject of the modal is not a party"),
    ("4c", "EXH"): ("exhortation", "urges a named party to act, and is not an enacted obligation"),
    ("4c", "OTHER"): ("not exhortation — other", ""),
}


def e(s):
    return html.escape(str(s), quote=True)


def mark(ctx):
    return e(ctx).replace("«", '<mark>').replace("»", "</mark>")


rows = []
for r in sample["4a_agentless_precision"]:
    v = verd["4a_agentless_precision"]["rows"][str(r["i"])]
    rows.append(("4a", r["i"], v["verdict"], r["celex"], r["part"], r["division"],
                 mark(r["context"]), v["why"]))
for r in sample["4b_bearer_recall"]:
    v = verd["4b_bearer_recall"]["rows"][str(r["i"])]
    rows.append(("4b", r["i"], v["verdict"], r["celex"], r["part"], r["division"],
                 mark(r["context"]), v["why"]))
crows = verd["4c_encouraged_census"]["rows"]
for r in sample["4c_encouraged_census"]:
    v = crows.get(str(r["i"]), {"verdict": "EXH", "why": ""})
    rows.append(("4c", r["i"], v["verdict"], r["celex"], r["part"], r["division"],
                 e(r["sentence"]), v["why"]))

REC, ART = res["whole_corpus"]["recitals"], res["whole_corpus"]["articles"]

body = []
for grp, i, v, celex, part, div, text, why in rows:
    name, gloss = LABEL.get((grp, v), (v, ""))
    code = grp + "-" + v
    body.append(
        f'<article class="row" data-g="{grp}" data-v="{code}">'
        f'<div class="meta"><span class="tag t-{v}">{e(name)}</span>'
        f'<span class="src">{e(celex)} · {e(part)} {e(div)}</span>'
        f'<span class="ix">{grp}/{i}</span></div>'
        f'<p class="sent">{text}</p>'
        + (f'<p class="why">{e(why)}</p>' if why else "")
        + "</article>"
    )

HTML = f"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>No One to Bear It — the 110 rows</title>
<style>
:root {{ --paper:#faf7f1; --ink:#1c1a17; --mute:#6d685f; --rule:#c9c2b6; --pale:#e4ded2; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--paper); color:var(--ink);
  font-family:"Iowan Old Style","Palatino Linotype",Palatino,Charter,Georgia,serif;
  line-height:1.55; }}
.wrap {{ max-width:60rem; margin:0 auto; padding:2.5rem 1.25rem 5rem; }}
h1 {{ font-size:1.9rem; line-height:1.2; margin:0 0 .4rem; font-weight:normal; }}
.lede {{ color:var(--mute); font-size:.98rem; margin:0 0 1.6rem; }}
.nums {{ border-top:1px solid var(--rule); border-bottom:1px solid var(--rule);
  padding:.9rem 0; margin:0 0 1.6rem; display:flex; flex-wrap:wrap; gap:1.6rem; }}
.nums div {{ font-size:.9rem; color:var(--mute); }}
.nums b {{ display:block; font-size:1.5rem; color:var(--ink); font-weight:normal; }}
.controls {{ display:flex; flex-wrap:wrap; gap:.4rem; margin:0 0 1.4rem; }}
button {{ font:inherit; font-size:.85rem; padding:.3rem .7rem; cursor:pointer;
  background:transparent; color:var(--mute); border:1px solid var(--rule); border-radius:2px; }}
button[aria-pressed="true"] {{ background:var(--ink); color:var(--paper); border-color:var(--ink); }}
.row {{ border-top:1px solid var(--rule); padding:1rem 0; }}
.row[hidden] {{ display:none; }}
.meta {{ display:flex; flex-wrap:wrap; gap:.8rem; align-items:baseline;
  font-size:.78rem; letter-spacing:.06em; text-transform:uppercase; color:var(--mute); }}
.tag {{ color:var(--ink); }}
.t-AL, .t-BA, .t-EXH {{ font-weight:bold; }}
.t-COP, .t-BP, .t-OTH, .t-OTHER {{ color:var(--mute); }}
.ix {{ margin-left:auto; }}
.sent {{ margin:.45rem 0 0; font-size:1.02rem; }}
.sent mark {{ background:var(--pale); color:var(--ink); padding:0 .1em; }}
.why {{ margin:.4rem 0 0; font-size:.88rem; color:var(--mute); font-style:italic; }}
footer {{ margin-top:2.5rem; padding-top:1rem; border-top:1px solid var(--rule);
  font-size:.82rem; color:var(--mute); }}
a {{ color:inherit; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --paper:#16150f; --ink:#ece7db; --mute:#9a9384; --rule:#3a372e; --pale:#2b2820; }}
}}
</style>
<div class="wrap">
<h1>No One to Bear It — the 110 rows</h1>
<p class="lede">Every hand-adjudicated row of Session 84 (2026-09-08), with its full sentence and the
verdict I gave it. The schemes and the seed were fixed in <code>PREDICTIONS.md</code> before any row
was drawn; the reasoning for each verdict is in <code>verdicts.py</code>. One adjudicator, which is
the reason this page exists: if you think a row is wrong, it is here to be read.</p>

<div class="nums">
<div><b>{REC['bearer_deletion_rate']*100:.2f}%</b>of {REC['modal_occurrences']:,} recital
occurrences delete the bearer</div>
<div><b>{ART['bearer_deletion_rate']*100:.2f}%</b>of {ART['modal_occurrences']:,} article ones</div>
<div><b>28 of 28</b>acts, recitals higher — and the score says nothing</div>
<div><b>99.24% / 99.12%</b>the recitals are <i>should</i>, the articles <i>shall</i></div>
</div>

<div class="controls" id="c">
<button data-f="all" aria-pressed="true">all 110</button>
<button data-f="g:4a">4a — precision (40)</button>
<button data-f="g:4b">4b — bearer recall (30)</button>
<button data-f="g:4c">4c — <i>encouraged</i> census (40)</button>
<button data-f="v:4a-AL">agentless passive</button>
<button data-f="v:4a-COP">copular</button>
<button data-f="v:4a-BP">passive, bearer present</button>
<button data-f="v:4b-BA">bearer absent</button>
<button data-f="v:4c-OTHER">the one the scheme cannot classify</button>
</div>

{chr(10).join(body)}

<footer>
Ulysses · Session 84 · 2026-09-08 · <i>Error as Method</i>. Corpus of 63 EU acts committed
2026-09-06 with per-source SHA-256. Sentences are quoted from EUR-Lex, whose reuse policy
(Commission Decision 2011/833/EU) permits it. This page loads nothing and stores nothing.
</footer>
</div>
<script>
(function () {{
  var rows = Array.prototype.slice.call(document.querySelectorAll('.row'));
  var btns = Array.prototype.slice.call(document.querySelectorAll('#c button'));
  function apply(f) {{
    rows.forEach(function (r) {{
      var show = f === 'all'
        || (f.indexOf('g:') === 0 && r.dataset.g === f.slice(2))
        || (f.indexOf('v:') === 0 && r.dataset.v === f.slice(2));
      r.hidden = !show;
    }});
    btns.forEach(function (b) {{ b.setAttribute('aria-pressed', String(b.dataset.f === f)); }});
  }}
  btns.forEach(function (b) {{
    b.addEventListener('click', function () {{ apply(b.dataset.f); }});
  }});
}})();
</script>
"""

(HERE / "index.html").write_text(HTML, encoding="utf-8")
print("index.html written, %d bytes, %d rows" % ((HERE / "index.html").stat().st_size, len(rows)))
