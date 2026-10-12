import json
s=json.load(open('/tmp/claude-0/s122/mk/m02/scratch/series.json'))
v=[round(333+x,1) for x in s['v']]   # height above lowest drawn pixel
data=json.dumps(v,separators=(',',':')); miss=json.dumps(s['missing'])
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Held to the Moon</title>
<style>
:root{--paper:#efece4;--ink:#1d2430;--soft:#8a8f96}
html,body{margin:0;height:100%;background:var(--paper)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
canvas{display:block}
</style></head><body>
<canvas id="c" width="1100" height="800" aria-label="Sixty lunar days of hourly values stacked as ridgelines; two ridges of high water run straight down the page, swelling and thinning, and near the bottom one tide climbs high over the rows above it."></canvas>
<script>
const V=__DATA__, MISS=new Set(__MISS__);
const L=24.8412;            // one lunar day in hours
const T0=6.0-L;             // phase chosen so the two high waters sit at a quarter and three quarters
const W=1100,H=800, X0=150, X1=950, TOP=150, ROWH=9.9, S=0.42;
const rows=Math.ceil((V.length-1-T0)/L);
const c=document.getElementById('c'), dpr=Math.max(1,window.devicePixelRatio||1);
c.width=W*dpr;c.height=H*dpr;c.style.width=W+'px';c.style.height=H+'px';
const g=c.getContext('2d');g.scale(dpr,dpr);
const css=getComputedStyle(document.documentElement);
const PAPER=css.getPropertyValue('--paper').trim(), INK=css.getPropertyValue('--ink').trim(), SOFT=css.getPropertyValue('--soft').trim();
g.fillStyle=PAPER;g.fillRect(0,0,W,H);
const base=V.slice().sort((a,b)=>a-b)[Math.floor(V.length*0.5)]; // median level = row baseline
const xOf=t=>X0+(X1-X0)*((t-T0)%L)/L;
for(let k=0;k<rows;k++){
  const y0=TOP+k*ROWH;
  const a=Math.max(0,Math.floor(T0+k*L)), b=Math.min(V.length-1,Math.ceil(T0+(k+1)*L));
  const pts=[];
  for(let t=a;t<=b;t++){const x=X0+(X1-X0)*(t-(T0+k*L))/L;pts.push([x,y0-(V[t]-base)*S,t]);}
  if(pts.length<2)continue;
  // clip to the row's lunar day so neighbouring rows meet edge to edge
  g.save();g.beginPath();g.rect(X0,0,X1-X0,H);g.clip();
  const path=new Path2D();path.moveTo(pts[0][0],pts[0][1]);
  for(let i=0;i<pts.length-1;i++){
    const p0=pts[Math.max(0,i-1)],p1=pts[i],p2=pts[i+1],p3=pts[Math.min(pts.length-1,i+2)];
    path.bezierCurveTo(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6,p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6,p2[0],p2[1]);
  }
  const fill=new Path2D(path);
  fill.lineTo(pts[pts.length-1][0],y0+ROWH*4);fill.lineTo(pts[0][0],y0+ROWH*4);fill.closePath();
  g.fillStyle=PAPER;g.fill(fill);
  g.lineWidth=1.05;g.strokeStyle=INK;g.lineJoin='round';g.stroke(path);
  // one grain per hour, as in the record; hours hidden in the source are left open
  for(const [x,y,t] of pts){
    if(x<X0-0.5||x>X1+0.5)continue;
    g.beginPath();g.arc(x,y,MISS.has(t)?1.3:1.25,0,2*Math.PI);
    if(MISS.has(t)){g.fillStyle=PAPER;g.fill();g.lineWidth=0.7;g.strokeStyle=INK;g.stroke();}
    else{g.fillStyle=INK;g.fill();}
  }
  g.restore();
}
// quiet marginalia
g.fillStyle=INK;g.font='italic 20px Georgia, "Times New Roman", serif';g.textBaseline='alphabetic';
g.fillText('Held to the Moon',X0,58);
g.fillStyle=SOFT;g.font='12px Georgia, "Times New Roman", serif';
g.fillText('1,464 hourly values, cut into lengths of 24 h 50 min, one lunar day per line, read downward',X0,80);
g.textAlign='right';
g.fillText('first hour',X0-14,TOP+3);
g.fillText('last hour',X0-14,TOP+(rows-1)*ROWH+3);
</script></body></html>'''
open('/tmp/claude-0/s122/mk/m02/work/index.html','w').write(html.replace('__DATA__',data).replace('__MISS__',miss))
