import json
v=json.load(open('vals.json'))
data=','.join(str(round(t*1000)) for t in v)
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixty-one Rounds</title>
<style>
:root{--ground:#f3eee3;--ink:#2b2620;--muted:#7a7064}
html,body{margin:0;height:100%;background:var(--ground)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
.frame{position:relative;width:1100px;height:800px}
canvas{position:absolute;inset:0;width:1100px;height:800px}
.cap{position:absolute;left:64px;bottom:72px;width:250px;font-family:Georgia,'Times New Roman',serif;color:var(--ink)}
.cap h1{font-weight:normal;font-size:30px;letter-spacing:.01em;margin:0 0 14px}
.cap p{font-size:13.5px;line-height:1.55;color:var(--muted);margin:0 0 10px}
.key{display:inline-block;width:18px;height:0;border-top:2px solid;vertical-align:middle;margin-right:6px}
</style></head><body>
<div class="frame">
<canvas id="c" width="1100" height="800" aria-label="Sixty-one daily loops of a tree's trunk radius wound around a 24-hour circle"></canvas>
<div class="cap">
<h1>Sixty-one Rounds</h1>
<p>The radius of one tree, read once an hour for sixty-one days and wound around a single day: one turn of the thread for every day, distance from the centre for the size of the trunk.</p>
<p><span class="key" style="border-color:#a5552f"></span>shrinking &nbsp;&nbsp; <span class="key" style="border-color:#2f6a86"></span>swelling</p>
</div>
</div>
<script>
const V=[DATA].map(x=>x/1000);
const c=document.getElementById('c'),dpr=Math.max(1,window.devicePixelRatio||1);
c.width=1100*dpr;c.height=800*dpr;const g=c.getContext('2d');g.scale(dpr,dpr);
const CX=700,CY=400,R0=62,RS=292;
const pt=(t,r)=>{const a=2*Math.PI*t/24-Math.PI/2,rr=R0+RS*r;return[CX+rr*Math.cos(a),CY+rr*Math.sin(a)]};
// faint hour ticks: one per reading-hour of the day
g.strokeStyle='rgba(43,38,32,0.28)';g.lineWidth=1;
for(let h=0;h<24;h++){const a=2*Math.PI*h/24-Math.PI/2,r1=R0+RS+16,r2=r1+(h%6?5:11);
 g.beginPath();g.moveTo(CX+r1*Math.cos(a),CY+r1*Math.sin(a));g.lineTo(CX+r2*Math.cos(a),CY+r2*Math.sin(a));g.stroke();}
// the thread: Catmull-Rom through hourly values, coloured by direction
const N=V.length,SUB=8;
const cr=(p0,p1,p2,p3,u)=>0.5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u*u+(-p0+3*p1-3*p2+p3)*u*u*u);
g.lineWidth=1.05;g.lineCap='round';
for(let i=0;i<N-1;i++){
 const p0=V[Math.max(0,i-1)],p1=V[i],p2=V[i+1],p3=V[Math.min(N-1,i+2)];
 const up=p2>=p1, flat=Math.abs(p2-p1)<0.004;
 g.strokeStyle=flat?'rgba(70,70,64,0.30)':(up?'rgba(47,106,134,0.42)':'rgba(165,85,47,0.42)');
 g.beginPath();
 for(let k=0;k<=SUB;k++){const u=k/SUB,[x,y]=pt(i+u,cr(p0,p1,p2,p3,u));k?g.lineTo(x,y):g.moveTo(x,y);}
 g.stroke();
}
// the 1,464 readings themselves
g.fillStyle='rgba(43,38,32,0.42)';
for(let i=0;i<N;i++){const[x,y]=pt(i,V[i]);g.beginPath();g.arc(x,y,1.0,0,2*Math.PI);g.fill();}
// first and last reading
const mark=(i,lab,dx)=>{const[x,y]=pt(i,V[i]);g.strokeStyle='rgba(43,38,32,0.8)';g.lineWidth=1;g.beginPath();g.arc(x,y,4.5,0,2*Math.PI);g.stroke();
 g.fillStyle='rgba(43,38,32,0.75)';g.font='italic 12px Georgia,serif';g.fillText(lab,x+dx,y+4);};
mark(0,'first hour',-70);mark(N-1,'last hour',9);
</script>
</body></html>'''
open('/tmp/claude-0/s131/mk/m01/work/index.html','w').write(html.replace('DATA',data))
