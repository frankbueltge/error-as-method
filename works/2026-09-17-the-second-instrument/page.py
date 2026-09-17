#!/usr/bin/env python3
"""page.py -- builds index.html: the reader's job, handed to the reader.

Session 90's page let a visitor write the word list and watch the falsifier move.  Tonight's does
the other half.  The night's finding is that the validation could not be delegated to a rule; so the
page delegates it to whoever opens it.  Forty sentences, one at a time, each with its carrier marked:
is that term the bearer of this obligation?  The visitor answers, and afterwards sees what one reader
said in September 2026, what three declared rules said, and what their own precision figure would
have done to a published number.

Self-contained: inline style and script, no outside fetches, every datum embedded from the committed
files beside it.
"""

import json
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
S90 = HERE.parent / "2026-09-15-not-part-of-the-act"

R = json.load(open(HERE / "results.json"))
ADJ = json.load(open(HERE / "adjudication.json"))
A = R["against_the_reader"]
P = R["over_the_population"]
HAND = {r["n"]: r for r in json.load(open(S90 / "handreading.json"))["rows"]}

DECLARED = ["R1_adjacent_subject", "R2_no_competing_nominal", "R3_active_governor"]
SHORT = {"R1_adjacent_subject": "R1 adjacent subject",
         "R2_no_competing_nominal": "R2 no competing nominal",
         "R3_active_governor": "R3 active governor"}

cards = []
for row in sorted(A["rows"], key=lambda r: r["n"]):
    h = HAND[row["n"]]
    cards.append({
        "n": row["n"], "act": row["act"], "modal": row["modal"],
        "sentence": h["sentence"],
        "carrier": row["carrier"], "dir": row["direction"], "dist": row["word_distance"],
        "reader": row["reader"], "reason": row["reader_reason"],
        "rules": {k: row["rules"][k] for k in DECLARED},
    })

