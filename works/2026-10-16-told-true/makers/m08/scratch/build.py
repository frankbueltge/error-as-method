import json
data=open('/tmp/claude-0/s130/mk/m08/scratch/days.json').read()
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Piles</title>
<style>
html,body{margin:0;height:100%;background:#e7e3da}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
canvas{display:block;width:min(100vw,137.5vh);height:auto;max-height:100vh}
</style></head><body>
<canvas id="c" width="2200" height="1600" aria-label="Sixty-one wooden piles in a row, each stained dark from below to the heights the water reached on one day."></canvas>
<script>
const D=__DATA__;
const cv=document.getElementById('c'),g=cv.getContext('2d');
g.scale(2,2);
const Wd=1100,Ht=800;
let s=20240917;function rnd(){s=(s*1664525+1013904223)>>>0;return s/4294967296}
// paper
g.fillStyle='#e7e3da';g.fillRect(0,0,Wd,Ht);
for(let i=0;i<9000;i++){g.fillStyle='rgba(90,80,60,'+(rnd()*0.035)+')';g.fillRect(rnd()*Wd,rnd()*Ht,1,1)}
const N=D.days.length,R=D.days[0].length,r0=D.r0;
const X0=72,X1=1028,pitch=(X1-X0)/N,pw=Math.round(pitch*0.68);
const Y0=58,Y1=716;               // rows r0..r0+R-1 mapped here
const rowY=r=>Y0+(r-r0)/(R-1)*(Y1-Y0);
const yRow=y=>r0+(y-Y0)/(Y1-Y0)*(R-1);
const top=40,bot=752;
function smooth(h){const o=new Array(h.length).fill(0),k=[0.06,0.24,0.4,0.24,0.06];
 for(let i=0;i<h.length;i++)for(let j=-2;j<=2;j++){const t=i+j;if(t>=0&&t<h.length)o[i]+=h[t]*k[j+2]}return o}
const dry=[208,199,183],wet=[22,33,34],mid=[96,108,86];
for(let d=0;d<N;d++){
 const h=smooth(D.days[d]);
 // exceedance: hours at or above each row (row index grows downward)
 const ex=[];let c=0;for(let i=0;i<R;i++){c+=h[i];ex.push(c)}
 const exAt=r=>{const t=r-r0;if(t<0)return 0;if(t>=R-1)return 24;const i=Math.floor(t),f=t-i;return ex[i]*(1-f)+ex[i+1]*f};
 const x=Math.round(X0+d*pitch+(pitch-pw)/2);
 const cut=top+rnd()*7;
 const grain=[];for(let i=0;i<pw;i++)grain.push((rnd()-0.5)*16+(i==0||i==pw-1?-14:0));
 let wob=0;
 for(let y=Math.floor(cut);y<bot;y++){
  wob+=(rnd()-0.5)*0.5;wob*=0.92;
  const e=Math.min(24,exAt(yRow(y+wob*2)));
  const t=e/24;
  const a=Math.min(1,Math.pow(t,0.62)*(0.9+rnd()*0.2)); // one hour of wetting still leaves a faint mark
  const m=Math.min(1,Math.pow(t,0.8)*1.5);
  for(let i=0;i<pw;i++){
   const gr=grain[i]+(rnd()-0.5)*10;
   const wc=[mid[0]+(wet[0]-mid[0])*m,mid[1]+(wet[1]-mid[1])*m,mid[2]+(wet[2]-mid[2])*m];
   const col=[0,1,2].map(k=>Math.round(dry[k]+gr+(wc[k]-dry[k]-gr)*a));
   g.fillStyle='rgb('+col+')';g.fillRect(x+i,y,1,1);
  }
 }
 // the day's highest wetting: a fine pale salt line where the stain begins
 for(let y=Math.floor(cut);y<bot;y++){
  if(exAt(yRow(y))>0.08){g.fillStyle='rgba(250,248,240,0.6)';g.fillRect(x,y-1,pw,1);break}
 }
 // shadow side
 g.fillStyle='rgba(0,0,0,0.10)';g.fillRect(x+pw-2,cut,2,bot-cut);
}
// ground of the harbour: everything below, always under
const grd=g.createLinearGradient(0,bot-30,0,Ht);
grd.addColorStop(0,'rgba(231,227,218,0)');grd.addColorStop(1,'rgba(231,227,218,1)');
g.fillStyle=grd;g.fillRect(0,bot-30,Wd,Ht-bot+30);
// caption
g.fillStyle='#4a463e';g.font='italic 15px Georgia, "Times New Roman", serif';
g.fillText('Sixty-One Piles',X0,783);
g.font='12px Georgia, "Times New Roman", serif';g.fillStyle='#7a7468';
g.textAlign='right';
g.fillText('one pile for each day of the record, left to right · each stained by the hours the water stood at or above every height',X1,783);
</script></body></html>'''
open('/tmp/claude-0/s130/mk/m08/work/index.html','w').write(html.replace('__DATA__',data))
