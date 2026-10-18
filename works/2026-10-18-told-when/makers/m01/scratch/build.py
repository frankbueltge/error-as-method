data=open('occ.txt').read()
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Eighteen Steps Down</title>
<style>
:root{--paper:#f2eee5;--ink:#1c2430;--faint:rgba(28,36,48,.10);--mute:#6b6f74}
html,body{margin:0;height:100%;background:var(--paper)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden;
 font-family:Georgia,"Times New Roman",serif;color:var(--ink)}
#w{position:relative;width:1100px;height:800px;flex:none}
canvas{position:absolute;left:0;top:0;width:1100px;height:800px}
.t{position:absolute;left:70px;bottom:48px;font-size:22px;letter-spacing:.02em}
.s{position:absolute;right:70px;bottom:50px;font-size:13px;color:var(--mute);text-align:right;line-height:1.55;font-style:italic}
</style></head><body>
<div id="w"><canvas id="c" width="1100" height="800"></canvas>
<div class="t">Eighteen Steps Down</div>
<div class="s">sixty-one days, one column each &middot; eighteen steps the instrument could tell apart<br>each tread is a step the reading stood on that day, darker where it stayed</div>
</div>
<script>
const RAW="'''+data+r'''";
const cols=RAW.split(',').map(r=>r.split('').map(Number)); // 296 image columns x 18 steps
const N=cols.length, D=61, K=18;
const c=document.getElementById('c'), dpr=Math.max(1,window.devicePixelRatio||1);
c.width=1100*dpr;c.height=800*dpr;const g=c.getContext('2d');g.scale(dpr,dpr);
const L=70,R=1030,T=70,B=650;
const pitchX=(R-L)/D, pitchY=(B-T)/(K-1);
const tileW=pitchX-4, tileH=9;
// steps: faint hairlines
g.strokeStyle='rgba(28,36,48,.09)';g.lineWidth=1;
for(let k=0;k<K;k++){const y=Math.round(B-k*pitchY)+.5;g.beginPath();g.moveTo(L-14,y);g.lineTo(R+14,y);g.stroke();}
// day ticks every 7 days along the floor, as counting marks only
g.fillStyle='rgba(28,36,48,.28)';
for(let d=0;d<=D;d++){const x=L+d*pitchX; g.fillRect(Math.round(x)-.5, B+22, 1, d%7===0?7:3);}
// treads
const w=N/D;
for(let d=0;d<D;d++){
  const a=d*w,b=a+w, x0=L+d*pitchX+2;
  for(let k=0;k<K;k++){
    const yc=B-k*pitchY;
    let any=0;
    for(let x=Math.floor(a);x<Math.ceil(b);x++){
      const lo=Math.max(a,x),hi=Math.min(b,x+1); if(hi<=lo) continue;
      const v=cols[x][k]; if(v<3) continue;
      any=1;
      const al=Math.min(1,.18+.82*(v-3)/5);
      g.fillStyle='rgba(28,36,48,'+al.toFixed(3)+')';
      const sx=x0+(lo-a)/w*tileW, ex=x0+(hi-a)/w*tileW;
      g.fillRect(sx,yc-tileH/2,ex-sx+.35,tileH);
    }
  }
}
</script></body></html>'''
open('/tmp/claude-0/s135/mk/m01/work/index.html','w').write(html)
