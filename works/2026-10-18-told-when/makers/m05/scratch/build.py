import json
runs=open('runs.json').read()
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eighteen Rings</title>
<style>
:root{--paper:#f2ede3;--ink:#2a2622;--faint:#8a8178}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--paper:#f2ede3;--ink:#2a2622;--faint:#8a8178}}
:root[data-theme="dark"]{--paper:#f2ede3;--ink:#2a2622;--faint:#8a8178}
html,body{margin:0;height:100%;background:var(--paper);overflow:hidden}
body{font-family:Georgia,"Times New Roman",serif;color:var(--ink)}
canvas{position:absolute;inset:0;width:100vw;height:100vh;display:block}
.t{position:absolute;left:44px;top:40px;max-width:250px}
.t h1{font-weight:normal;font-size:26px;letter-spacing:.02em;margin:0 0 14px}
.t p{font-size:12.5px;line-height:1.55;color:var(--faint);margin:0 0 9px}
.k{position:absolute;left:44px;bottom:40px;font-size:11.5px;color:var(--faint);line-height:1.6}
.k i{display:inline-block;width:120px;height:6px;vertical-align:middle;margin:0 8px;border-radius:3px;
 background:linear-gradient(90deg,#b4532a,#c98a3a,#7d8a6a,#3f6f8f,#283e6b)}
</style></head><body>
<canvas id="c"></canvas>
<div class="t"><h1>Eighteen Rings</h1>
<p>A record of 1,464 hours, one value an hour, wound so that one turn of the circle is one day.</p>
<p>The value only ever took eighteen steps. Each step has its own ring; the highest is outermost. A ring is inked only for the hours the record stood on that step.</p>
<p>Each ring is a coil: day one runs along its outer edge, day sixty-one along its inner edge.</p></div>
<div class="k">first day<i></i>sixty-first day<br>top of the circle: the record&rsquo;s first hour; time runs clockwise</div>
<script>
const RUNS=''' + runs + r''';
const N=1464, LEVELS=18;
const cv=document.getElementById('c'), cx=cv.getContext('2d');
const stops=[[0,[180,83,42]],[.25,[201,138,58]],[.5,[125,138,106]],[.75,[63,111,143]],[1,[40,62,107]]];
function col(f,a){let i=0;while(i<stops.length-2&&f>stops[i+1][0])i++;
 const [f0,c0]=stops[i],[f1,c1]=stops[i+1],u=Math.min(1,Math.max(0,(f-f0)/(f1-f0)));
 return `rgba(${c0.map((v,k)=>Math.round(v+(c1[k]-v)*u)).join(',')},${a})`;}
function draw(){
 const dpr=window.devicePixelRatio||1, W=innerWidth, H=innerHeight;
 cv.width=W*dpr; cv.height=H*dpr; cx.setTransform(dpr,0,0,dpr,0,0);
 cx.fillStyle='#f2ede3'; cx.fillRect(0,0,W,H);
 const R=Math.min(H/2-22, W/2-60), ox=Math.max(R+330, W/2+120)>W-R-30? W-R-40 : W/2+120, oy=H/2;
 const R0=R*0.2, s=(R-R0)/LEVELS;
 const rad=(L,t)=>R0+(LEVELS-L)*s - (t/N)*s*0.92;
 const ang=t=>-Math.PI/2+ (t%24)/24*2*Math.PI;
 // empty coils: where the record could have been
 cx.lineWidth=0.5; cx.strokeStyle='rgba(60,50,40,0.07)';
 for(let L=0;L<LEVELS;L++){cx.beginPath();
  for(let t=0;t<=N;t+=0.25){const r=rad(L,t),a=ang(t);const x=ox+r*Math.cos(a),y=oy+r*Math.sin(a);t?cx.lineTo(x,y):cx.moveTo(x,y);}
  cx.stroke();}
 // ring boundaries, faint
 cx.strokeStyle='rgba(60,50,40,0.10)';cx.lineWidth=0.6;
 for(let L=0;L<=LEVELS;L++){cx.beginPath();cx.arc(ox,oy,R0+(LEVELS-L)*s+0.5,0,2*Math.PI);cx.stroke();}
 // inked hours
 cx.lineCap='round';
 const order=RUNS.slice().sort((p,q)=>p[1]-q[1]);
 for(const [L,a,b] of order){
  const f=((a+b)/2)/N;
  for(const [w,al] of [[3.2,0.10],[1.5,0.85]]){
   cx.lineWidth=w; cx.strokeStyle=col(f,al); cx.beginPath();
   for(let t=a;t<=b+1e-6;t+=0.1){const r=rad(L,t),g=ang(t);const x=ox+r*Math.cos(g),y=oy+r*Math.sin(g);t===a?cx.moveTo(x,y):cx.lineTo(x,y);}
   cx.stroke();}
 }
 // first hour mark
 cx.strokeStyle='rgba(42,38,34,0.55)';cx.lineWidth=1;cx.beginPath();cx.moveTo(ox,oy-R-14);cx.lineTo(ox,oy-R-4);cx.stroke();
 cx.fillStyle='rgba(42,38,34,0.6)';cx.beginPath();cx.arc(ox,oy,1.6,0,7);cx.fill();
}
draw(); addEventListener('resize',draw);
</script></body></html>'''
open('/tmp/claude-0/s135/mk/m05/work/index.html','w').write(html)
