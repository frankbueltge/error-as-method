import json
days=json.load(open('days.json'))
data=json.dumps([[round(v,1) for v in q] for q in days],separators=(',',':'))
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixty-One Strings</title>
<style>
:root{--paper:#f2ede3;--ink:#1c1a17;--faint:#8a8378}
html,body{margin:0;height:100%;background:var(--paper)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
svg{display:block;width:100vw;height:100vh;max-width:1100px;max-height:800px}
text{font-family:Georgia,"Times New Roman",serif;fill:var(--faint)}
</style></head><body>
<svg id="w" viewBox="0 0 1100 800" preserveAspectRatio="xMidYMid meet" aria-label="Sixty-one vertical strings hanging from a rail, each threaded with 24 beads"></svg>
<script>
// 61 days x 24 values, estimated from the ink of the source picture:
// each number is a height in source pixels (0 = top of picture = largest value),
// the day's 24 hours sorted from highest to lowest. Hour order within a day is not recoverable.
const DAYS=__DATA__;
const NS="http://www.w3.org/2000/svg",svg=document.getElementById("w");
const el=(t,a,p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e};
const L=70,R=1030,TOP=88,S=7.0,RAIL=78,step=(R-L)/60;
el("rect",{x:0,y:0,width:1100,height:800,fill:"#f2ede3"});
el("line",{x1:L-22,x2:R+22,y1:RAIL,y2:RAIL,stroke:"#1c1a17","stroke-width":2.2,"stroke-linecap":"round"});
const g=el("g",{});
DAYS.forEach((q,d)=>{
  const x=L+d*step, low=TOP+q[q.length-1]*S;
  el("line",{x1:x,x2:x,y1:RAIL,y2:low+7,stroke:"#1c1a17","stroke-width":0.7,"stroke-opacity":0.55},g);
  el("circle",{cx:x,cy:RAIL,r:1.6,fill:"#1c1a17"},g);
  q.forEach((v,i)=>{
    el("circle",{cx:x,cy:TOP+v*S,r:3.7,fill:"#1c1a17","fill-opacity":0.62},g);
  });
  el("line",{x1:x-2.2,x2:x+2.2,y1:low+7,y2:low+7,stroke:"#1c1a17","stroke-width":0.9,"stroke-opacity":0.7},g);
});
const t=el("text",{x:L-22,y:772,"font-size":13,"letter-spacing":"0.04em"});
t.textContent="Sixty-One Strings — one string for each day, one bead for each hour, 1,464 in all; on every string the day’s hours are sorted by height, because the picture kept how high each hour stood but not in what order.";
</script>
</body></html>'''
open('/tmp/claude-0/s128/mk/m06/work/index.html','w').write(html.replace('__DATA__',data))
