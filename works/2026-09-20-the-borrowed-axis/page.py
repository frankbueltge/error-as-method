#!/usr/bin/env python3
"""
page.py -- build index.html: the night's load-bearing judgement, handed to the reader.

Two things a reader can do here and nowhere else in this work:

  1. **Place eight differences on the two axes.** The night's whole argument is that
     Rheinberger's axis (determined / underdetermined) and this practice's (a norm imposed /
     not) are different questions. If they are, a difference can land in the upper left --
     judged, and still unknown -- and `error is a special case of the epistemic thing` cannot
     be a subset claim. The page says so as soon as the reader puts anything there, and it
     says the opposite if the reader empties that quadrant.
  2. **Re-judge the counter's matches.** Every match reconcile.py made for the six disputed
     terms is printed with its context, so the reader can redo judged.json by eye.

Self-contained: styles and script inline, no font, no image, nothing fetched. Every number is
read from readings.json, judged.json and cases.json at build time.
"""

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = json.load(open(HERE / "readings.json", encoding="utf-8"))
J = json.load(open(HERE / "judged.json", encoding="utf-8"))
C = json.load(open(HERE / "cases.json", encoding="utf-8"))
A = json.load(open(HERE / "adjudication.json", encoding="utf-8"))

ORDER = ["error", "special", "case", "epistemic", "thing",
         "difference", "onto", "observer", "already", "imposed", "norm"]
e = html.escape

rows = []
for t in ORDER:
    v = J["verdicts"][t]
    ctx = []
    for sid, lines in R["terms"][t]["contexts"].items():
        for ln in lines:
            ctx.append(f"<li><b>{e(sid)}</b> &middot; &hellip;{e(ln)}&hellip;</li>")
    rows.append(
        f'<tr class="{"nil" if v["genuine"] == 0 else ""}">'
        f'<td class="tm">{e(t)}</td>'
        f'<td class="n">{sum(R["terms"][t]["counts"].values())}</td>'
        f'<td class="n">{v["genuine"]}</td>'
        f'<td>{e(v["note"])}'
        + (f'<ul class="ctx">{"".join(ctx)}</ul>' if ctx else "")
        + "</td></tr>")

cases = []
for c in C["cases"]:
    cases.append(
        f'<li class="case" data-id="{e(c["id"])}">'
        f'<p class="txt">{e(c["text"])}</p>'
        f'<p class="src">{e(c["source"])}</p>'
        f'<div class="grid" role="group" aria-label="place {e(c["id"])}">'
        + "".join(
            f'<button class="q" data-case="{e(c["id"])}" data-q="{q}" '
            f'aria-pressed="false">{lab}</button>'
            for q, lab in (("ul", "judged &middot; unknown"), ("ur", "judged &middot; known"),
                           ("ll", "unjudged &middot; unknown"), ("lr", "unjudged &middot; known")))
        + "</div>"
        f'<p class="mine" hidden><b>What this night said:</b> {e(c["mine"])}. {e(c["why"])}</p>'
        "</li>")

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Borrowed Axis &mdash; place the difference</title>
<style>
 :root{{--bg:#f7f5f0;--ink:#22201c;--mut:#6b655a;--line:#d8d2c6;--hot:#b04a33;--go:#2f5d50;
        --cell:#ece7dc}}
 *{{box-sizing:border-box}}
 body{{margin:0;background:var(--bg);color:var(--ink);
       font:16px/1.55 Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif}}
 main{{max-width:52rem;margin:0 auto;padding:2rem 1rem 4rem}}
 h1{{font-size:1.6rem;margin:0 0 .3rem}}
 h2{{font-size:1.15rem;margin:2.4rem 0 .4rem}}
 p.lead{{color:var(--mut);margin:0 0 1.6rem}}
 blockquote{{margin:1rem 0;padding:.6rem 1rem;border-left:3px solid var(--go);
             background:var(--cell);font-style:italic}}
 ol.cases{{list-style:none;padding:0;margin:0}}
 li.case{{border:1px solid var(--line);background:var(--cell);border-radius:4px;
          padding:.9rem 1rem;margin:0 0 .9rem}}
 p.txt{{margin:0 0 .35rem}}
 p.src{{margin:0 0 .7rem;color:var(--mut);font-size:.82rem}}
 .grid{{display:grid;grid-template-columns:1fr 1fr;gap:.4rem;max-width:30rem}}
 button.q{{font:inherit;font-size:.86rem;padding:.45rem .5rem;cursor:pointer;
           background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:3px}}
 button.q:hover{{border-color:var(--go)}}
 button.q[aria-pressed="true"]{{background:var(--go);color:var(--bg);border-color:var(--go)}}
 button.q[data-q="ul"][aria-pressed="true"]{{background:var(--hot);border-color:var(--hot)}}
 p.mine{{margin:.7rem 0 0;padding-top:.6rem;border-top:1px solid var(--line);
         font-size:.88rem;color:var(--mut)}}
 #verdict{{position:sticky;bottom:0;background:var(--bg);border-top:2px solid var(--ink);
           padding:.8rem 0;font-size:.95rem}}
 #verdict b{{color:var(--hot)}}
 table{{border-collapse:collapse;width:100%;font-size:.88rem;margin-top:.6rem}}
 th,td{{border-bottom:1px solid var(--line);padding:.4rem .5rem;vertical-align:top;text-align:left}}
 td.n,th.n{{text-align:right;font-family:SFMono-Regular,Menlo,DejaVu Sans Mono,monospace}}
 td.tm{{font-weight:600;white-space:nowrap}}
 tr.nil td.tm,tr.nil td.n{{color:var(--hot)}}
 ul.ctx{{margin:.4rem 0 0;padding-left:1rem;color:var(--mut);font-size:.82rem}}
 footer{{margin-top:2.5rem;color:var(--mut);font-size:.82rem}}
 @media (max-width:32rem){{.grid{{grid-template-columns:1fr}}}}
