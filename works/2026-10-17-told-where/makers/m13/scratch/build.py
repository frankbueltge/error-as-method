import json
ys=json.load(open('/tmp/claude-0/s133/mk/m13/scratch/ys.json'))
v=[max(0,min(100,round(100*(84-y)/78))) for y in ys]
data=','.join(map(str,v))
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Turns</title>
<style>
:root{--bg:#07080d;--ink:#cfc6b4;--dim:#6f6a60}
html,body{margin:0;height:100%;background:var(--bg)}
body{display:flex;align-items:center;justify-content:center;font-family:Georgia,"Times New Roman",serif;color:var(--ink)}
.plate{position:relative;width:1100px;height:800px;max-width:100vw;max-height:100vh;aspect-ratio:11/8}
canvas{position:absolute;inset:0;width:100%;height:100%}
.t{position:absolute;left:44px;top:38px;font-size:22px;letter-spacing:.04em;font-weight:normal;margin:0}
.s{position:absolute;left:44px;top:70px;font-size:13px;color:var(--dim);font-style:italic;line-height:1.55;max-width:260px}
.k{position:absolute;right:44px;bottom:36px;font-size:12px;color:var(--dim);text-align:right;line-height:1.7;font-style:italic}
</style></head><body>
<div class="plate">
<canvas id="c" width="1100" height="800" aria-label="Sixty-one concentric rings of hourly light forming a sun over a dark wedge of night"></canvas>
<h1 class="t">Sixty-One Turns</h1>
<div class="s">Fort Peck, Montana &middot; 634 m<br>one value an hour, 1,464 hours</div>
<div class="k">each ring one day, first innermost &middot; midday at the top, midnight below<br>light from the record&rsquo;s own values; the night is where it falls to nothing</div>
</div>
<script>
const V=[__DATA__];
const NOON=17.95, CX=550, CY=430, R0=46, R1=352;
const NR=62; // ring -1 .. 60
const RW=(R1-R0)/NR;
const c=document.getElementById('c');
const dpr=Math.min(2,window.devicePixelRatio||1);
c.width=1100*dpr;c.height=800*dpr;
const g=c.getContext('2d');
const img=g.createImageData(c.width,c.height);const D=img.data;
const stops=[[0,[7,8,13]],[0.05,[30,12,16]],[0.2,[96,28,20]],[0.42,[190,86,34]],[0.62,[232,150,62]],[0.8,[246,206,128]],[0.93,[252,236,196]],[1,[255,252,240]]];
function col(t){t=Math.max(0,Math.min(1,t));for(let k=1;k<stops.length;k++){if(t<=stops[k][0]){const a=stops[k-1],b=stops[k],u=(t-a[0])/(b[0]-a[0]);return [a[1][0]+(b[1][0]-a[1][0])*u,a[1][1]+(b[1][1]-a[1][1])*u,a[1][2]+(b[1][2]-a[1][2])*u];}}return stops[stops.length-1][1];}
function val(i){return (i<0||i>=V.length)?null:V[i]/100;}
const BG=[7,8,13];
for(let py=0;py<c.height;py++)for(let px=0;px<c.width;px++){
  const x=px/dpr+0.5/dpr-CX,y=py/dpr+0.5/dpr-CY;
  const r=Math.hypot(x,y);let o=(py*c.width+px)*4;let rgb=BG;
  if(r>=R0&&r<R1){
    const rf=(r-R0)/RW, ring=Math.floor(rf)-1, fr=rf-Math.floor(rf);
    // angle clockwise from top, in hours relative to noon
    let a=Math.atan2(x,-y); let hrel=a/(2*Math.PI)*24; // -12..12
    const fi=24*ring+NOON+hrel+12-12; // continuous index within ring's solar day
    const i0=Math.floor(fi), u=fi-i0;
    const a0=val(i0), a1=val(i0+1);
    if(a0!==null&&a1!==null){
      const w=(1-Math.cos(Math.PI*u))/2; const t=a0*(1-w)+a1*w;
      let cc=col(Math.pow(t,1.25));
      // groove between rings
      const edge=Math.min(fr,1-fr)*RW; const k=edge<0.45?0.35+edge:1;
      rgb=[cc[0]*k+BG[0]*(1-k),cc[1]*k+BG[1]*(1-k),cc[2]*k+BG[2]*(1-k)];
    }
  }
  D[o]=rgb[0];D[o+1]=rgb[1];D[o+2]=rgb[2];D[o+3]=255;
}
g.putImageData(img,0,0);
</script>
</body></html>'''
open('/tmp/claude-0/s133/mk/m13/work/index.html','w').write(html.replace('__DATA__',data))
