import json
days=json.load(open('days.json'))
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nine Weeks Down</title>
<style>
:root{--paper:#f3efe6;--ink:#1d1b18;--faint:#cfc8b8;--soft:#8a8274}
html,body{margin:0;background:var(--paper);height:100%}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
svg{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}
text{font-family:Georgia,"Times New Roman",serif;fill:var(--ink)}
</style></head><body>
<svg id="w" viewBox="0 0 1100 800" preserveAspectRatio="xMidYMid meet" role="img"
 aria-label="Sixty-one days from 15 July to 13 September 2025 laid out as a wall calendar; in each day's square the hourly record is drawn as ink on eighteen fixed steps, and the ink sinks lower week by week."></svg>
<script>
const D=__DATA__;
const NS='http://www.w3.org/2000/svg', svg=document.getElementById('w');
function el(n,a,p){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e}
el('rect',{x:0,y:0,width:1100,height:800,fill:'#f3efe6'});
const L=74,T=118,CW=136,RH=70,S=10,LV=18,DX=12,DY=3.35;
const t=el('text',{x:L,y:56,'font-size':26,'letter-spacing':'0.5'});t.textContent='Nine Weeks Down';
const s=el('text',{x:L,y:80,'font-size':13,fill:'#8a8274','font-style':'italic'});
s.textContent='15 July – 13 September 2025 · one quantity, read every hour, kept on eighteen steps';
['Mon','Tue','Wed','Thu','Fri','Sat','Sun'].forEach((d,i)=>{const e=el('text',{x:L+i*CW+4,y:T-12,'font-size':11,fill:'#8a8274','letter-spacing':'1.5'});e.textContent=d.toUpperCase()});
const g=el('g',{});
for(let d=0;d<61;d++){
  const idx=d+1, col=idx%7, row=Math.floor(idx/7);   // 15 Jul 2025 is a Tuesday
  const x0=L+col*CW, y0=T+row*RH;
  const date=new Date(Date.UTC(2025,6,15+d));
  const dn=date.getUTCDate();
  const lab=el('text',{x:x0+4,y:y0+10,'font-size':10,fill:'#8a8274'},g);
  lab.textContent=dn===1||d===0?(dn+' '+['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep'][date.getUTCMonth()]):dn;
  if(dn===1||d===0)lab.setAttribute('fill','#1d1b18');
  const cx=x0+14, cy=y0+6;
  for(let l=0;l<LV;l++)for(let k=0;k<S;k++){
    const q=+D[d][l*S+k], x=cx+k*DX, y=cy+l*DY;
    if(q===0){el('circle',{cx:x,cy:y,r:0.55,fill:'#cfc8b8'},g)}
    else el('circle',{cx:x,cy:y,r:(0.7+q*0.11).toFixed(2),fill:'#1d1b18','fill-opacity':(0.18+q*0.09).toFixed(2)},g);
  }
}
const f=el('text',{x:L,y:T+9*RH+18,'font-size':11,fill:'#8a8274','font-style':'italic'});
f.textContent='Each square is one day, its hours running left to right in ten readings of the original picture. Higher in the square is a larger value; the eighteen rows are the same in every square.';
</script></body></html>'''
open('/tmp/claude-0/s135/mk/m03/work/index.html','w').write(html.replace('__DATA__',json.dumps(days)))