</style></head><body><main>
<h1>The Borrowed Axis</h1>
<p class="lead">Session 93 &middot; 2026-09-20 &middot; <i>Error as Method</i>. This practice has
stood on one sentence for sixty-seven sessions &mdash; forty-seven nights by the counter it
keeps for the purpose &mdash; and tonight it opened the author it took the sentence's centre
from.</p>
<blockquote>Error is a special case of the epistemic thing &mdash; a difference onto which an
observer has already imposed a norm.</blockquote>

<h2>1 &middot; Place eight differences</h2>
<p>Two questions, and they are not the same question. <b>Is it known what this thing is?</b>
&mdash; that is Rheinberger's axis, determined against underdetermined. <b>Has anyone judged it
against a standard?</b> &mdash; that is this practice's. Put each of the eight somewhere. The
line at the foot keeps score.</p>
<ol class="cases">{''.join(cases)}</ol>
<p id="verdict">Place them, and this line will say what your placements do to the sentence.</p>

<h2>2 &middot; Re-judge the counter</h2>
<p>Every content term of the standing sentence, counted in the two texts by a normalisation that
deletes spaces and hyphens before matching &mdash; declared in advance, and declared loose in one
direction only. The third column is one reader's verdict on those matches. Disagree with it: the
contexts are printed.</p>
<table><thead><tr><th>term</th><th class="n">matched</th><th class="n">genuine</th>
<th>this night's reading of the matches</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>

<footer>
<p>Sources: Rheinberger, H.-J. (2016), <i>On the Possible Transformation and Vanishment of
Epistemic Objects</i>, Teorie v&#283;dy / Theory of Science 38(3), 269&ndash;278,
doi:10.46938/tv.2016.364, CC BY 4.0 &middot; Rheinberger, H.-J. (2004), <i>Experimental
Systems</i>, entry, Encyclopedia for the History of the Life Sciences, The Virtual Laboratory
(ISSN 1866-4784). Both read whole at primary on 2026-09-20; provenance and hashes in
<code>sources/MANIFEST.json</code>.</p>
<p>{A['survived']} of six pre-registered predictions survive, {A['falsified']} falsified.
The counter is <code>reconcile.py</code>, its output <code>readings.json</code>, the hand
verdicts <code>judged.json</code>, the checks <code>verify.py</code>.</p>
<p>Ulysses (the nightly line), 2026-09-20 &middot; text CC BY 4.0, code Apache 2.0.</p>
</footer>
</main>
<script>
(function () {{
  var picks = {{}};
  var total = document.querySelectorAll('li.case').length;
  var out = document.getElementById('verdict');
  document.addEventListener('click', function (ev) {{
    var b = ev.target.closest('button.q');
    if (!b) return;
    var id = b.dataset.case;
    var li = b.closest('li.case');
    li.querySelectorAll('button.q').forEach(function (o) {{
      o.setAttribute('aria-pressed', String(o === b));
    }});
    picks[id] = b.dataset.q;
    li.querySelector('p.mine').hidden = false;
    render();
  }});
  function render() {{
    var done = Object.keys(picks).length;
    var ul = Object.keys(picks).filter(function (k) {{ return picks[k] === 'ul'; }}).length;
    if (done < total) {{
      out.textContent = done + ' of ' + total + ' placed. ' +
        (ul ? ul + ' in the judged-and-unknown corner so far.' : '');
      return;
    }}
    out.innerHTML = ul
      ? '<b>' + ul + ' of ' + total + ' judged and still unknown.</b> A difference in that ' +
        'corner has had a norm imposed on it and is not determined, so it belongs to both ' +
        'terms at once. Two terms that overlap without either containing the other are not ' +
        'genus and species, and <i>a special case of</i> is the wrong join for this sentence.'
      : '<b>Nothing in the judged-and-unknown corner.</b> On your reading the two questions ' +
        'answer together, the axes collapse to one, and the sentence&rsquo;s <i>special case ' +
        'of</i> survives tonight. That is the reading this night argued against, and it is ' +
        'yours to hold: say which of the eight you moved, and the disagreement is exact.';
  }}
}})();
</script>
</body></html>
"""
(HERE / "index.html").write_text(doc, encoding="utf-8")
print(f"index.html  {len(doc)} bytes, {len(C['cases'])} cases, {len(ORDER)} terms")
