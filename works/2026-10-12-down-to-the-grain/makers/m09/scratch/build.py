import json
d=json.load(open('/tmp/claude-0/s122/mk/m09/scratch/series.json'))
vals=','.join(str(int(round(x))) for x in d['v'])
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fifty Minutes Late</title>
<style>
:root{--paper:#f3efe6;--ink:#1d2430;--muted:#7d7a72}
html,body{margin:0;height:100%;background:var(--paper)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
canvas{display:block}
</style></head><body>
<canvas id="c" width="1100" height="800" style="width:1100px;height:800px"></canvas>
<script>
const V=[__VALS__];
const W=1100,H=800,dpr=Math.max(1,window.devicePixelRatio||1);
const cv=document.getElementById('c');cv.width=W*dpr;cv.height=H*dpr;
const g=cv.getContext('2d');g.scale(dpr,dpr);
g.fillStyle='#f3efe6';g.fillRect(0,0,W,H);
const N=V.length,PX=19,COLS=48*PX,RH=9,GAP=1,L=94,T=46;
function at(t){if(t<0||t>N-1)return null;const i=Math.floor(t),f=t-i;return i>=N-1?V[N-1]:V[i]*(1-f)+V[i+1]*f;}
// colour: paper -> deep sea ink across the ordinary tidal range; beyond it, a rust ink for water the tide alone does not bring
const P=[243,239,230],A=[178,196,204],B=[46,72,98],C=[20,26,38],R=[150,62,36],R2=[96,30,18];
function mix(a,b,f){return a.map((x,k)=>Math.round(x+(b[k]-x)*f));}
function col(v){
  const lo=48,mid=106,hi=186,top=335;
  if(v<=lo)return P;
  if(v<mid){const f=(v-lo)/(mid-lo);return mix(P,A,Math.pow(f,1.15));}
  if(v<hi){const f=(v-mid)/(hi-mid);return f<.75?mix(A,B,f/.75):mix(B,C,(f-.75)/.25);}
  const f=Math.min(1,(v-hi)/(top-hi));return f<.3?mix(C,R,f/.3):mix(R,R2,(f-.3)/.7);
}
for(let d=0;d<61;d++){
  const y=T+d*(RH+GAP);
  for(let x=0;x<COLS;x++){
    const v=at(d*24+(x+.5)/PX);if(v===null)continue;
    const c=col(v);g.fillStyle='rgb('+c+')';g.fillRect(L+x,y,1,RH);
  }
}
// hairline between the day and the day after
g.strokeStyle='rgba(243,239,230,.9)';g.lineWidth=1;
g.beginPath();g.moveTo(L+24*PX+.5,T-6);g.lineTo(L+24*PX+.5,T+61*(RH+GAP));g.stroke();
// text
g.fillStyle='#1d2430';g.font='italic 26px Georgia, "Times New Roman", serif';g.textBaseline='alphabetic';
g.fillText('Fifty Minutes Late',L,T+61*(RH+GAP)+48);
g.fillStyle='#7d7a72';g.font='12px Georgia, "Times New Roman", serif';
const cap=['Sixty-one days of an hourly record, one day to a row, each row followed by the next day so the bands can run on.',
'Darker is higher. The dark bands lean right: twice a day the peak comes, and each day it comes about fifty minutes later.',
'Rust marks the few hours that rise above the highest level reached on any other day.'];
cap.forEach((s,i)=>g.fillText(s,L,T+61*(RH+GAP)+74+i*18));
// small tick marks: noon/midnight of each day half, no numbers
g.fillStyle='#7d7a72';
for(let h=0;h<=48;h+=6){const x=L+h*PX;g.fillRect(Math.round(x),T-(h%24===0?10:6),1,h%24===0?6:3);}
</script></body></html>'''
open('/tmp/claude-0/s122/mk/m09/work/index.html','w').write(html.replace('__VALS__',vals))
