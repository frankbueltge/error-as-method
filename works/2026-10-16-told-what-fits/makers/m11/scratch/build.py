import json
s=json.load(open('series.json'))
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Breaths</title>
<style>
:root{--paper:#f3eee4;--ink:#2b2118;--faint:#8a7b68}
html,body{margin:0;height:100%;background:var(--paper)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
svg{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}
text{font-family:Georgia,'Times New Roman',serif;fill:var(--ink)}
</style></head><body>
<svg id="w" viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg" role="img"
 aria-label="Sixty-one daily rings of a tree trunk's radius, drawn as a cross-section"></svg>
<script>
const S=__DATA__;
const NS="http://www.w3.org/2000/svg", svg=document.getElementById('w');
const cx=550, cy=392, R0=62, K=3.45;            // radius = R0 + K * measured value (exaggerated)
const el=(n,a)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);svg.appendChild(e);return e};
const pt=i=>{const a=2*Math.PI*(i/24)-Math.PI/2, r=R0+K*S[i];return [cx+r*Math.cos(a), cy+r*Math.sin(a)]};
// pith and a hairline for the first hour of each day
el('circle',{cx,cy,r:3,fill:'#2b2118'});
el('line',{x1:cx,y1:cy-R0+8,x2:cx,y2:cy-372,stroke:'#8a7b68','stroke-width':.5,'stroke-dasharray':'2 4'});
// one ring per day, older days paler, the last days darkest
const lerp=(a,b,t)=>a+(b-a)*t;
for(let d=0; d<61; d++){
  const t=d/60, from=d*24, to=Math.min(S.length-1,d*24+24);
  // Catmull-Rom through the hourly points, so a day reads as a continuous breath
  const P=[];for(let i=Math.max(0,from-1);i<=Math.min(S.length-1,to+1);i++)P.push(pt(i));
  const o=from>0?1:0, n=to-from; let p='M'+P[o][0].toFixed(1)+' '+P[o][1].toFixed(1);
  for(let j=o;j<o+n;j++){const a=P[Math.max(0,j-1)],b=P[j],c=P[j+1],e=P[Math.min(P.length-1,j+2)];
    p+='C'+(b[0]+(c[0]-a[0])/6).toFixed(1)+' '+(b[1]+(c[1]-a[1])/6).toFixed(1)+' '+(c[0]-(e[0]-b[0])/6).toFixed(1)+' '+(c[1]-(e[1]-b[1])/6).toFixed(1)+' '+c[0].toFixed(1)+' '+c[1].toFixed(1)}
  const col=`rgb(${lerp(201,38,t)|0},${lerp(138,28,t)|0},${lerp(72,22,t)|0})`;
  el('path',{d:p,fill:'none',stroke:col,'stroke-width':lerp(.55,1.05,t),'stroke-opacity':lerp(.75,.9,t),'stroke-linejoin':'round'});
}
// one dot per hour, as in the record
for(let i=0;i<S.length;i++){const [x,y]=pt(i),t=i/(S.length-1);
  el('circle',{cx:x.toFixed(1),cy:y.toFixed(1),r:.9,fill:`rgba(43,33,24,${(.18+.5*t).toFixed(2)})`});}
const tx=(x,y,s,txt,o={})=>{const e=el('text',Object.assign({x,y,'font-size':s},o));e.textContent=txt;return e};
tx(48,738,26,'Sixty-One Breaths',{'font-style':'italic'});
tx(48,764,13,'The radius of one tree trunk, hourly, for 61 days. One turn = one day; distance from centre = radius (greatly exaggerated).',{fill:'#5e5142'});
tx(1052,738,12,'pale: first days',{'text-anchor':'end',fill:'#c98a48'});
tx(1052,756,12,'dark: last days',{'text-anchor':'end',fill:'#2b2118'});
tx(1052,774,12,'dotted line: first hour of each day',{'text-anchor':'end',fill:'#8a7b68'});
</script></body></html>'''
open('/tmp/claude-0/s131/mk/m11/work/index.html','w').write(html.replace('__DATA__',json.dumps(s,separators=(',',':'))))
