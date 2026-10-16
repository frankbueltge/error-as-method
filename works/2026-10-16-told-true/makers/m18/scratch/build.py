import json
ys=json.load(open('ys.json'))
v=[round(90-y,1) for y in ys]
data=json.dumps(v,separators=(',',':'))
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Breaths</title>
<style>
:root{--paper:#f3efe6;--ink:#1d1b18;--faint:#8a8378}
html,body{margin:0;height:100%;background:var(--paper)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
svg{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}
text{font-family:Georgia,"Times New Roman",serif;fill:var(--ink)}
.cap{fill:var(--faint);font-size:11.5px;letter-spacing:.02em}
</style></head><body>
<svg id="s" viewBox="0 0 1100 800" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
<rect width="1100" height="800" fill="#f3efe6"/>
<g id="ridges"></g>
<text x="64" y="86" font-size="26">Sixty-One Breaths</text>
<text class="cap" x="64" y="110">carbon dioxide in the air at one station</text>
<text class="cap" x="64" y="128">one line per day, one point per hour</text>
<text class="cap" x="64" y="742">day 1 at the top, day 61 at the foot.</text>
<text class="cap" x="64" y="760">Heights are relative; the record carried no scale.</text>
</svg>
<script>
const V=__DATA__;
const NS="http://www.w3.org/2000/svg", g=document.getElementById("ridges");
const X0=300, X1=900, TOP=150, BOT=770, D=61, Hh=24, V0=5, K=1.55;
const step=(BOT-TOP)/(D-1), dx=(X1-X0)/(Hh-1);
function path(pts){ // Catmull-Rom to cubic Bezier
  let d="M"+pts[0][0].toFixed(1)+","+pts[0][1].toFixed(1);
  for(let i=0;i<pts.length-1;i++){
    const p0=pts[i-1]||pts[i],p1=pts[i],p2=pts[i+1],p3=pts[i+2]||p2,t=6;
    const c1=[p1[0]+(p2[0]-p0[0])/t,p1[1]+(p2[1]-p0[1])/t];
    const c2=[p2[0]-(p3[0]-p1[0])/t,p2[1]-(p3[1]-p1[1])/t];
    d+="C"+c1.map(n=>n.toFixed(1))+" "+c2.map(n=>n.toFixed(1))+" "+p2[0].toFixed(1)+","+p2[1].toFixed(1);
  }
  return d;
}
function el(n,a){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);g.appendChild(e);return e}
for(let d=0;d<D;d++){
  const base=TOP+d*step, pts=[];
  for(let h=0;h<Hh;h++){const v=V[d*Hh+h];pts.push([X0+h*dx, base-(v-V0)*K]);}
  const line=path(pts);
  el("path",{d:line+"L"+X1+","+(base+3)+"L"+X0+","+(base+3)+"Z",fill:"#f3efe6"});
  el("path",{d:line,fill:"none",stroke:"#1d1b18","stroke-width":1.05,"stroke-linejoin":"round"});
  for(const p of pts) el("circle",{cx:p[0].toFixed(1),cy:p[1].toFixed(1),r:1.35,fill:"#1d1b18"});
}
</script>
</body></html>'''
open('/tmp/claude-0/s130/mk/m18/work/index.html','w').write(html.replace('__DATA__',data))
