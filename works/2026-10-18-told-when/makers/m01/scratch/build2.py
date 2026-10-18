data=open('days.txt').read()
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Eighteen Steps Down</title>
<style>
:root{--paper:#f2eee5;--ink:#1c2430;--mute:#71757a}
html,body{margin:0;height:100%;background:var(--paper)}
body{display:flex;align-items:center;justify-content:center;overflow:hidden;
 font-family:Georgia,"Times New Roman",serif;color:var(--ink)}
#w{position:relative;width:1100px;height:800px;flex:none}
canvas{position:absolute;left:0;top:0;width:1100px;height:800px}
.t{position:absolute;left:70px;bottom:52px;font-size:22px;letter-spacing:.02em}
.s{position:absolute;right:70px;bottom:52px;font-size:13px;color:var(--mute);text-align:right;line-height:1.6;font-style:italic}
</style></head><body>
<div id="w"><canvas id="c" width="1100" height="800"></canvas>
<div class="t">Eighteen Steps Down</div>
<div class="s">sixty-one days, one column each, read left to right &middot; eighteen steps the instrument could tell apart<br>a tread marks a step the reading stood on that day, darker the longer it stayed</div>
</div>
<script>
// day x step dwell, 0-9, recovered from the plotted record (61 days x 18 steps, lowest step first)
const RAW="'''+data+r'''";
const M=RAW.split(',').map(r=>r.split('').map(Number));
const D=M.length, K=18;
const c=document.getElementById('c'), dpr=Math.max(1,window.devicePixelRatio||1);
c.width=1100*dpr;c.height=800*dpr;const g=c.getContext('2d');g.scale(dpr,dpr);
const L=70,R=1030,T=66,B=650;
const pitchX=(R-L)/D, pitchY=(B-T)/(K-1);
const tileW=pitchX-3.2, tileH=13;
g.strokeStyle='rgba(28,36,48,.075)';g.lineWidth=1;
for(let k=0;k<K;k++){const y=Math.round(B-k*pitchY)+.5;g.beginPath();g.moveTo(L-16,y);g.lineTo(R+16,y);g.stroke();}
g.fillStyle='rgba(28,36,48,.30)';
for(let d=0;d<=D;d++){const x=Math.round(L+d*pitchX-1.6);g.fillRect(x,B+26,1,d%7===0?8:3);}
for(let d=0;d<D;d++){
  const x=L+d*pitchX+1.6;
  for(let k=0;k<K;k++){
    const v=M[d][k]; if(v<1) continue;
    const al=Math.min(1,.12+.88*Math.pow(v/7,1.1));
    g.fillStyle='rgba(28,36,48,'+al.toFixed(3)+')';
    g.fillRect(x,B-k*pitchY-tileH/2,tileW,tileH);
  }
}
</script></body></html>'''
open('/tmp/claude-0/s135/mk/m01/work/index.html','w').write(html)
