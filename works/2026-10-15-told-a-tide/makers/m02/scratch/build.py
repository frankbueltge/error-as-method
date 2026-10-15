pix=open('/tmp/claude-0/s128/mk/m02/scratch/pix.txt').read()
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixty-One Turns</title>
<style>
:root{--paper:#f2eee5;--ink:#2a2723;--faint:#8a8378}
html,body{margin:0;height:100%;background:var(--paper)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
#w{position:relative;width:1100px;height:800px;flex:none}
canvas{position:absolute;left:0;top:0;width:1100px;height:800px}
.t{position:absolute;left:56px;top:48px;font:italic 15px/1.4 Georgia,'Times New Roman',serif;color:var(--ink);letter-spacing:.02em}
.t span{display:block;font-style:normal;font-size:11px;color:var(--faint);letter-spacing:.12em;text-transform:uppercase;margin-top:4px}
</style></head><body>
<div id="w"><canvas id="c" width="2200" height="1600"></canvas>
<div class="t">Sixty-One Turns<span>1,464 hours wound on one day</span></div></div>
<script>
const P="__PIX__";
const W=300,H=90,X0=2.5,HPP=1463/294,LOW=18.04;
const ink=new Float32Array(W*H);
for(let i=0;i<W*H;i++)ink[i]=parseInt(P[i],16)/15;
const cv=document.getElementById('c'),g=cv.getContext('2d');
g.scale(2,2);
g.fillStyle='#f2eee5';g.fillRect(0,0,1100,800);
// colour by elapsed fraction of the record: blue-black at the start, rust at the end
const A=[28,44,74],B=[138,52,30];
function col(f,a){return `rgba(${A.map((v,i)=>Math.round(v+(B[i]-v)*f)).join(',')},${a})`}
const CX=550,CY=350,RIN=24,K=3.25;
const rad=y=>RIN+(85-y)*K;
// faint guide rings: the highest and lowest levels reached
g.lineWidth=0.6;g.strokeStyle='rgba(120,110,95,.25)';
g.beginPath();g.arc(CX,CY,292,0,Math.PI*2);g.stroke();
g.fillStyle='rgba(120,110,95,.5)';g.beginPath();g.arc(CX,CY,1.6,0,Math.PI*2);g.fill();
// wind: each image column holds ~5 consecutive hours; its ink is laid along that span of the dial
g.globalCompositeOperation='multiply';
const SUB=[-.5,-.3,-.1,.1,.3,.5],WT=[.45,.85,1,1,.85,.45];
// median level of each column, then a 24-hour (5-column) running median of that: the slow swell
const med=new Float32Array(W);
for(let x=0;x<W;x++){let s=0;for(let y=0;y<H;y++)s+=ink[y*W+x];let a=0;for(let y=0;y<H;y++){a+=ink[y*W+x];if(a>=s/2){med[x]=y;break}}}
const swell=new Float32Array(W);
for(let x=0;x<W;x++){const w=[];for(let k=-2;k<=2;k++){const j=Math.min(W-1,Math.max(0,x+k));w.push(med[j])}w.sort((a,b)=>a-b);swell[x]=w[2]}
const base=[...swell].sort((a,b)=>a-b)[W>>1];
for(let x=0;x<W;x++){
  const tc=(x-X0)*HPP, f=Math.min(1,Math.max(0,tc/1463));
  for(let y=0;y<H;y++){
    const v=ink[y*W+x]; if(v<=0)continue;
    const r=rad(y-(swell[x]-base)); if(r<6||r>290)continue; g.lineWidth=K*1.05;
    for(let s=0;s<SUB.length;s++){
      const t=tc+SUB[s]*HPP, a0=((t-LOW)/24)*Math.PI*2+Math.PI/2, da=(.22*HPP/24)*Math.PI*2;
      g.strokeStyle=col(f,(v*.06*WT[s]).toFixed(4));
      g.beginPath();g.arc(CX,CY,r,a0-da/2,a0+da/2);g.stroke();
    }
  }
}
// the record unwound, as given, beneath
const SX=60,SY=676,SW=980,sx=SW/294,sy=1.0;
for(let x=0;x<W;x++){
  const f=Math.min(1,Math.max(0,(x-X0)*HPP/1463));
  for(let y=0;y<H;y++){
    const v=ink[y*W+x]; if(v<=0)continue;
    g.fillStyle=col(f,(v*.8).toFixed(3));
    g.beginPath();g.arc(SX+(x-X0)*sx,SY+y*sy,1.25,0,Math.PI*2);g.fill();
  }
}
// day marks: one tick per 24 hours under the strip
g.globalCompositeOperation='source-over';
g.fillStyle='rgba(120,110,95,.45)';
for(let d=0;d<=61;d++){const xx=SX+(d*24/HPP)*sx;g.fillRect(xx-.3,SY+94,.6,4)}
</script></body></html>'''
open('/tmp/claude-0/s128/mk/m02/work/index.html','w').write(html.replace('__PIX__',pix))
