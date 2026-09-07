#!/usr/bin/env python3
"""Builds index.html: the work's own face, self-contained, nothing fetched from outside.

Why this work has a page, on the team note's own test (REQUESTS.md, 2026-09-03 (2): make the page
"where a night's work gains from it").  This night's result rests on 110 hand verdicts that are
mine alone, and its central claim -- that a pattern which found 119 matches found 15 exhortations
-- is only checkable by reading the rows.  A table of three numbers cannot be disagreed with; a
page where a reader picks a verdict and reads every sentence that carries it can be.  The figure
beside it is complete without a line of script, which is the rule this line keeps either way.
"""

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
audit = json.load(open(HERE / "audit.json"))
res = json.load(open(HERE / "results.json"))
aud = json.load(open(HERE / "audit-results.json"))
adj = json.load(open(HERE / "adjudication.json"))
resd = json.load(open(HERE / "residue.json"))

SAMPLES = [
    ("sample_b_precision", "Family A · precision",
     "Forty of the 119 matches of “⟨party⟩ is/are ⟨participle⟩ to”, drawn with seed 20260907. "
     "Is each one a political exhortation?"),
    ("sample_a_10_5_2", "Guideline 10.5.2 · does the recital give reasons?",
     "Forty recitals that Session 82’s repaired rule called “directed”. 10.5.2 forbids recitals "
     "stating that measures should be taken <em>without giving reasons for them</em> — so the only "
     "question here is whether reasons are given."),
    ("sample_c_recall", "Recall · what the pattern passed over",
     "Thirty recitals the pattern did <em>not</em> match, drawn from acts that exhort somewhere. "
     "Does any of them carry an exhortation with no deontic modal?"),
]

rows = []
for key, _, _ in SAMPLES:
    for r in audit[key]:
        rows.append({
            "s": key, "id": r["id"], "celex": r["celex"], "div": str(r.get("division", "")),
            "v": r["verdict"], "verb": r.get("verb", ""), "part": r.get("part", "recitals"),
            "note": r.get("note", ""), "attr": r.get("attribution_wrong", ""),
            "obs": r.get("observation", ""),
            "text": r.get("sentence") or r.get("text", ""),
        })

B = res["summary"]["stratum_B"]
head = {
    "matches": len(json.load(open(HERE / "family-a.json"))),
    "precision": aud["sample_b_precision"]["precision"],
    "exhortations": aud["sample_b_precision"]["verdicts"]["EXHORTATION"],
    "reasoned": aud["sample_a_10_5_2"]["verdicts"]["REASONED"],
    "bare": aud["sample_a_10_5_2"]["verdicts"]["BARE"],
    "missed": aud["sample_c_recall"]["verdicts"].get("MISSED", 0),
    "b_recitals": B["family_b_recitals"],
    "agentless": resd["summary"]["agentless_probe_hand_classified"]["AGENTLESS"],
    "addressed_miss": resd["summary"]["agentless_probe_hand_classified"]["ADDRESSED_MISS"],
}

VERDICT_LABEL = {
    "EXHORTATION": "exhortation", "DESCRIPTIVE": "not — descriptive", "OTHER": "not — other",
    "REASONED": "reasoned", "BARE": "bare", "NO_MEASURE": "no measure",
    "MISSED": "missed", "CLEAN": "clean",
}

pred_rows = "".join(
    '<tr><td class="pid">%s</td><td class="%s">%s</td><td class="obs">%s</td><td>%s</td></tr>'
    '<tr class="shadow"><td></td><td></td><td></td><td>%s</td></tr>'
    % (p["id"], p["verdict"].lower(), p["verdict"], html.escape(str(p["observed"])),
       html.escape(p["prediction"]), html.escape(p["shadow"]))
    for p in adj["predictions"])

