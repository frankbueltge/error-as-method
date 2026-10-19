import json
D=json.load(open('data.json'))
days=D['days']
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=1100">
<title>Sixty-One Measures</title>
<style>
html,body{margin:0;background:#efebe2;}
body{width:1100px;height:800px;overflow:hidden;font-family:Georgia,"Times New Roman",serif;color:#2a2724}
canvas{display:block}
</style></head><body>
<canvas id="c" width="1100" height="800"></canvas>
<script>
// Per-day ink profiles read from record.jpg: for each of the 61 days, the darkness
// of the plot summed over that day's ~4.85 pixel columns, row by row (90 rows, top = high).
const DAYS=__DAYS__;
const c=document.getElementById('c'),g=c.getContext('2d');
const dpr=window.devicePixelRatio||1;
c.width=1100*dpr;c.height=800*dpr;c.style.width='1100px';c.style.height='800px';g.scale(dpr,dpr);
const W=1100,H=800,L=78,R=1022,TOP=96,BOT=700,Y0=4,Y1=86;
const N=DAYS.length,step=(R-L)/(N-1);
const ys=v=>TOP+(v-Y0)/(Y1-Y0)*(BOT-TOP);
// smooth a profile onto a fine grid (sub-rows), gaussian sigma in rows
function fine(p,sub,sig){
  const out=[];const n=p.length*sub;
  for(let i=0;i<n;i++){const r=(i+0.5)/sub-0.5;let s=0,ws=0;
    for(let k=Math.max(0,Math.floor(r-3*sig));k<=Math.min(p.length-1,Math.ceil(r+3*sig));k++){
      const w=Math.exp(-((k-r)**2)/(2*sig*sig));s+=w*p[k];ws+=w;}
    out.push(s/ws);}
  return out;}
// equal time per day: every day holds 24 hours, so each profile is normalised to the same area
const SUB=8;
const prof=DAYS.map(p=>{const q=p.map(v=>Math.max(0,v-26));const f=fine(q,SUB,1.35);const a=f.reduce((s,v)=>s+v,0);return f.map(v=>v/a);});
let mx=0;prof.forEach(f=>f.forEach(v=>{if(v>mx)mx=v;}));
const HALF=step*0.5; // widest half-width
// faint thread through each day's median level
const med=prof.map(f=>{let s=0;for(let i=0;i<f.length;i++){s+=f[i];if(s>=0.5)return (i+0.5)/SUB-0.5;}return 0;});
g.strokeStyle='rgba(60,52,44,0.22)';g.lineWidth=1;g.beginPath();
med.forEach((m,d)=>{const x=L+d*step,y=ys(m);d?g.lineTo(x,y):g.moveTo(x,y);});g.stroke();
// the measures
prof.forEach((f,d)=>{
  const cx=L+d*step;
  g.beginPath();
  const pts=[];
  for(let i=0;i<f.length;i++){const w=f[i]/mx*HALF;if(w<0.2)continue;pts.push([ys((i+0.5)/SUB-0.5),w]);}
  if(!pts.length)return;
  g.moveTo(cx,pts[0][0]);
  pts.forEach(([y,w])=>g.lineTo(cx+w+0.35,y));
  for(let j=pts.length-1;j>=0;j--)g.lineTo(cx-pts[j][1]-0.35,pts[j][0]);
  g.closePath();
  g.fillStyle='#221f1c';g.fill();
});
// small marks: week ticks under the ground, first and last date
g.fillStyle='rgba(42,39,36,0.55)';
for(let d=0;d<N;d+=7){g.fillRect(L+d*step-0.5,BOT+34,1,6);}
g.font='italic 13px Georgia,serif';g.fillStyle='#5a534b';
g.textAlign='left';g.fillText('15 October',L-8,BOT+60);
g.textAlign='right';g.fillText('14 December 2025',R+8,BOT+60);
g.textAlign='left';g.font='15px Georgia,serif';g.fillStyle='#2a2724';
g.fillText('Sixty-One Measures',L-8,44);
g.font='italic 12px Georgia,serif';g.fillStyle='#7a7168';
g.fillText('each figure is one day: where the hourly value stood, and how long it stayed there',L+150,44);
</script></body></html>'''
html=html.replace('__DAYS__',json.dumps(days,separators=(',',':')))
open('/tmp/claude-0/s137/mk/m08/work/index.html','w').write(html)
print(len(html))
