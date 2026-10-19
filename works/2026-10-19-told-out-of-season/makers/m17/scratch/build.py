import json
Y=[90-v for v in json.load(open('/tmp/claude-0/s137/mk/m17/scratch/q.json'))]
data=','.join(str(round(v*10)) for v in Y)
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Folded at the Low Hour</title>
<style>
html,body{margin:0;height:100%;background:#efe9dd}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
svg{display:block;width:100vw;height:100vh;max-width:1100px;max-height:800px}
</style></head><body>
<svg id="w" viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg" role="img"
 aria-label="Sixty-one days of an hourly record, cut into one line per day at the daily low point and stacked, first day at the back."></svg>
<script>
// 1,464 hourly values re-traced from the source dot plot, in tenths of a pixel of its height (larger = higher).
const V=[__DATA__].map(v=>v/10);
const NS='http://www.w3.org/2000/svg', svg=document.getElementById('w');
const PAPER='#efe9dd', INK='#1e1c19';
const el=(n,a,p=svg)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e};
el('rect',{x:0,y:0,width:1100,height:800,fill:PAPER});
const OFF=14;                       // each line begins at the hour the daily cycle is lowest
const ROWS=Math.ceil((V.length+24-OFF)/24);
const X0=170, X1=930, TOP=__TOP__, BOT=742, S=__S__, FLOOR=5;
const dx=(X1-X0)/23, gap=(BOT-TOP)/(ROWS-1);
const g=el('g',{});
function path(pts){ // Catmull-Rom through points
  let d='M'+pts[0][0].toFixed(1)+' '+pts[0][1].toFixed(1);
  for(let i=0;i<pts.length-1;i++){
    const p0=pts[Math.max(0,i-1)],p1=pts[i],p2=pts[i+1],p3=pts[Math.min(pts.length-1,i+2)];
    const c1=[p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6],c2=[p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6];
    d+=' C'+c1.map(n=>n.toFixed(1)).join(' ')+' '+c2.map(n=>n.toFixed(1)).join(' ')+' '+p2[0].toFixed(1)+' '+p2[1].toFixed(1);
  }
  return d;
}
for(let r=0;r<ROWS;r++){
  const base=TOP+r*gap, pts=[];
  for(let k=0;k<24;k++){
    const h=r*24-(24-OFF)+k; if(h<0||h>=V.length) continue;
    pts.push([X0+k*dx, base-(V[h]-FLOOR)*S]);
  }
  if(pts.length<2) continue;
  const line=path(pts);
  const xa=pts[0][0], xb=pts[pts.length-1][0];
  el('path',{d:line+` L${xb.toFixed(1)} ${base+40} L${xa.toFixed(1)} ${base+40} Z`,fill:PAPER,stroke:'none'},g);
  el('path',{d:line,fill:'none',stroke:INK,'stroke-width':1.15,'stroke-linejoin':'round','stroke-linecap':'round'},g);
}
// a margin of paper below the last line so the fills do not show
el('rect',{x:0,y:BOT+10,width:1100,height:800-BOT-10,fill:PAPER});
const t=el('text',{x:X0,y:778,fill:INK,'font-family':'Georgia, "Times New Roman", serif','font-size':13,'letter-spacing':'0.4'});
t.textContent='Folded at the Low Hour';
const c=el('text',{x:X1,y:778,fill:'#6d665b','text-anchor':'end','font-family':'Georgia, "Times New Roman", serif','font-size':11.5,'font-style':'italic'});
c.textContent='1,464 hourly readings · one line per day, cut where each day is lowest · first day at the back';
</script>
</body></html>
'''
open('/tmp/claude-0/s137/mk/m17/work/index.html','w').write(html.replace('__DATA__',data))
