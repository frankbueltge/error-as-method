q=open('/tmp/claude-0/s133/mk/m20/scratch/q.txt').read()
html='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixty-One Days of Light</title>
<style>
  :root { --bg:#0a0a0d; --ink:#d9d2c3; --dim:#7d7668; --faint:#3a3730; }
  html,body { margin:0; background:var(--bg); color:var(--ink); }
  body { width:1100px; height:800px; overflow:hidden; position:relative;
         font-family: Georgia, "Times New Roman", serif; }
  canvas { position:absolute; left:0; top:0; }
</style>
</head>
<body>
<canvas id="c" width="1100" height="800"></canvas>
<script>
// Estimated hourly values (0-100, 100 = the brightest hour in the record) read back
// from a 300x90 dot plot of 1,464 hourly readings at Fort Peck, Montana.
const Q=[__Q__];
const W=1100,H=800,cv=document.getElementById('c');
const dpr=Math.max(1,window.devicePixelRatio||1);
cv.width=W*dpr;cv.height=H*dpr;cv.style.width=W+'px';cv.style.height=H+'px';
const g=cv.getContext('2d');g.scale(dpr,dpr);
g.fillStyle='#0a0a0d';g.fillRect(0,0,W,H);

// colour of light: night indigo -> dusk violet -> ember -> amber -> straw -> white
const stops=[[0,[17,18,30]],[.08,[40,24,58]],[.25,[118,38,52]],[.45,[196,84,40]],
             [.65,[236,150,58]],[.85,[248,214,128]],[1,[255,250,232]]];
function col(v){v=Math.max(0,Math.min(1,v));
  for(let i=1;i<stops.length;i++){if(v<=stops[i][0]){const a=stops[i-1],b=stops[i],t=(v-a[0])/(b[0]-a[0]);
    return [0,1,2].map(k=>Math.round(a[1][k]+(b[1][k]-a[1][k])*t));}}return stops[stops.length-1][1];}

// rows are days from (inferred) local midnight to midnight; the record begins at 17:00 and ends at 16:00
const OFF=7, ROWS=62;
const L=150, R=950, T=96, RH=9, GAP=1, BW=R-L;
const val=(row,h)=>{const i=(row-1)*24+h+OFF;return (i<0||i>=Q.length)?null:Q[i]/100;};
const img=g.createImageData(BW*dpr|0,1);
for(let r=0;r<ROWS;r++){
  const y=T+r*(RH+GAP);
  for(let px=0;px<BW;px++){
    const hf=px/BW*24-0.5, h0=Math.floor(hf), t=hf-h0, s=(1-Math.cos(Math.PI*t))/2;
    const a=val(r,Math.max(0,h0)), b=val(r,Math.min(23,h0+1));
    let v;
    if(a===null&&b===null) continue;
    if(a===null) { if(t<0.5) continue; v=b; }
    else if(b===null) { if(t>0.5) continue; v=a; }
    else v=a+(b-a)*s;
    const c=col(v);
    g.fillStyle='rgb('+c[0]+','+c[1]+','+c[2]+')';
    g.fillRect(L+px,y,1.02,RH);
  }
  // daily total, a quiet rule to the right
  let sum=0,n=0;for(let h=0;h<24;h++){const v=val(r,h);if(v!==null){sum+=v;n++;}}
  if(n===24){g.fillStyle='#5b5447';g.fillRect(R+18,y+RH/2-0.75,sum*14,1.5);}
  else {g.fillStyle='#3a3730';g.fillRect(R+18,y+RH/2-0.5,sum*14,1);}
}
// hour ticks
g.fillStyle='#7d7668';g.font='11px Georgia, serif';g.textAlign='center';
const yb=T+ROWS*(RH+GAP)+14;
[['midnight',0],['6',6],['noon',12],['18',18],['midnight',24]].forEach(([s,h])=>{
  const x=L+h/24*BW; g.fillRect(x-0.5,yb-10,1,5); g.fillText(s,x,yb+6);});
// left margin: first and last day
g.textAlign='right';g.fillStyle='#7d7668';
g.fillText('first reading',L-14,T+RH-1);
g.fillText('last reading',L-14,T+(ROWS-1)*(RH+GAP)+RH-1);
g.save();g.translate(L-60,T+ROWS*(RH+GAP)/2);g.rotate(-Math.PI/2);g.textAlign='center';
g.fillStyle='#4f4a40';g.fillText('one row per day  \\u2193',0,0);g.restore();
g.textAlign='left';g.fillStyle='#4f4a40';g.fillText('light per day',R+18,T-10);

// title
g.textAlign='left';g.fillStyle='#d9d2c3';g.font='italic 26px Georgia, serif';
g.fillText('Sixty-One Days of Light',L,52);
g.fillStyle='#7d7668';g.font='12px Georgia, serif';
g.fillText('Sunlight on level ground at Fort Peck, Montana, 634 m above sea level. One band per hour, one row per day.',L,72);
// key
const kx=L, ky=H-44, kw=220;
for(let i=0;i<kw;i++){const c=col(i/(kw-1));g.fillStyle='rgb('+c+')';g.fillRect(kx+i,ky,1.02,6);}
g.fillStyle='#7d7668';g.font='11px Georgia, serif';g.textAlign='left';
g.fillText('none',kx,ky+20);g.textAlign='right';g.fillText('the brightest hour of the record',kx+kw,ky+20);
g.textAlign='right';g.fillStyle='#4f4a40';
g.fillText('Values are read back from a small dot plot and are approximate; rows are aligned on the night gaps, read as local midnight.',R,ky+20);
</script>
</body>
</html>
'''
open('/tmp/claude-0/s133/mk/m20/work/index.html','w').write(html.replace('__Q__',q))
