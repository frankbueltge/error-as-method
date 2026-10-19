import json
v=json.load(open('/tmp/claude-0/s137/mk/m07/scratch/series.json'))
data=",".join(str(int(round(x*1000))) for x in v)
html=r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-one Nights</title>
<style>
:root{--bg:#0c0e12;--ink:#d9d2c3;--dim:#7d7a73;--faint:#3a3d44}
html,body{margin:0;height:100%;background:var(--bg)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden;
font-family:Georgia,"Iowan Old Style","Times New Roman",serif;color:var(--ink)}
.stage{position:relative;width:1100px;height:800px;flex:none}
canvas{position:absolute;left:0;top:0}
.side{position:absolute;left:820px;top:96px;width:240px}
h1{font-weight:normal;font-size:30px;line-height:1.1;margin:0 0 6px;letter-spacing:.01em}
.dates{font-size:13px;color:var(--dim);letter-spacing:.08em;text-transform:uppercase;margin-bottom:28px}
p{font-size:13.5px;line-height:1.55;color:#a9a497;margin:0 0 14px}
.key{position:absolute;left:820px;top:560px;width:240px;font-size:11px;color:var(--dim);letter-spacing:.06em}
.ramp{height:8px;margin:6px 0 4px;border-radius:1px}
.row{display:flex;justify-content:space-between}
</style></head><body>
<div class="stage">
<canvas id="c" width="1100" height="800"></canvas>
<div class="side">
<h1>Sixty-one Nights</h1>
<div class="dates">15 Jan &ndash; 16 Mar 2025</div>
<p>One turn of the coil is one day of the record, read from the outer edge inward. The top of the circle is the same hour every day.</p>
<p>For six weeks something is filled each evening and drains away by the next afternoon, always at the same hours. Late in February it is not filled again, and what remains settles lower than any afternoon before.</p>
</div>
<div class="key">
<div class="row"><span>LOWER</span><span>HIGHER</span></div>
<div class="ramp" id="ramp"></div>
<div style="margin-top:22px">THE RECORD, LEFT TO RIGHT</div>
<canvas id="strip" width="240" height="56" style="position:static;display:block;margin-top:8px"></canvas>
</div>
</div>
<script>
const V=[__DATA__].map(x=>x/1000), N=V.length;
const stops=[[0,[19,23,31]],[0.14,[32,41,56]],[0.3,[52,52,78]],[0.44,[112,48,58]],[0.58,[184,74,42]],[0.76,[232,146,66]],[1,[252,236,204]]];
function col(v){v=Math.max(0,Math.min(1,v));for(let i=1;i<stops.length;i++){if(v<=stops[i][0]){const a=stops[i-1],b=stops[i],f=(v-a[0])/(b[0]-a[0]);return a[1].map((c,k)=>Math.round(c+(b[1][k]-c)*f));}}return stops[stops.length-1][1];}
const css=c=>`rgb(${c[0]},${c[1]},${c[2]})`;
function val(t){const i=Math.floor(t),f=t-i;if(i>=N-1)return V[N-1];if(i<0)return V[0];return V[i]*(1-f)+V[i+1]*f;}
const cv=document.getElementById('c'),dpr=Math.max(1,window.devicePixelRatio||1);
cv.width=1100*dpr;cv.height=800*dpr;cv.style.width='1100px';cv.style.height='800px';
const g=cv.getContext('2d');g.scale(dpr,dpr);
const cx=405,cy=400,R0=338,R1=30,turns=N/24,dr=(R0-R1)/turns;
const ang=t=>(t%24)/24*Math.PI*2-Math.PI/2;
const rad=t=>R0-t/24*dr;
// faint hour guides
g.strokeStyle='rgba(217,210,195,0.18)';g.lineWidth=1;
g.fillStyle='rgba(217,210,195,0.38)';g.font='11px Georgia,serif';g.textAlign='center';g.textBaseline='middle';
for(let h=0;h<24;h++){const a=h/24*Math.PI*2-Math.PI/2,r1=R0+6,r2=R0+(h%6?9:14);
g.beginPath();g.moveTo(cx+Math.cos(a)*r1,cy+Math.sin(a)*r1);g.lineTo(cx+Math.cos(a)*r2,cy+Math.sin(a)*r2);g.stroke();
if(h%6===0){const r3=R0+25;g.fillText(String(h).padStart(2,'0')+':00',cx+Math.cos(a)*r3,cy+Math.sin(a)*r3);}}
// the coil
const SUB=6,gap=0.7;
for(let i=0;i<N;i++){for(let s=0;s<SUB;s++){
 const t0=i+s/SUB,t1=i+(s+1)/SUB+0.02;
 const a0=ang(t0),a1=ang(t0)+(t1-t0)/24*Math.PI*2;
 const ro0=rad(t0),ro1=rad(t1),ri0=ro0-dr+gap,ri1=ro1-dr+gap;
 g.beginPath();
 g.moveTo(cx+Math.cos(a0)*ro0,cy+Math.sin(a0)*ro0);
 g.lineTo(cx+Math.cos(a1)*ro1,cy+Math.sin(a1)*ro1);
 g.lineTo(cx+Math.cos(a1)*ri1,cy+Math.sin(a1)*ri1);
 g.lineTo(cx+Math.cos(a0)*ri0,cy+Math.sin(a0)*ri0);
 g.closePath();g.fillStyle=css(col(val(t0+0.5/SUB)));g.fill();}}
// month marks: 1 Feb (day 17), 1 Mar (day 45), and the last filling (~day 42)
function mark(day,label,side){const t=day*24,r=rad(t)-dr/2,a=ang(t);
 g.strokeStyle='rgba(217,210,195,0.55)';g.lineWidth=1;
 const x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r;
 g.beginPath();g.arc(x,y,1.6,0,Math.PI*2);g.fillStyle='rgba(240,232,215,0.9)';g.fill();
 const lx=x+side*Math.max(26,(R0-r)+40);g.beginPath();g.moveTo(x+side*4,y);g.lineTo(lx-side*4,y);g.stroke();
 g.fillStyle='rgba(217,210,195,0.7)';g.textAlign=side>0?'left':'right';g.font='11px Georgia,serif';g.fillText(label,lx,y);}
{const r=rad(0)-dr/2;g.beginPath();g.arc(cx,cy-r,1.6,0,Math.PI*2);g.fillStyle='rgba(240,232,215,0.9)';g.fill();g.strokeStyle='rgba(217,210,195,0.45)';g.beginPath();g.moveTo(cx+3,cy-r-2);g.lineTo(cx+30,cy-R0-16);g.stroke();g.fillStyle='rgba(217,210,195,0.7)';g.textAlign='left';g.font='11px Georgia,serif';g.fillText('15 Jan',cx+34,cy-R0-17);}
{const t=N-1,r=rad(t)-dr/2,a=ang(t);g.beginPath();g.arc(cx+Math.cos(a)*r,cy+Math.sin(a)*r,1.6,0,Math.PI*2);g.fillStyle='rgba(240,232,215,0.9)';g.fill();g.fillStyle='rgba(217,210,195,0.7)';g.textAlign='center';g.font='11px Georgia,serif';g.fillText('16 Mar',cx,cy);}
// ramp + strip
const rp=document.getElementById('ramp');rp.style.background='linear-gradient(90deg,'+stops.map(s=>css(s[1])+' '+(s[0]*100)+'%').join(',')+')';
const sc=document.getElementById('strip');sc.width=240*dpr;sc.height=56*dpr;sc.style.width='240px';sc.style.height='56px';
const sg=sc.getContext('2d');sg.scale(dpr,dpr);
for(let i=0;i<N;i++){const x=i/(N-1)*238+1,y=54-V[i]*52;sg.fillStyle=css(col(V[i]));sg.fillRect(x-0.5,y-0.5,1.1,1.1);}
</script></body></html>"""
open('/tmp/claude-0/s137/mk/m07/work/index.html','w').write(html.replace('__DATA__',data))
