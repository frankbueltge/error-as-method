import json
H=json.load(open('hours.json')); S=open('src.txt').read()
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Days</title>
<style>
:root{--paper:#f2eee5;--ink:#1c2230;--soft:#8a8578}
html,body{margin:0;background:var(--paper);}
body{display:flex;justify-content:center;align-items:center;min-height:100vh}
canvas{display:block;width:1100px;height:800px;max-width:100vw;height:auto;aspect-ratio:1100/800}
</style></head><body>
<canvas id="c" width="1100" height="800" aria-label="Sixty-one columns of 24 dots each: one column per day of an hourly carbon dioxide record, its hours sorted by value."></canvas>
<script>
// 61 days x 24 hourly values, read from the source plot: row position in the 90-px-high original (0 = top = highest)
const H=__H__;
// the source plot itself, 300 x 90, darkness 0-9
const S="__S__";
const c=document.getElementById('c'),g=c.getContext('2d');
const dpr=Math.max(1,Math.min(3,window.devicePixelRatio||1));
c.width=1100*dpr;c.height=800*dpr;g.scale(dpr,dpr);
g.fillStyle='#f2eee5';g.fillRect(0,0,1100,800);
const X0=95,DX=(1005-95)/60,Ytop=4,Ybot=86,YA=96,YB=600;
const Y=r=>YA+(r-Ytop)/(Ybot-Ytop)*(YB-YA);
// faint level lines from the source's own pixel grid (every 10 px of the original)
g.strokeStyle='rgba(28,34,48,0.06)';g.lineWidth=1;
for(let r=10;r<=80;r+=10){g.beginPath();g.moveTo(70,Math.round(Y(r))+.5);g.lineTo(1030,Math.round(Y(r))+.5);g.stroke();}
// each day: a hairline from its highest to its lowest hour, then the 24 hours as dots
for(let d=0;d<61;d++){
  const hs=H[d].slice().sort((a,b)=>a-b), x=X0+d*DX;
  g.strokeStyle='rgba(28,34,48,0.22)';g.lineWidth=0.8;
  g.beginPath();g.moveTo(x,Y(hs[0]));g.lineTo(x,Y(hs[23]));g.stroke();
  // hours that sit at the same level push each other sideways, so the day takes the shape of where its air lingered
  const R=2.3,placed=[];
  for(let i=0;i<24;i++){
    const y=Y(hs[i]);let px=0;
    for(let k=0;k<40;k++){
      const t=k===0?0:(k%2?1:-1)*Math.ceil(k/2)*0.9;
      if(placed.every(q=>(q[0]-t)*(q[0]-t)+(q[1]-y)*(q[1]-y)>=(2*R+0.3)*(2*R+0.3))){px=t;break;}
      px=t;
    }
    placed.push([px,y]);
    g.fillStyle='rgba(28,34,48,0.84)';
    g.beginPath();g.arc(x+px,y,R,0,Math.PI*2);g.fill();
  }
}
// the record as it was given, at its own size
const ox=95,oy=668;
for(let r=0;r<90;r++)for(let k=0;k<300;k++){
  const v=+S[r*300+k]; if(!v)continue;
  g.fillStyle='rgba(28,34,48,'+(v/9*0.7).toFixed(3)+')';g.fillRect(ox+k,oy+r-4,1,1);
}
// words
g.fillStyle='#1c2230';g.font='600 22px Georgia,"Times New Roman",serif';g.textBaseline='alphabetic';
g.fillText('Sixty-One Days',560,688);
g.fillStyle='#5b5a55';g.font='14px Georgia,"Times New Roman",serif';
const L=['Carbon dioxide at one station, one value an hour.',
'Each column is a day; its 24 dots are that day’s hours,',
'sorted by level. When they came is set aside;',
'how high and how low the air went is kept.',
'Below: the record as it arrived.'];
L.forEach((t,i)=>g.fillText(t,560,714+i*18));
</script></body></html>'''
html=html.replace('__H__',json.dumps(H,separators=(',',':'))).replace('__S__',S)
open('/tmp/claude-0/s131/mk/m12/work/index.html','w').write(html)
print(len(html))
