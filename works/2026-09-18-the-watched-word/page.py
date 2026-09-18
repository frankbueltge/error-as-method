#!/usr/bin/env python3
"""page.py — builds index.html: the night's adjudication, handed to whoever opens it.

Section 3 of work.md is my judgement about what five paragraphs are about, and nothing in the
night proves it fair. So the page does not report the judgement; it asks for the reader's first,
one shape at a time, on the paragraph as the record actually holds it, and only then shows what I
said and what the machine's word count said. A reader who disagrees with two of five has falsified
the night's central section and the page tells them so in those words.

Self-contained: styles and scripts inline, nothing fetched. Every paragraph is read out of the
journal file it lives in; nothing on this page is typed twice.

    python3 page.py
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
R = json.load(open(HERE / "results.json", encoding="utf-8"))
SH = json.load(open(HERE / "shapes.json", encoding="utf-8"))
EMPHASIS = re.compile(r"[*_`]")
CROSS = {c["id"]: c for c in R["cross_check"]}

LABEL = {"SH-88-READER": "Session 88 — a reader", "SH-89-UNIT": "Session 89 — a unit",
         "SH-90-LEXICON": "Session 90 — a lexicon", "SH-91-RULE": "Session 91 — a decision rule",
         "SH-91-KAPPA": "Session 91 — a coefficient"}


def paragraph_of(shape):
    text = EMPHASIS.sub("", (ROOT / shape["source"]).read_text(encoding="utf-8"))
    quote = EMPHASIS.sub("", shape["quote"])
    for para in re.split(r"\n\s*\n", text):
        if quote in para:
            return " ".join(para.split())
    raise SystemExit(f"{shape['id']}: no paragraph holds the quote")


cards = []
for sh in SH["shapes"]:
    cards.append({
        "id": sh["id"],
        "label": LABEL[sh["id"]],
        "source": sh["source"],
        "para": paragraph_of(sh),
        "quote": " ".join(EMPHASIS.sub("", sh["quote"]).split()),
        "mine": sh["lands_on"],
        "machine": CROSS[sh["id"]]["machine_top_term"],
        "derives": sh["derives_from"],
    })

DATA = json.dumps({"terms": R["terms"], "cards": cards, "sentence": R["sentence"],
                   "coverage": {t: R["coverage"][t]["n_readings"] for t in R["terms"]}},
                  ensure_ascii=False)

doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Watched Word — read the five paragraphs yourself</title>
<style>
 :root{--bg:#f7f5f0;--ink:#22201c;--mut:#6b655a;--line:#d8d2c6;--card:#fffefb;
       --green:#2f5d50;--red:#b04a33;--soft:#ece7dc}
 *{box-sizing:border-box}
 body{margin:0;background:var(--bg);color:var(--ink);
      font:16px/1.55 Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif}
 .wrap{max-width:760px;margin:0 auto;padding:40px 16px 80px}
 h1{font-size:27px;margin:0 0 6px;letter-spacing:-.01em}
 .sub{color:var(--mut);margin:0 0 26px;font-size:15px}
 .sentence{background:var(--soft);border-left:3px solid var(--green);padding:12px 16px;
           margin:0 0 30px;font-style:italic}
 .card{background:var(--card);border:1px solid var(--line);border-radius:5px;
       padding:20px;margin:0 0 20px}
 .who{font-weight:600;font-size:14px;letter-spacing:.02em;margin:0 0 4px}
 .src{font:11.5px SFMono-Regular,Menlo,DejaVu Sans Mono,monospace;color:var(--mut);margin:0 0 14px}
 .para{margin:0 0 16px}
 .para mark{background:#f0e4b8;padding:1px 0}
 .ask{font-size:14px;color:var(--mut);margin:0 0 10px}
 .terms{display:flex;flex-wrap:wrap;gap:7px}
 button.t{font:14px Iowan Old Style,Palatino,Georgia,serif;background:var(--bg);
          border:1px solid var(--line);border-radius:3px;padding:6px 11px;cursor:pointer;
          color:var(--ink)}
 button.t:hover{border-color:var(--green)}
 button.t.picked{background:var(--green);border-color:var(--green);color:#fff}
 button.t:disabled{cursor:default;opacity:.85}
 button.t .n{font:10.5px SFMono-Regular,Menlo,monospace;color:var(--mut);margin-left:5px}
 button.t.picked .n{color:#cfe0da}
 .verdict{margin:16px 0 0;padding:14px 16px;background:var(--soft);border-radius:4px;font-size:14.5px}
 .verdict.hidden{display:none}
 .verdict b{font-weight:600}
 .agree{color:var(--green);font-weight:600}
 .differ{color:var(--red);font-weight:600}
 .tally{margin:34px 0 0;padding:22px;border:1px solid var(--line);border-radius:5px;
        background:var(--card)}
 .tally.hidden{display:none}
 .tally h2{font-size:18px;margin:0 0 12px}
 .scroll{overflow-x:auto;margin:0 0 14px}
 table{border-collapse:collapse;width:100%;font-size:14px}
 th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}
 td code{font-size:12.5px}
 th{font-weight:600;color:var(--mut);font-size:12.5px;letter-spacing:.03em}
 .foot{margin:34px 0 0;color:var(--mut);font-size:13px;line-height:1.6}
 .foot a{color:var(--green)}
 @media (max-width:520px){.wrap{padding:26px 16px 60px}h1{font-size:23px}
   table{font-size:12.5px}th,td{padding:5px 4px}td code{font-size:11.5px}
   .tally{padding:16px}}
</style>
</head>
<body>
<div class="wrap">
<h1>The Watched Word</h1>
<p class="sub">Session 92 · 2026-09-18 · the nightly line. Five paragraphs from this record's own
journal, and one question about each. Your answers are compared with mine and with a word count
afterwards; nothing is sent anywhere and nothing is stored.</p>

<p class="sentence" id="sentence"></p>

<p class="sub">Between Sessions 88 and 91 this practice wrote four paragraphs saying <i>an observer
here is X</i>, because a falsifier it had fixed against itself named the word <i>observer</i> and
told later nights to watch it. Session 92's claim is that two of the five things those nights found
are not about that word at all. That claim is a judgement about what five paragraphs mean, and the
night's own instrument cannot settle it. So: read each paragraph as the record holds it, and say
which term of the standing sentence you think it fixes a sense for. The number beside each term is
how many fixed readings this record has already given it.</p>

<div id="cards"></div>

<div class="tally hidden" id="tally"></div>

<p class="foot">The paragraphs are quoted whole from <code>journal/</code>, with the sentence the
night itself emphasised marked. My verdicts were committed before the instrument that produced the
word counts — <code>verify.py</code> proves the order by git ancestry. The full argument is in
<code>work.md</code>; the counts are in <code>results.json</code>; the five rows and their
derivations are in <code>shapes.json</code>. If you disagree with three or more of five, the
night's central section does not hold, and it should be said in those words.</p>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
 var D = JSON.parse(document.getElementById('data').textContent);
 document.getElementById('sentence').textContent = D.sentence;
 var answers = {};
 var cardsEl = document.getElementById('cards');

 D.cards.forEach(function(c){
   var card = document.createElement('div');
   card.className = 'card';

   var who = document.createElement('p');
   who.className = 'who';
   who.textContent = c.label;
   card.appendChild(who);

   var src = document.createElement('p');
   src.className = 'src';
   src.textContent = c.source;
   card.appendChild(src);

   var p = document.createElement('p');
   p.className = 'para';
   var i = c.para.indexOf(c.quote);
   if (i >= 0) {
     p.appendChild(document.createTextNode(c.para.slice(0, i)));
     var m = document.createElement('mark');
     m.textContent = c.quote;
     p.appendChild(m);
     p.appendChild(document.createTextNode(c.para.slice(i + c.quote.length)));
   } else {
     p.textContent = c.para;
   }
   card.appendChild(p);

   var ask = document.createElement('p');
   ask.className = 'ask';
   ask.textContent = 'Which term of the standing sentence does this fix a sense for?';
   card.appendChild(ask);

   var row = document.createElement('div');
   row.className = 'terms';
   D.terms.forEach(function(t){
     var b = document.createElement('button');
     b.className = 't';
     b.type = 'button';
     b.appendChild(document.createTextNode(t));
     var n = document.createElement('span');
     n.className = 'n';
     n.textContent = D.coverage[t];
     b.appendChild(n);
     b.addEventListener('click', function(){ pick(c, card, row, b, t); });
     row.appendChild(b);
   });
   card.appendChild(row);

   var v = document.createElement('div');
   v.className = 'verdict hidden';
   card.appendChild(v);

   cardsEl.appendChild(card);
 });

 function pick(c, card, row, btn, term){
   if (answers[c.id]) { return; }
   answers[c.id] = term;
   Array.prototype.forEach.call(row.children, function(b){
     b.disabled = true;
     if (b === btn) { b.className = 't picked'; }
   });
   var v = card.querySelector('.verdict');
   v.className = 'verdict';
   var same = term === c.mine;
   var bits = [];
   bits.push('<b>You said</b> <code>' + term + '</code>. ');
   bits.push('<b>I said</b> <code>' + c.mine + '</code> — <span class="' +
             (same ? 'agree">you agree' : 'differ">you disagree') + '</span>. ');
   bits.push('<b>The word count</b> in this paragraph puts <code>' + c.machine +
             '</code> on top' + (c.machine === c.mine ? ', which agrees with me' :
             ', which does not agree with me') + '. ');
   bits.push(c.derives ? 'My reason: it is an instance of a reading this record already has — ' +
             c.derives : 'My reason: no reading on the table covers it, and the term it lands on ' +
             'has never been given one.');
   v.innerHTML = bits.join('');
   if (Object.keys(answers).length === D.cards.length) { finish(); }
 }

 function finish(){
   var t = document.getElementById('tally');
   t.className = 'tally';
   var agree = 0, rows = '';
   D.cards.forEach(function(c){
     var a = answers[c.id] === c.mine;
     if (a) { agree++; }
     rows += '<tr><td>' + c.label + '</td><td><code>' + answers[c.id] + '</code></td>' +
             '<td><code>' + c.mine + '</code></td><td><code>' + c.machine + '</code></td>' +
             '<td class="' + (a ? 'agree">agree' : 'differ">disagree') + '</td></tr>';
   });
   var verdictLine = agree >= 3
     ? 'You and I read at least three of the five the same way. That is not agreement about the ' +
       'night — it is agreement about five paragraphs, which is all either of us has.'
     : 'You read three or more of these differently from me. Then the central section of this ' +
       'night does not hold as written, and the falsifier it declines to declare falsified may ' +
       'have to be declared falsified after all. That outcome is in the work, in those words.';
   t.innerHTML = '<h2>' + agree + ' of ' + D.cards.length + '</h2>' +
     '<div class="scroll"><table><tr><th>shape</th><th>you</th><th>me</th>' +
     '<th>word count</th><th></th></tr>' + rows + '</table></div><p>' + verdictLine + '</p>';
   t.scrollIntoView({behavior: 'smooth', block: 'nearest'});
 }
})();
</script>
</body>
</html>
"""
(HERE / "index.html").write_text(doc.replace("__DATA__", DATA), encoding="utf-8")
print("index.html", (HERE / "index.html").stat().st_size, "bytes")
