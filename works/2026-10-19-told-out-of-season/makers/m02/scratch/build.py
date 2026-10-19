data=open('data.txt').read()
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixty-One Pulses</title>
<style>
:root{--bg:#f3f0e8;--ink:#1f3442;--soft:#8a969b;--faint:#d9d6cc}
html,body{margin:0;background:var(--bg);}
body{display:flex;justify-content:center;align-items:center;min-height:100vh}
svg{display:block;width:100%;max-width:1100px;height:auto}
text{font-family:Georgia,"Times New Roman",serif;fill:var(--ink)}
.s{font-family:Helvetica,Arial,sans-serif;font-size:10.5px;fill:var(--soft);letter-spacing:.06em}
</style></head><body>
<svg id="w" viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg" role="img"
 aria-label="Sixty-one days of hourly readings arranged as a grid of dots, one column per day, followed by the whole record as a single line."></svg>
<script>
const D=[@@DATA@@].map(v=>v/100);
const NS="http://www.w3.org/2000/svg", svg=document.getElementById("w");
function el(n,a,p){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e}
function txt(s,a){const e=el("text",a);e.textContent=s;return e}
const lo=Math.min(...D), hi=Math.max(...D), N=v=>(v-lo)/(hi-lo);
function col(t){ // pale mineral to deep slate-blue
  const a=[205,212,210], b=[24,52,72];
  return "rgb("+a.map((x,i)=>Math.round(x+(b[i]-x)*Math.pow(t,0.8))).join(",")+")";
}
el("rect",{x:0,y:0,width:1100,height:800,fill:"#f3f0e8"});
txt("Sixty-One Pulses",{x:70,y:66,"font-size":26,"font-style":"italic"});
txt("one reading every hour · one column every day",{x:70,y:88,class:"s"});

// grid: 61 days across, 24 hours down
const gx=78, gy=128, px=15.8, py=17.2;
const g=el("g",{});
for(let d=0;d<61;d++){
  for(let h=0;h<24;h++){
    const v=N(D[d*24+h]);
    el("circle",{cx:(gx+d*px).toFixed(1),cy:(gy+h*py).toFixed(1),r:(0.7+6.3*v).toFixed(2),fill:col(v)},g);
  }
}
txt("hour 1",{x:gx-16,y:gy+3.5,class:"s","text-anchor":"end"});
txt("hour 24",{x:gx-16,y:gy+23*py+3.5,class:"s","text-anchor":"end"});
for(const d of [0,9,26,42,60]){
  txt("day "+(d+1),{x:(gx+d*px).toFixed(1),y:gy+23*py+30,class:"s","text-anchor":"middle"});
}

// the whole record, restored to a line
const sx=gx-6, sw=60*px+12, sy0=730, sh=150;
for(let d=0;d<=61;d++){
  const x=sx+sw*d*24/(D.length);
  el("line",{x1:x.toFixed(1),x2:x.toFixed(1),y1:sy0-sh-6,y2:sy0+4,stroke:"#e2ded3","stroke-width":d%7?0.6:1});
}
let p="";
D.forEach((v,i)=>{p+=(i?"L":"M")+(sx+sw*i/(D.length-1)).toFixed(2)+","+(sy0-sh*N(v)).toFixed(2)});
el("path",{d:p,fill:"none",stroke:"#1f3442","stroke-width":0.75,"stroke-linejoin":"round",opacity:.85});
txt("the same 1,464 readings, end to end",{x:sx,y:sy0+28,class:"s"});
txt("values traced back out of a 300 × 90 picture; every height is approximate",{x:sx+sw,y:sy0+28,class:"s","text-anchor":"end"});
</script></body></html>
'''.replace('@@DATA@@',data)
open('../work/index.html','w').write(html)
