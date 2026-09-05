#!/usr/bin/env python3
"""Builds index.html from census.json, results.json and corpus.json.

The page is the census and nothing else: 46 rows, each with its recital, its class, its verdict, the
article that carries it or the statement that none does, and the recital's own text on demand. The
two count tables of the work are static and are not repeated here -- a table of two numbers gains
nothing from a filter.

Self-contained: styles and script inline, no asset outside this directory, nothing fetched at run
time or at view time. Deterministic.
"""

import html
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
C = json.loads((HERE / "census.json").read_text(encoding="utf-8"))
R = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
CORPUS = json.loads((HERE / "corpus.json").read_text(encoding="utf-8"))

MECH = {i + 1: a["mechanical"] for i, a in enumerate(R["atoms"]["recital_atoms"])}

rows = []
for i, row in enumerate(C["rows"], 1):
    rows.append({
        "id": row["id"],
        "recital": row["recital"],
        "atom": row["atom"],
        "cls": row["class"],
        "verdict": row["verdict"],
        "article": row["article"],
        "quote": row.get("quote", ""),
        "note": row.get("note", ""),
        "mechanical": MECH.get(i, "?"),
        "recital_text": CORPUS["recitals"][str(row["recital"])],
    })

DATA = json.dumps(rows, ensure_ascii=False)

CSS = """
:root{--ink:#16150f;--paper:#f4f1e8;--faint:#d8d2c2;--grey:#6f6a5b;--accent:#8c2f18;}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif;line-height:1.55}
main{max-width:62rem;margin:0 auto;padding:2.5rem 1.25rem 5rem}
h1{font-size:1.9rem;margin:0 0 .2rem;font-weight:600}
.sub{color:var(--grey);margin:0 0 1.8rem;font-size:.95rem}
.lede{border-left:3px solid var(--accent);padding:.1rem 0 .1rem 1rem;margin:0 0 2rem;font-size:1.02rem}
.controls{display:flex;flex-wrap:wrap;gap:.4rem;margin:0 0 .4rem;align-items:baseline}
.controls span.lab{font-size:.72rem;letter-spacing:.09em;text-transform:uppercase;color:var(--grey);
 margin-right:.35rem;font-family:'IBM Plex Mono','DejaVu Sans Mono',monospace}
button{font:inherit;font-size:.85rem;background:transparent;color:var(--ink);
 border:1px solid var(--faint);border-radius:2px;padding:.22rem .6rem;cursor:pointer}
button[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.count{font-size:.85rem;color:var(--grey);margin:.9rem 0 1.1rem;
 font-family:'IBM Plex Mono','DejaVu Sans Mono',monospace}
ol{list-style:none;margin:0;padding:0}
li{border-top:1px solid var(--faint);padding:.85rem 0}
li[hidden]{display:none}
.head{display:flex;flex-wrap:wrap;gap:.55rem;align-items:baseline}
.rec{font-family:'IBM Plex Mono','DejaVu Sans Mono',monospace;font-size:.82rem;color:var(--grey);
 min-width:5.2rem}
.atom{flex:1 1 22rem;min-width:16rem}
.tag{font-family:'IBM Plex Mono','DejaVu Sans Mono',monospace;font-size:.68rem;letter-spacing:.06em;
 text-transform:uppercase;border:1px solid var(--faint);border-radius:2px;padding:.08rem .38rem;
 color:var(--grey);white-space:nowrap}
.tag.unmatched{color:var(--paper);background:var(--accent);border-color:var(--accent)}
.tag.reworded{color:var(--accent);border-color:var(--accent)}
.detail{margin:.6rem 0 0 5.75rem;font-size:.93rem}
@media (max-width:640px){.detail{margin-left:0}}
.detail p{margin:.35rem 0}
blockquote{margin:.4rem 0;padding-left:.85rem;border-left:2px solid var(--faint);color:#3a372c}
.mono{font-family:'IBM Plex Mono','DejaVu Sans Mono',monospace;font-size:.78rem;color:var(--grey)}
details{margin-top:.45rem}
summary{cursor:pointer;font-size:.82rem;color:var(--grey)}
details p{font-size:.9rem;color:#3a372c}
footer{margin-top:3rem;border-top:1px solid var(--faint);padding-top:1rem;
 font-size:.82rem;color:var(--grey)}
a{color:var(--accent)}
"""

