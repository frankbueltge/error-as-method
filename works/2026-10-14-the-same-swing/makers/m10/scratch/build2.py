import json, sys
f=json.load(open('fit.json')); pts=open('pts.txt').read()
P=295/61.0
B=[d['b'] for d in f['days']]; A=[d['a'] for d in f['days']]
prm=dict(R0=46,S=5.4,G=0.30,YC=38,PH=0.75)
if len(sys.argv)>2: prm.update(json.loads(sys.argv[2]))
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Turns</title>
<style>
:root{--ground:#efebe2;--ink:#191714;--dust:#8a8274;--note:#6f685d}
html,body{margin:0;height:100%;background:var(--ground)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
canvas{display:block}
</style></head><body>
<canvas id="c" role="img" aria-label="A record of 1,464 values wound into a spiral of 61 turns, one turn for each day it covers; the daily swing bulges outward at the top of every turn."></canvas>
<script>
// Material: every dark pixel of record.jpg (x, height from bottom, darkness/16),
// and, per day of the record, the level (B) and swing (A) fitted to those pixels
// using the record's own average daily shape (SH, 12 steps of 2 hours).
const RAW="__PTS__";
const B=__B__, A=__A__, SH=__SH__;
const W=1100,H=800,P=__P__,X0=3,N=61;
const {R0,S,G,YC,PH}=__PRM__;
const c=document.getElementById('c'),dpr=Math.max(1,window.devicePixelRatio||1);
c.width=W*dpr;c.height=H*dpr;c.style.width=W+'px';c.style.height=H+'px';
const g=c.getContext('2d');g.scale(dpr,dpr);
const cs=getComputedStyle(document.documentElement),col=k=>cs.getPropertyValue(k).trim();
g.fillStyle=col('--ground');g.fillRect(0,0,W,H);
const CX=W/2,CY=H/2;
const ang=t=>2*Math.PI*(t-PH)-Math.PI/2;
const shape=ph=>{const u=ph*SH.length-0.5,i=Math.floor(u),f=u-i,n=SH.length;return SH[((i%n)+n)%n]*(1-f)+SH[(((i+1)%n)+n)%n]*f;};
const daily=(arr,t)=>{const u=t-0.5,i=Math.max(0,Math.min(N-2,Math.floor(u))),f=Math.max(0,Math.min(1,u-i));return arr[i]*(1-f)+arr[i+1]*f;};
const pos=(t,y)=>{const r=R0+S*t+G*(y-YC),a=ang(t);return[CX+r*Math.cos(a),CY+r*Math.sin(a)];};
// dust: the original dots, each where its moment of the day falls
const a=RAW.split(',').map(Number);
g.fillStyle=col('--dust');
for(let i=0;i<a.length;i+=3){const t=(a[i]-X0)/P,[x,y]=pos(t,a[i+1]);g.globalAlpha=a[i+2]/15*__DA__;g.fillRect(x-0.6,y-0.6,1.2,1.2);}
g.globalAlpha=1;
// the swing: one continuous line, one turn per day
g.strokeStyle=col('--ink');g.lineJoin='round';
let prev=null;
for(let t=0;t<=N;t+=1/480){
  const y=daily(B,t)+daily(A,t)*shape(((t%1)+1)%1);
  const p=pos(t,y);
  if(prev){g.lineWidth=__LW0__+__LW1__*(daily(A,t)/55);g.beginPath();g.moveTo(prev[0],prev[1]);g.lineTo(p[0],p[1]);g.stroke();}
  prev=p;
}
</script></body></html>'''
html=(html.replace('__PTS__',pts).replace('__B__',json.dumps(B)).replace('__A__',json.dumps(A))
 .replace('__SH__',json.dumps([round(s,3) for s in f['shape']])).replace('__P__',repr(P)).replace('__PRM__',json.dumps(prm))
 .replace('__DA__',str(prm.get('DA',0.5))).replace('__LW0__',str(prm.get('LW0',0.5))).replace('__LW1__',str(prm.get('LW1',1.2))))
open(sys.argv[1],'w').write(html)