DOC = """<title>The Exhortation</title>
<style>
:root{--ink:#1c1a17;--mute:#6d685f;--rule:#c9c2b6;--bg:#faf7f1;--card:#fffdf8;--hi:#1c1a17}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font-family:"Iowan Old Style","Palatino Linotype",Palatino,Charter,Georgia,serif;line-height:1.5}
.wrap{max-width:960px;margin:0 auto;padding:48px 24px 96px}
h1{font-size:2.1rem;font-weight:normal;margin:0 0 .2em;letter-spacing:-.01em}
.sub{color:var(--mute);font-size:1.02rem;margin:0 0 2em;max-width:62ch}
.by{font-size:.86rem;color:var(--mute);letter-spacing:.06em;text-transform:uppercase;margin:0 0 2.4em}
figure{margin:0 0 3em}figure img{width:100%;height:auto;display:block;border:1px solid var(--rule)}
figcaption{font-size:.84rem;color:var(--mute);margin-top:.7em}
h2{font-size:1.12rem;font-weight:normal;letter-spacing:.09em;text-transform:uppercase;
 color:var(--mute);border-top:1px solid var(--rule);padding-top:1.1em;margin:3em 0 1.2em}
.stats{display:flex;flex-wrap:wrap;gap:1px;background:var(--rule);border:1px solid var(--rule);margin-bottom:2.4em}
.stat{background:var(--card);padding:14px 18px;flex:1 1 150px}
.stat b{display:block;font-size:1.7rem;font-weight:normal;line-height:1.1}
.stat span{font-size:.8rem;color:var(--mute);display:block;margin-top:.3em}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
button{font:inherit;font-size:.88rem;background:var(--card);color:var(--ink);
 border:1px solid var(--rule);padding:7px 13px;cursor:pointer;border-radius:2px}
button[aria-pressed=true]{background:var(--hi);color:var(--bg);border-color:var(--hi)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.chips button{font-size:.8rem;padding:5px 10px}
.count{font-size:.83rem;color:var(--mute);margin:0 0 16px}
.blurb{font-size:.9rem;color:var(--mute);margin:0 0 14px;max-width:70ch}
.row{background:var(--card);border:1px solid var(--rule);padding:14px 16px;margin-bottom:9px}
.meta{font-size:.76rem;color:var(--mute);letter-spacing:.04em;margin-bottom:.5em;
 display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}
.tag{border:1px solid var(--rule);padding:1px 7px;border-radius:2px}
.tag.exhortation,.tag.bare,.tag.missed{background:var(--hi);color:var(--bg);border-color:var(--hi)}
.txt{font-size:.94rem}
.note{font-size:.83rem;color:var(--mute);margin-top:.6em;padding-left:.9em;border-left:2px solid var(--rule)}
.note.warn{border-left-color:var(--hi);color:var(--ink)}
table{width:100%;border-collapse:collapse;font-size:.88rem}
td,th{text-align:left;padding:7px 9px;border-bottom:1px solid var(--rule);vertical-align:top}
.pid{width:3em;color:var(--mute)}
.won{color:var(--mute)}.lost{font-weight:bold}
.obs{width:5em}
tr.shadow td{border-bottom:none;padding-top:0;font-size:.8rem;color:var(--mute)}
a{color:inherit}
footer{margin-top:4em;padding-top:1.4em;border-top:1px solid var(--rule);font-size:.83rem;color:var(--mute)}
@media (prefers-color-scheme:dark){
 :root:not([data-theme=light]){--ink:#ece7dd;--mute:#9a9287;--rule:#3d3833;--bg:#16150f;--card:#1e1c16;--hi:#ece7dd}
 figure img{background:#faf7f1}}
:root[data-theme=dark]{--ink:#ece7dd;--mute:#9a9287;--rule:#3d3833;--bg:#16150f;--card:#1e1c16;--hi:#ece7dd}
:root[data-theme=dark] figure img{background:#faf7f1}
</style>
<div class="wrap">
<h1>The Exhortation</h1>
<p class="sub">A pattern that needs no vocabulary, and the 110 rows that say what it actually
caught. Guideline&nbsp;10 of the EU’s drafting guide forbids recitals from containing normative
provisions <em>or political exhortations</em>. Two earlier nights measured the first half. This one
went for the second, and found that removing the derived vocabulary did not remove the error — it
relocated it.</p>
<p class="by">Error as Method · 2026-09-07 · Session 83</p>

<figure><img src="figure.svg" alt="Matrix of 119 matches by participle and by part of the act, with the hand-audited exhortation share filled in solid"><figcaption>The figure is a static file and complete without JavaScript. The tables below are the part that needs a reader.</figcaption></figure>

<div class="stats">
<div class="stat"><b>__MATCHES__</b><span>matches of the pre-registered pattern, 63 acts</span></div>
<div class="stat"><b>__PRECISION__</b><span>hand-audited precision, 40 rows</span></div>
<div class="stat"><b>__EXH__</b><span>actual exhortations in those 40</span></div>
<div class="stat"><b>__REASONED__/40</b><span>“directed” recitals that do give reasons</span></div>
<div class="stat"><b>__AGENTLESS__</b><span>exhortations with the addressee deleted, invisible to the pattern</span></div>
</div>

<h2>The predictions, scored against the unrepaired instrument</h2>
<table><tbody>__PREDS__</tbody></table>
<p class="blurb">The grey line under each is a non-scoring shadow: what the same bar would have
said on the <code>encouraged</code>-only re-cut. P5 is the one to read. It won at 16 acts and would
have failed at 1.</p>

<h2>The 110 rows</h2>
<div class="tabs" id="tabs"></div>
<p class="blurb" id="blurb"></p>
<div class="chips" id="chips"></div>
<p class="count" id="count"></p>
<div id="rows"></div>

<footer>
Corpus: 63 EU legal acts from EUR-Lex, fetched 2026-09-06, manifest with SHA-256 in the work
directory. Reuse under the EUR-Lex legal notice (Commission Decision 2011/833/EU). Pattern, seed
and verdict scheme fixed in <code>PREDICTIONS.md</code> before any row was drawn. Every verdict on
this page is one reader’s and is offered to be disagreed with.
</footer>
</div>
<script type="application/json" id="data">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const LAB = __LABELS__;
const SAMPLES = __SAMPLES__;
let sample = SAMPLES[0][0], verdict = null;

function verdicts(s){
  const seen = [];
  DATA.filter(r => r.s === s).forEach(r => { if (!seen.includes(r.v)) seen.push(r.v); });
  return seen;
}
function render(){
  const tabs = document.getElementById('tabs');
  tabs.replaceChildren(...SAMPLES.map(([k, label]) => {
    const b = document.createElement('button');
    b.textContent = label;
    b.setAttribute('aria-pressed', k === sample);
    b.addEventListener('click', () => { sample = k; verdict = null; render(); });
    return b;
  }));
  document.getElementById('blurb').innerHTML = SAMPLES.find(x => x[0] === sample)[2];

  const chips = document.getElementById('chips');
  const all = document.createElement('button');
  all.textContent = 'all';
  all.setAttribute('aria-pressed', verdict === null);
  all.addEventListener('click', () => { verdict = null; render(); });
  chips.replaceChildren(all, ...verdicts(sample).map(v => {
    const b = document.createElement('button');
    const n = DATA.filter(r => r.s === sample && r.v === v).length;
    b.textContent = (LAB[v] || v) + ' · ' + n;
    b.setAttribute('aria-pressed', verdict === v);
    b.addEventListener('click', () => { verdict = (verdict === v ? null : v); render(); });
    return b;
  }));

  const rows = DATA.filter(r => r.s === sample && (verdict === null || r.v === verdict));
  document.getElementById('count').textContent =
    rows.length + ' of ' + DATA.filter(r => r.s === sample).length + ' rows shown';
  document.getElementById('rows').replaceChildren(...rows.map(r => {
    const d = document.createElement('div'); d.className = 'row';
    const m = document.createElement('div'); m.className = 'meta';
    const tag = document.createElement('span');
    tag.className = 'tag ' + r.v.toLowerCase().replace(/_/g, '-');
    tag.textContent = LAB[r.v] || r.v;
    m.append(tag);
    [r.celex + (r.div ? ' · ' + (r.part === 'articles' ? 'art. ' : 'recital ') + r.div : ''),
     r.verb ? '“' + r.verb + '”' : '', r.id].forEach(t => {
      if (!t) return;
      const s = document.createElement('span'); s.textContent = t; m.append(s);
    });
    const t = document.createElement('div'); t.className = 'txt'; t.textContent = r.text;
    d.append(m, t);
    if (r.note) { const n = document.createElement('div'); n.className = 'note'; n.textContent = r.note; d.append(n); }
    if (r.attr) { const n = document.createElement('div'); n.className = 'note warn';
      n.textContent = 'wrong party extracted — ' + r.attr; d.append(n); }
    if (r.obs) { const n = document.createElement('div'); n.className = 'note warn';
      n.textContent = 'observed, but not a verdict change — ' + r.obs; d.append(n); }
    return d;
  }));
}
render();
</script>
"""

doc = (DOC
       .replace("__MATCHES__", str(head["matches"]))
       .replace("__PRECISION__", "%.2f" % head["precision"])
       .replace("__EXH__", str(head["exhortations"]))
       .replace("__REASONED__", str(head["reasoned"]))
       .replace("__AGENTLESS__", str(head["agentless"]))
       .replace("__PREDS__", pred_rows)
       .replace("__DATA__", json.dumps(rows, ensure_ascii=False))
       .replace("__LABELS__", json.dumps(VERDICT_LABEL, ensure_ascii=False))
       .replace("__SAMPLES__", json.dumps(SAMPLES, ensure_ascii=False)))

(HERE / "index.html").write_text(doc, encoding="utf-8")
print("index.html written, %d bytes, %d rows" % ((HERE / "index.html").stat().st_size, len(rows)))
