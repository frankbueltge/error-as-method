import json
v=json.load(open('series3.json'))
data=','.join(str(int(round(x*10))) for x in v)
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Breaths</title>
<style>
html,body{margin:0;height:100%;background:#f3f0e9;overflow:hidden}
canvas{display:block;width:100vw;height:100vh}
.cap{position:fixed;left:44px;bottom:38px;font:12px/1.6 Georgia,'Times New Roman',serif;color:#6b665d;letter-spacing:.02em;max-width:270px}
.cap b{display:block;font-weight:normal;font-size:19px;color:#2a2926;letter-spacing:.04em;margin-bottom:6px}
</style></head><body>
<canvas id="c"></canvas>
<div class="cap"><b>Sixty-One Breaths</b>
The air over one place, hour by hour for 61 days: one turn of the line for each day, the first day at the centre.
The line swings outward in the hours when the air is richest and is drawn in when it is leanest.
It thickens and darkens over the days when the whole air stood higher.</div>
<script>
const V=[DATA].map(x=>x/10);
const N=V.length, c=document.getElementById('c'), g=c.getContext('2d');
function draw(){
 const dpr=window.devicePixelRatio||1, W=innerWidth, H=innerHeight;
 c.width=W*dpr; c.height=H*dpr; g.setTransform(dpr,0,0,dpr,0,0);
 g.fillStyle='#f3f0e9'; g.fillRect(0,0,W,H);
 // 24-hour running mean (mirrored at the ends) and departure from it
 const P=[]; for(let i=11;i>=0;i--)P.push(V[i]); P.push(...V); for(let i=N-1;i>=N-12;i--)P.push(V[i]);
 const M=new Array(N);
 for(let i=0;i<N;i++){let s=0;for(let k=0;k<24;k++)s+=P[i+k];M[i]=s/24;}
 const D=V.map((x,i)=>x-M[i]);
 const sm=[...M].sort((a,b)=>a-b), lo=sm[Math.floor(N*.02)], hi=sm[Math.floor(N*.98)];
 const s=Math.min(W/1100,H/800), cx=W*0.56, cy=H/2, R0=68*s, R1=360*s, gd=1.45*s;
 const cr=(A,i,t)=>{const p0=A[Math.max(i-1,0)],p1=A[i],p2=A[i+1],p3=A[Math.min(i+2,N-1)];
   return .5*(2*p1+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t);};
 g.lineCap='round'; g.lineJoin='round';
 let prev=null; const SUB=6;
 for(let i=0;i<N-1;i++)for(let k=0;k<SUB;k++){
   const t=k/SUB, h=(i+t)/24, r=R0+(R1-R0)*h/61+gd*cr(D,i,t), a=2*Math.PI*h-Math.PI/2;
   const p=[cx+r*Math.cos(a),cy+r*Math.sin(a)];
   const q=Math.min(1,Math.max(0,(cr(M,i,t)-lo)/(hi-lo)));
   if(prev){const L=Math.round(205-180*q);
     g.strokeStyle='rgb('+L+','+(L-3)+','+(L-8)+')'; g.lineWidth=(0.55+2.3*q*q)*s;
     g.beginPath(); g.moveTo(prev[0],prev[1]); g.lineTo(p[0],p[1]); g.stroke();}
   prev=p;}
}
draw(); addEventListener('resize',draw);
</script></body></html>'''.replace('DATA',data)
open('/tmp/claude-0/s131/mk/m17/work/index.html','w').write(html)
print(len(html))