DATA = {
    "cards": cards,
    "reader": {"yes": A["reader_yes"], "no": A["reader_no"], "precision": A["reader_base_rate"]},
    "rules": {k: A["by_rule"][k] for k in DECLARED},
    "short": SHORT,
    "reach": {l: P[l]["session_90_published_reach_pct"] for l in ("base", "narrow", "wide")},
    "in_reach": {l: P[l]["rows_in_reach_at_word_36"] for l in ("base", "narrow", "wide")},
    "s88": 0.611,
    "spans": ADJ["predictions"]["P4"]["numbers"],
}

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Second Instrument &#183; Error as Method</title>
<style>
:root{--bg:#f7f5f0;--ink:#22201c;--dim:#6b655a;--rule:#d8d2c6;--deep:#2f5d50;--warn:#b04a33;--pale:#ece7dc}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font:17px/1.55 Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif}
main{max-width:760px;margin:0 auto;padding:40px 20px 80px}
h1{font-size:30px;line-height:1.2;margin:0 0 6px;font-weight:600}
h2{font-size:18px;margin:38px 0 10px;font-weight:600}
p.lede{color:var(--dim);margin:0 0 26px}
p{margin:0 0 14px}
.card{border:1px solid var(--rule);background:#fff;padding:22px;margin:0 0 18px}
.meta{font:12px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;color:var(--dim);
 margin:0 0 12px;letter-spacing:.02em}
.sent{font-size:18px;line-height:1.6;margin:0 0 18px}
mark{background:#e7dfc9;padding:0 2px;font-weight:600}
mark.m{background:#d9e5e0;padding:0 2px;font-weight:600}
.ask{font-size:15px;color:var(--dim);margin:0 0 12px}
button{font:15px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;background:var(--pale);
 border:1px solid var(--rule);color:var(--ink);padding:9px 18px;cursor:pointer;margin-right:8px}
button:hover{background:#e2dccd}
button:disabled{opacity:.45;cursor:default}
button.go{background:var(--deep);color:#fff;border-color:var(--deep)}
.verdict{border-top:1px solid var(--rule);margin-top:18px;padding-top:16px;font-size:15px}
.verdict.hidden{display:none}
.vrow{display:flex;gap:10px;align-items:baseline;margin:0 0 7px}
.tag{font:11.5px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;color:var(--dim);
 min-width:180px;flex:0 0 180px}
.y{color:var(--deep);font-weight:600}
.n{color:var(--dim)}
.x{color:var(--warn);font-weight:600}
.bar{height:22px;background:var(--pale);border:1px solid var(--rule);position:relative;margin:4px 0 2px}
.bar i{display:block;height:100%;background:var(--deep)}
table{border-collapse:collapse;width:100%;font-size:14.5px;margin:6px 0 16px}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--rule)}
th{font-weight:600;color:var(--dim);font-size:13px}
td.num,th.num{text-align:right;font:13px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace}
.note{font-size:14px;color:var(--dim)}
footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--rule);font-size:13.5px;color:var(--dim)}
a{color:var(--deep)}
@media (prefers-color-scheme:dark){
 :root{--bg:#1b1a18;--ink:#e8e4da;--dim:#9c958a;--rule:#3a3733;--pale:#2a2825;--deep:#8fbfae}
 .card{background:#211f1d}
 mark{background:#4a412c;color:#f2ecdd}
 mark.m{background:#2c403a;color:#e8f0ec}
 button.go{color:#1b1a18}
}
</style>
</head>
<body>
<main>
<h1>The Second Instrument</h1>
<p class="lede">Forty sentences from Acts of Parliament. Each one carries an obligation whose agent
has been deleted &#8212; <em>must be given</em>, <em>shall be published</em> &#8212; and a term for a
party standing near it. A scan that has run for four nights counts that term as evidence the bearer
might be named nearby. The question it never asks is whether the term is actually the bearer. You
answer it forty times, and then find out what one reader and three rules said.</p>

<div id="deck"></div>

<div id="done" style="display:none">
<h2>Your reading</h2>
<div id="summary"></div>
</div>

<footer>
Session 91 &#183; 2026-09-17 &#183; <em>Error as Method</em>. Corpus: 63 UK Public General Acts
2012&#8211;2014, harvested and committed by Session 90 from
<a href="https://www.legislation.gov.uk/">legislation.gov.uk</a> under the Open Government Licence.
The forty verdicts and the three rules are committed beside this page; nothing here is fetched.
</footer>
</main>
<script id="d" type="application/json">__DATA__</script>
<script>
(function(){
var D=JSON.parse(document.getElementById('d').textContent);
var i=0,mine=[],deck=document.getElementById('deck');

function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}

function mark(sent,carrier,modal){
 var h=esc(sent);
 if(carrier){
  var c=esc(carrier);
  h=h.replace(c,'<mark>'+c+'</mark>');
 }
 h=h.replace(new RegExp('\\\\b'+modal+'\\\\b'),'<mark class="m">'+modal+'</mark>');
 return h;
}

function render(){
 if(i>=D.cards.length){deck.innerHTML='';finish();return;}
 var c=D.cards[i];
 deck.innerHTML='';
 var el=document.createElement('div');el.className='card';
 el.innerHTML='<p class="meta">'+(i+1)+' of '+D.cards.length+' &#183; '+esc(c.act)+
  ' &#183; carrier &#8220;'+esc(c.carrier)+'&#8221; stands '+c.dist+' word'+(c.dist===1?'':'s')+' '+
  c.dir+' the modal</p>'+
  '<p class="sent">'+mark(c.sentence,c.carrier,c.modal)+'</p>'+
  '<p class="ask">Is <strong>'+esc(c.carrier)+'</strong> the bearer of this obligation &#8212; '+
  'the one who must act?</p>'+
  '<p><button class="go" data-v="1">Bearer</button>'+
  '<button data-v="0">Not the bearer</button></p>'+
  '<div class="verdict hidden"></div>';
 deck.appendChild(el);
 el.querySelectorAll('button[data-v]').forEach(function(b){
  b.addEventListener('click',function(){answer(el,c,b.getAttribute('data-v')==='1');});
 });
}

function answer(el,c,v){
 mine.push({n:c.n,mine:v,reader:c.reader});
 el.querySelectorAll('button[data-v]').forEach(function(b){b.disabled=true;});
 var d=el.querySelector('.verdict');d.className='verdict';
 var rows='<div class="vrow"><span class="tag">you</span><span class="'+(v?'y':'n')+'">'+
  (v?'bearer':'not the bearer')+'</span></div>'+
  '<div class="vrow"><span class="tag">the reader, Session 90</span><span class="'+
  (c.reader!==v?'x':(c.reader?'y':'n'))+'">'+(c.reader?'bearer':'not the bearer')+'</span></div>'+
  '<div class="vrow"><span class="tag"></span><span class="note">'+esc(c.reason)+'</span></div>';
 Object.keys(D.short).forEach(function(k){
  var f=c.rules[k];
  rows+='<div class="vrow"><span class="tag">'+esc(D.short[k])+'</span><span class="'+
   (f!==c.reader?'x':(f?'y':'n'))+'">'+(f?'fires':'silent')+'</span></div>';
 });
 d.innerHTML=rows+'<p><button class="go" id="nx">Next</button></p>';
 d.querySelector('#nx').addEventListener('click',function(){
  el.querySelector('#nx').disabled=true;i++;render();window.scrollTo(0,0);});
}

function finish(){
 var agree=0,yes=0;
 mine.forEach(function(m){if(m.mine===m.reader)agree++;if(m.mine)yes++;});
 var prec=yes/mine.length;
 var s=document.getElementById('summary');
 var t='<p>You called <strong>'+yes+'</strong> of '+mine.length+' nearby party terms the bearer &#8212; '+
  'a precision of <strong>'+prec.toFixed(3)+'</strong> for the scan\\'s ceiling. '+
  'The reader of Session 90 put it at <strong>'+D.reader.precision.toFixed(3)+
  '</strong> on these same forty rows; the reader of Session 88 put it at <strong>'+
  D.s88.toFixed(3)+'</strong> on a different corpus. You agreed with Session 90 on <strong>'+
  agree+' of '+mine.length+'</strong>.</p>';
 t+='<div class="bar"><i style="width:'+(prec*100).toFixed(1)+'%"></i></div>'+
  '<p class="note">your precision, against a bar whose full width is 1.0</p>';
 t+='<h2>What that would do to a published number</h2>'+
  '<table><tr><th>vocabulary</th><th class="num">rows in reach</th>'+
  '<th class="num">reach published</th><th class="num">&#215; your precision</th></tr>';
 ['base','narrow','wide'].forEach(function(l){
  t+='<tr><td>'+l+'</td><td class="num">'+D.in_reach[l]+'</td><td class="num">'+
   D.reach[l].toFixed(2)+'%</td><td class="num">'+(D.reach[l]*prec).toFixed(2)+'%</td></tr>';
 });
 t+='</table>';
 var sp=(D.reach.wide-D.reach.base)*prec;
 t+='<p>Session 90 published those three figures as they stand: a span of <strong>'+
  D.spans.uncorrected_span_session_90+'</strong> points across three vocabularies one author '+
  'declared in advance, against a falsification band of 20. Multiplying all three by a single '+
  'precision leaves the span at <strong>'+sp.toFixed(2)+'</strong> points &#8212; a flat scaling '+
  'shrinks the interval but cannot close it, because one number applied to all three lists cannot '+
  'know that the lists differ in how often their terms act. That is what the three rules were for, '+
  'and what they could not agree about.</p>';
 t+='<h2>The three rules, on the same forty rows</h2><table>'+
  '<tr><th>rule</th><th class="num">fires</th><th class="num">agrees with the reader</th>'+
  '<th class="num">precision on its own YES</th></tr>';
 Object.keys(D.short).forEach(function(k){
  var r=D.rules[k];
  t+='<tr><td>'+D.short[k]+'</td><td class="num">'+r.fires+'</td><td class="num">'+
   r.agreements+'/40</td><td class="num">'+(r.precision_on_yes===null?'&#8212;':
   r.precision_on_yes.toFixed(3))+'</td></tr>';
 });
 t+='</table><p class="note">Always answering &#8220;not the bearer&#8221; agrees with the reader on '+
  D.reader.no+' of 40. Two of the three declared rules do not beat that.</p>';
 s.innerHTML=t;
 document.getElementById('done').style.display='block';
}

render();
})();
</script>
</body>
</html>
"""

out = HTML.replace("__DATA__", json.dumps(DATA, separators=(",", ":")))
(HERE / "index.html").write_text(out)
print("wrote index.html -- %d bytes, %d cards" % (len(out), len(cards)))
