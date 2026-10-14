import json
D=open('/tmp/claude-0/s124/mk/m12/scratch/dark.json').read().strip()
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=1100">
<title>1,464 into 40</title>
<style>
html,body{margin:0;background:#f4f1ea}
body{width:1100px;height:800px;overflow:hidden}
canvas{display:block;width:1100px;height:800px}
</style></head><body><canvas id="c" width="1100" height="800"></canvas>
<script>
// Darkness (0 = white, 1 = black) of each of the 12 pixels in each of the 40 columns
// of record.jpg, top row first. This grid is all the source contains.
const D=__D__;
const W=1100,H=800,dpr=Math.max(1,window.devicePixelRatio||1);
const cv=document.getElementById('c');cv.width=W*dpr;cv.height=H*dpr;
const g=cv.getContext('2d');g.scale(dpr,dpr);
const ink='26,24,22';
g.fillStyle='#f4f1ea';g.fillRect(0,0,W,H);

const L=90,R=1010,span=R-L,NC=40,NH=1464,PER=NH/NC; // 36.6 hours per column
const top=70,bot=470,rowH=(bot-top)/12;
const colW=span/NC,gap=3;

// 1. the forty columns: each pixel's darkness, smoothed only between its own row centres
for(let c=0;c<NC;c++){
  const x0=L+c*colW+gap/2,w=colW-gap,d=D[c];
  for(let y=top;y<bot;y++){
    const r=(y+0.5-top)/rowH-0.5;
    let v;
    if(r<=0)v=d[0];else if(r>=11)v=d[11];
    else{const i=Math.floor(r),f=r-i;v=d[i]*(1-f)+d[i+1]*f;}
    v=Math.max(0,Math.min(1,v));
    g.fillStyle='rgba('+ink+','+(v*0.92).toFixed(3)+')';
    g.fillRect(x0,y,w,1);
  }
}

// 2. the hours: 1,464 hairlines on a ruler, each drawn up to the column that swallowed it
const hy=700,fy=520; // ruler line, mouth of the funnel
g.lineWidth=0.35;
for(let h=0;h<NH;h++){
  const xh=L+(h+0.5)*span/NH;
  const c=Math.min(NC-1,Math.floor((h+0.5)/PER));
  const xc=L+(c+0.5)*colW;
  // position of this hour inside its column's 36.6, spread across the mouth
  const u=((h+0.5)-c*PER)/PER-0.5;
  const xm=xc+u*3;
  g.strokeStyle='rgba('+ink+',0.22)';
  g.beginPath();g.moveTo(xh,hy);
  g.bezierCurveTo(xh,hy-70,xm,fy+120,xm,fy);
  g.lineTo(xm,bot+2);
  g.stroke();
}
/* mouth */
g.strokeStyle='rgba('+ink+',0.5)';g.lineWidth=0.6;


// ruler: an hour tick each, a longer tick at each day's start
for(let h=0;h<=NH;h++){
  const x=L+h*span/NH,day=h%24===0;
  g.strokeStyle='rgba('+ink+','+(day?0.85:0.35)+')';
  g.lineWidth=day?0.8:0.4;
  g.beginPath();g.moveTo(x,hy);g.lineTo(x,hy+(day?14:5));g.stroke();
}

// captions
g.fillStyle='rgba('+ink+',0.8)';
g.font='12px Georgia, \"Times New Roman\", serif';
g.textBaseline='alphabetic';
g.fillText('1,464 hours, one value each',L,hy+36);
g.textAlign='right';
g.fillText('61 days',R,hy+36);
g.textAlign='left';
g.fillStyle='rgba('+ink+',0.55)';
g.font='italic 12px Georgia, \"Times New Roman\", serif';
g.fillText('what reached us: 40 columns of 12 grey pixels, each holding 36.6 hours',L,top-22);
g.textAlign='right';
g.fillText('higher is more',R,top-22);
</script></body></html>'''
open('/tmp/claude-0/s124/mk/m12/work/index.html','w').write(html.replace('__D__',D))