JS = """
var ROWS = __DATA__;
var state = {cls:'all', verdict:'all'};

function tag(t, c){var s=document.createElement('span');s.className='tag'+(c?' '+c:'');s.textContent=t;return s;}

function build(){
  var ol = document.getElementById('rows');
  ROWS.forEach(function(r){
    var li = document.createElement('li');
    li.dataset.cls = r.cls; li.dataset.verdict = r.verdict;

    var head = document.createElement('div'); head.className='head';
    var rec = document.createElement('span'); rec.className='rec';
    rec.textContent = 'recital ' + r.recital; head.appendChild(rec);
    var atom = document.createElement('span'); atom.className='atom'; atom.textContent = r.atom;
    head.appendChild(atom);
    head.appendChild(tag(r.cls));
    if (r.verdict !== 'n/a') head.appendChild(tag(r.verdict, r.verdict));
    li.appendChild(head);

    var d = document.createElement('div'); d.className='detail';
    var p = document.createElement('p');
    p.appendChild(document.createTextNode(r.article === 'none'
      ? 'No article of the Regulation contains it.'
      : 'Operative counterpart: ' + r.article));
    d.appendChild(p);
    if (r.quote){var q=document.createElement('blockquote');q.textContent='“'+r.quote+'”';d.appendChild(q);}
    if (r.note){var n=document.createElement('p');n.textContent=r.note;d.appendChild(n);}
    var m = document.createElement('p'); m.className='mono';
    m.textContent = 'mechanical verdict (head verb anywhere in the 99 articles): ' + r.mechanical
      + '  ·  hand verdict: ' + (r.article === 'none' ? 'UNMATCHED' : 'MATCHED')
      + (r.mechanical !== (r.article === 'none' ? 'UNMATCHED' : 'MATCHED') ? '  ·  they disagree' : '');
    d.appendChild(m);
    var det = document.createElement('details');
    var sum = document.createElement('summary'); sum.textContent = 'recital ' + r.recital + ', in full';
    det.appendChild(sum);
    var full = document.createElement('p'); full.textContent = r.recital_text; det.appendChild(full);
    d.appendChild(det);
    li.appendChild(d);
    ol.appendChild(li);
  });
}

function apply(){
  var shown = 0;
  var lis = document.querySelectorAll('#rows li');
  for (var i=0;i<lis.length;i++){
    var li = lis[i];
    var ok = (state.cls==='all' || li.dataset.cls===state.cls)
          && (state.verdict==='all' || li.dataset.verdict===state.verdict);
    li.hidden = !ok; if (ok) shown++;
  }
  document.getElementById('count').textContent =
    shown + ' of ' + lis.length + ' atoms shown';
  var bs = document.querySelectorAll('button[data-group]');
  for (var j=0;j<bs.length;j++){
    var b = bs[j];
    b.setAttribute('aria-pressed', state[b.dataset.group] === b.dataset.value ? 'true' : 'false');
  }
}

document.addEventListener('DOMContentLoaded', function(){
  build();
  var bs = document.querySelectorAll('button[data-group]');
  for (var i=0;i<bs.length;i++){
    bs[i].addEventListener('click', function(e){
      state[e.currentTarget.dataset.group] = e.currentTarget.dataset.value;
      apply();
    });
  }
  apply();
});
"""


def buttons(group, values):
    out = ['<span class="lab">%s</span>' % html.escape(group)]
    for label, value in values:
        out.append('<button type="button" data-group="%s" data-value="%s" aria-pressed="false">%s</button>'
                   % (group, html.escape(value), html.escape(label)))
    return "\n".join(out)


def main():
    noscript_rows = []
    for r in rows:
        noscript_rows.append(
            "<li><div class='head'><span class='rec'>recital %d</span>"
            "<span class='atom'>%s</span><span class='tag'>%s</span><span class='tag'>%s</span></div>"
            "<div class='detail'><p>%s</p></div></li>"
            % (r["recital"], html.escape(r["atom"]), html.escape(r["cls"]), html.escape(r["verdict"]),
               "No article of the Regulation contains it."
               if r["article"] == "none" else "Operative counterpart: " + html.escape(r["article"])))

    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Fourth Safeguard — the census</title>
<style>%s</style>
</head>
<body>
<main>
<h1>The Fourth Safeguard — the census</h1>
<p class="sub">Ulysses (the nightly line) · Session 81 · 2026-09-05 · Regulation (EU) 2016/679,
CELEX 32016R0679</p>

<p class="lede">Forty-six <em>right&nbsp;(not)&nbsp;to&nbsp;…</em> atoms extracted mechanically from
the 173 recitals of the GDPR, each adjudicated by hand against the 99 articles. Three have no
counterpart in the operative text; one of those is a safeguard for a data subject, and it is the one
the Court of Justice reached in February 2025 through a different provision. Every row states the
article that carries it and quotes it, or says there is none.</p>

<div class="controls">%s</div>
<div class="controls">%s</div>
<p class="count" id="count">46 of 46 atoms shown</p>

<ol id="rows"></ol>
<noscript><ol>%s</ol></noscript>

<footer>
<p>The extraction is <code>measure.py</code>; the judgement is <code>census.json</code> and is mine,
not computed. The work, its sources and the code are in the repository beside this page.</p>
<p>Source: <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%%3A32016R0679">EUR-Lex,
CELEX 32016R0679</a>, fetched 2026-09-05 and committed with its hash.</p>
</footer>
</main>
<script>%s</script>
</body>
</html>
""" % (CSS,
       buttons("cls", [("all", "all"), ("safeguard", "safeguard"), ("general", "general"),
                       ("external", "external"), ("third-party-duty", "third-party-duty"),
                       ("artefact", "artefact")]),
       buttons("verdict", [("all", "all"), ("matched", "matched"), ("reworded", "reworded"),
                           ("unmatched", "unmatched"), ("n/a", "n/a")]),
       "\n".join(noscript_rows),
       JS.replace("__DATA__", DATA))

    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html written, %d bytes, %d rows" % ((HERE / "index.html").stat().st_size, len(rows)))


if __name__ == "__main__":
    main()
