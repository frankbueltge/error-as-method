import json
f=json.load(open('fold.json'))
H=[o['hours'] for o in f]
S=json.load(open('strip.json'))
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Light Draws In</title>
<style>
:root{--bg:#0b0c12;--ink:#d9cfbd;--dim:#7d7668;--faint:#3a3833}
html,body{margin:0;background:var(--bg);}
body{display:flex;align-items:center;justify-content:center;min-height:100vh;}
canvas{display:block;width:1100px;height:800px;max-width:100vw;height:auto;}
</style></head><body>
<canvas id="c" width="2200" height="1600" aria-label="Sixty-two lines of light, one per day, narrowing and dimming downward"></canvas>
<script>
const HOURS=__H__;
const STRIP=__S__;
const cv=document.getElementById('c'),g=cv.getContext('2d');
g.scale(2,2);
const W=1100,Ht=800;
g.fillStyle='#0b0c12';g.fillRect(0,0,W,Ht);

// geometry of the fold
const L=170,R=930,T=128,B=642;          // field
const n=HOURS.length, rowH=(B-T)/n, gap=Math.max(1.4,rowH*0.2);
const hx=h=>L+(h/24)*(R-L);              // solar hour -> x

// colour ramp: night indigo -> ember -> amber -> pale noon
const stops=[[0,[22,25,40]],[0.06,[52,30,48]],[0.2,[120,40,36]],[0.4,[188,84,34]],[0.6,[228,142,52]],[0.8,[246,204,120]],[1,[255,246,222]]];
function col(v){v=Math.max(0,Math.min(1,v));
  for(let i=1;i<stops.length;i++){if(v<=stops[i][0]){const a=stops[i-1],b=stops[i],t=(v-a[0])/(b[0]-a[0]);
    return a[1].map((c,j)=>Math.round(c+(b[1][j]-c)*t));}}return stops[stops.length-1][1];}

// smooth value at continuous solar hour (samples at whole hours)
function val(row,h){const i=Math.floor(h),t=h-i;
  const p=k=>row[Math.max(0,Math.min(23,k))];
  const p0=p(i-1),p1=p(i),p2=p(i+1),p3=p(i+2);
  const v=0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t);
  return Math.max(0,v);}

// recorded span: first row starts at ~17h, last row ends at ~16h solar
const firstH=17, lastH=16;
for(let r=0;r<n;r++){
  const y=T+r*rowH, h=rowH-gap;
  for(let x=L;x<R;x++){
    const sh=(x-L+0.5)/(R-L)*24;
    if((r===0&&sh<firstH-0.5)||(r===n-1&&sh>lastH+0.5)){
      // not in the record
      if((x+r*3)%6===0){g.fillStyle='#24242a';g.fillRect(x,y+h/2-0.5,1,1);}
      continue;}
    const v=val(HOURS[r],sh-0.0);
    const c=col(v);
    g.fillStyle=`rgb(${c[0]},${c[1]},${c[2]})`;
    g.fillRect(x,y,1.02,h);
  }
}

// soft bloom over the brightest light
g.save();g.globalCompositeOperation='lighter';g.filter='blur(6px)';g.globalAlpha=0.22;
g.drawImage(cv,L*2,T*2,(R-L)*2,(B-T)*2,L,T,R-L,B-T);
g.restore();g.filter='none';

// daily sums, at right
const sums=HOURS.map(r=>r.reduce((a,b)=>a+b,0)), smax=Math.max(...sums);
const SX=966, SW=104;
for(let r=0;r<n;r++){
  const y=T+r*rowH, h=rowH-gap, w=sums[r]/smax*SW;
  const part=(r===0||r===n-1);
  g.fillStyle=part?'#4a4438':'#c9a46a';
  g.globalAlpha=part?1:0.35+0.65*sums[r]/smax;
  g.fillRect(SX,y+h*0.15,w,h*0.7);
}
g.globalAlpha=1;

// type
g.textBaseline='alphabetic';
g.fillStyle='#e8dfcd';g.font='300 30px Georgia, "Times New Roman", serif';
g.fillText('The Light Draws In',L,62);
g.fillStyle='#8a8272';g.font='13px Georgia, "Times New Roman", serif';
g.fillText('Sunlight on level ground at Fort Peck, Montana, 634 m. One line per day, read downward; sun time across, noon at the centre.',L,88);

g.font='11px ui-monospace, Menlo, Consolas, monospace';g.fillStyle='#6f6858';
g.textAlign='center';
[[0,'midnight'],[6,'6'],[12,'noon'],[18,'18'],[24,'midnight']].forEach(([h,s])=>{
  g.fillText(s,hx(h),T-14);
  g.fillStyle='#3a3730';g.fillRect(Math.round(hx(h)),T-8,1,5);g.fillStyle='#6f6858';});
// noon thread
g.fillStyle='rgba(255,240,210,0.05)';g.fillRect(hx(12)-0.5,T,1,B-T);

g.textAlign='right';
g.fillText('first evening',L-16,T+rowH*0.8);
g.fillText('last afternoon',L-16,B-rowH*0.2);
// ten-day bracket
const by=T+rowH*21, be=by+rowH*10;
g.fillStyle='#4d483e';g.fillRect(L-16,by,1,be-by);g.fillRect(L-20,by,5,1);g.fillRect(L-20,be,5,1);
g.fillStyle='#6f6858';g.fillText('ten days',L-26,(by+be)/2+4);

g.textAlign='left';
g.fillText('light per day',SX,T-14);

// the record as received
const sy=692, sh=62, sx0=L, sx1=1070;
g.fillStyle='#6f6858';g.fillText('the record as it arrived: 1,464 hours, left to right',sx0,sy-12);
g.fillStyle='#16171f';g.fillRect(sx0,sy,sx1-sx0,sh);
g.fillStyle='rgba(217,190,140,0.75)';
for(const [x,y] of STRIP){
  const px=sx0+(x/300)*(sx1-sx0), py=sy+(y/90)*sh;
  g.fillRect(px-0.6,py-0.6,1.2,1.2);}
// marks where the fold cuts the strip (each local midnight)
const P=4.82071,n0=6.29415;
g.fillStyle='rgba(120,130,170,0.18)';
for(let k=-1;k<=60;k++){const xm=n0+(k+0.5)*P; if(xm>0&&xm<300) g.fillRect(sx0+(xm/300)*(sx1-sx0),sy,1,sh);}
g.fillStyle='#5a5448';g.font='10.5px ui-monospace, Menlo, Consolas, monospace';
g.fillText('faint rules: the midnights at which the strip was cut and stacked above',sx0,sy+sh+18);
</script></body></html>'''
html=html.replace('__H__',json.dumps(H,separators=(',',':'))).replace('__S__',json.dumps(S,separators=(',',':')))
open('/tmp/claude-0/s133/mk/m10/work/index.html','w').write(html)
print(len(html))
