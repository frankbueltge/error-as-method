import json
d=json.load(open('data.json'))
days=d['days']; env=d['env']; half=d['half']
data={'days':days,'env':[round(e,2) for e in env],'half':[round(h,2) for h in half]}
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixty-One Days Exposure</title>
<style>
:root{--bg:#07070c}
html,body{margin:0;height:100%;background:var(--bg)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
canvas{display:block;width:min(100vw,137.5vh);height:auto;aspect-ratio:1100/800}
</style></head><body>
<canvas id="c" width="2200" height="1600" aria-label="Sixty-one nested arcs of light over a dark horizon, one for each day of sunlight measured"></canvas>
<script>
const DATA=__DATA__;
const c=document.getElementById('c'),g=c.getContext('2d');
g.scale(2,2);
const W=1100,H=800,HZ=640,CX=550,KX=60,TOP=560,VMAX=78;
// sky: dark, a faint warmth near the horizon
let sky=g.createLinearGradient(0,0,0,HZ);
sky.addColorStop(0,'#04050b');sky.addColorStop(0.55,'#080810');sky.addColorStop(1,'#120e0d');
g.fillStyle=sky;g.fillRect(0,0,W,HZ);
let gr=g.createLinearGradient(0,HZ,0,H);
gr.addColorStop(0,'#0c0a09');gr.addColorStop(1,'#030303');
g.fillStyle=gr;g.fillRect(0,HZ,W,H-HZ);
// sun path for a day: standard sin(elevation) form, cos(h)-cos(H0)
const w=Math.PI/12;
function pos(day,t){
  const T=DATA.half[day]+1.2, e0=DATA.env[1], e1=DATA.env[DATA.env.length-2];
  const A=260+(TOP-260)*(DATA.env[day]-e1)/(e0-e1);
  const e=(Math.cos(w*t)-Math.cos(w*T))/(1-Math.cos(w*T));
  return [CX+t*KX, HZ-A*Math.max(e,0)];
}
function val(pts,t){
  if(!pts.length||t<pts[0][0]||t>pts[pts.length-1][0])return null;
  for(let i=1;i<pts.length;i++){if(t<=pts[i][0]){const[a,va]=pts[i-1],[b,vb]=pts[i];const f=b>a?(t-a)/(b-a):0;return va+(vb-va)*f;}}
  return pts[pts.length-1][1];
}
function col(I,a){ // deep ember -> amber -> pale gold
  const r=Math.round(120+135*Math.min(1,I*1.4)), gg=Math.round(25+225*Math.pow(I,1.6)), b=Math.round(15+200*Math.pow(I,4));
  return `rgba(${r},${gg},${b},${a})`;
}
g.globalCompositeOperation='lighter';
g.lineCap='butt';
const n=DATA.days.length;
for(let pass=0;pass<2;pass++){
 for(let d=0;d<n;d++){
  const T=DATA.half[d]+1.2;
  let pts=DATA.days[d].slice();
  // full days fall to zero at the horizon; the two cut days stop where the record stops
  if(d>0&&d<n-1){ if(pts[0][0]>-T)pts.unshift([-T,0]); if(pts[pts.length-1][0]<T)pts.push([T,0]); }
  for(let t=-T;t<T;t+=0.1){
    const v0=val(pts,t),v1=val(pts,t+0.1); if(v0==null||v1==null)continue;
    const I=Math.max(0,(v0+v1)/2/VMAX); if(I<0.01)continue;
    const p=pos(d,t),q=pos(d,t+0.1);
    if(p[1]>=HZ-0.2&&q[1]>=HZ-0.2)continue;
    g.beginPath();g.moveTo(p[0],p[1]);g.lineTo(q[0],q[1]);
    if(pass==0){g.lineWidth=12;g.strokeStyle=col(I,0.05*Math.pow(I,4));}
    else{g.lineWidth=0.5+2.4*I*I;g.strokeStyle=col(I,Math.min(1,0.03+1.1*Math.pow(I,2.6)));}
    g.stroke();
  }
 }
}
g.globalCompositeOperation='source-over';
// horizon
g.fillStyle='rgba(255,220,180,0.10)';g.fillRect(0,HZ,W,1);
// grain, seeded
let s=1464;function rnd(){s=(s*16807)%2147483647;return s/2147483647;}
for(let i=0;i<26000;i++){const x=rnd()*W,y=rnd()*H,a=rnd()*0.05;g.fillStyle=`rgba(255,240,225,${a})`;g.fillRect(x,y,0.6,0.6);}
</script></body></html>'''
html=html.replace('__DATA__',json.dumps(data,separators=(',',':')))
open('/tmp/claude-0/s133/mk/m18/work/index.html','w').write(html)
print(len(html))
