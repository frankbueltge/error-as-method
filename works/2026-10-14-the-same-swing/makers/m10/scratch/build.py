import sys
pts=open('pts.txt').read()
P=295/61.0
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Turns</title>
<style>
:root{--ground:#f2eee5;--ink:#1d1b18;--faint:#b9b1a2}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ground:#f2eee5;--ink:#1d1b18;--faint:#b9b1a2}}
html,body{margin:0;height:100%;background:var(--ground)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
canvas{display:block}
</style></head><body>
<canvas id="c" aria-label="A record of 1,464 values wound into a spiral of 61 turns, one turn per day"></canvas>
<script>
const RAW="__PTS__";
const W=1100,H=800,P=__P__,X0=3;
const c=document.getElementById('c'),dpr=Math.max(1,window.devicePixelRatio||1);
c.width=W*dpr;c.height=H*dpr;c.style.width=W+'px';c.style.height=H+'px';
const g=c.getContext('2d');g.scale(dpr,dpr);
const cs=getComputedStyle(document.documentElement);
const ink=cs.getPropertyValue('--ink').trim(),faint=cs.getPropertyValue('--faint').trim();
g.fillStyle=cs.getPropertyValue('--ground').trim();g.fillRect(0,0,W,H);
const a=RAW.split(',').map(Number),pts=[];
for(let i=0;i<a.length;i+=3)pts.push([a[i],a[i+1],a[i+2]]);
const CX=W/2,CY=H/2+6,R0=__R0__,S=__S__,G=__G__,YC=__YC__,PH=__PH__;
const ang=t=>2*Math.PI*(t-PH)-Math.PI/2;      // warmest phase of the day at the top, clockwise
// guide: the day itself, the spiral the record is wound on
g.strokeStyle=faint;g.lineWidth=0.6;g.beginPath();
for(let t=0;t<=61;t+=0.005){const r=R0+S*t,A=ang(t);const x=CX+r*Math.cos(A),y=CY+r*Math.sin(A);t?g.lineTo(x,y):g.moveTo(x,y);}
g.stroke();
// the material: every dark pixel of the record, re-placed
for(const [x,y,w] of pts){
  const t0=(x-0.5-X0)/P,t1=(x+0.5-X0)/P;   // a pixel column spans ~4.9 hours of the record
  g.globalAlpha=w/15*__AL__;g.strokeStyle=ink;g.lineWidth=__LW__;g.beginPath();
  for(let k=0;k<=12;k++){const t=t0+(t1-t0)*k/12,r=R0+S*t+G*(y-YC),A=ang(t),px=CX+r*Math.cos(A),py=CY+r*Math.sin(A);k?g.lineTo(px,py):g.moveTo(px,py);}
  g.stroke();
}
g.globalAlpha=1;
</script></body></html>'''
v=dict(R0='34',S='5.6',G='0.42',YC='45',PH='0.75',DR='1.25',AL='0.35',LW='1.3')
for k,val in v.items(): html=html.replace(f'__{k}__',val)
html=html.replace('__P__',repr(P)).replace('__PTS__',pts)
open(sys.argv[1],'w').write(html)
