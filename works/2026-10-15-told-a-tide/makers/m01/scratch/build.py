data=open('/tmp/claude-0/s128/mk/m01/scratch/data.txt').read().strip()
html=r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>It Keeps the Sun's Time</title>
<style>
  :root{--paper:#f3efe6;--ink:#1d2730;--muted:#6d6a62;--ghost:#c4492f;}
  html,body{margin:0;background:var(--paper);}
  body{width:1100px;height:800px;overflow:hidden;font-family:Georgia,"Iowan Old Style","Palatino Linotype",serif;color:var(--ink);}
  svg{display:block}
</style>
</head>
<body>
<svg id="w" width="1100" height="800" viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg"></svg>
<script>
// 1,464 hourly values, read back (approximately) from the 300 x 90 px dot plot supplied.
// Units are the plot's own: pixels of height x 10. Larger = higher.
const V=[__DATA__].map(a=>a/10);
const N=V.length, DAYS=N/24;
const NS='http://www.w3.org/2000/svg', svg=document.getElementById('w');
const el=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e;};

// --- the spiral: one turn per day, day 1 at the centre, clockwise from the top
const CX=405, CY=400, R0=62, R1=372, STEP=(R1-R0)/DAYS;
const rad=t=>R0+STEP*t/24;                       // t in hours
const pt=(t,r)=>{const a=2*Math.PI*(t%24)/24-Math.PI/2;return [CX+r*Math.cos(a),CY+r*Math.sin(a)];};

// colour: low water pale, high water deep
const lo=18, hi=73;
const stops=[[0,[240,232,214]],[0.30,[200,214,205]],[0.55,[104,150,160]],[0.80,[38,82,105]],[1,[16,32,46]]];
function col(v){let x=Math.max(0,Math.min(1,(v-lo)/(hi-lo)));
  for(let i=1;i<stops.length;i++){if(x<=stops[i][0]){const[a,ca]=stops[i-1],[b,cb]=stops[i],f=(x-a)/(b-a);
    return 'rgb('+ca.map((c,j)=>Math.round(c+(cb[j]-c)*f)).join(',')+')';}}}

const g=el('g',{});
for(let i=0;i<N;i++){
  const t0=i, t1=i+1.04, steps=6, w=STEP*0.56;
  const outer=[], inner=[];
  for(let s=0;s<=steps;s++){const t=t0+(t1-t0)*s/steps, r=rad(t);
    outer.push(pt(t,r+w)); inner.unshift(pt(t,r-w));}
  const d='M'+outer.concat(inner).map(p=>p[0].toFixed(2)+' '+p[1].toFixed(2)).join('L')+'Z';
  el('path',{d,fill:col(V[i])},g);
}

// --- where a tide's high waters would have fallen: every 12 h 25 min, so
// about 50 minutes later each day. Two arms; their starting hour is arbitrary.
const M2=12.4206, T0=2;
for(const off of [0,M2]){
  const pts=[];
  for(let j=0;;j+=0.05){const t=T0+off+j*2*M2; if(t>N)break;
    const ang=2*Math.PI*((T0+off+j*(2*M2-24))/24)-Math.PI/2, r=rad(t);
    pts.push([CX+r*Math.cos(ang),CY+r*Math.sin(ang)]);}
  const d='M'+pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join('L');
  el('path',{d,fill:'none',stroke:'#f3efe6','stroke-width':4.2,opacity:0.75,'stroke-linecap':'round'});
  el('path',{d,fill:'none',stroke:'#c4492f','stroke-width':1.6,'stroke-linecap':'round'});
}
el('circle',{cx:CX,cy:CY,r:2,fill:'#1d2730'});

// --- right-hand column
const X=820;
const txt=(s,y,size,fill,style,weight)=>{const t=el('text',{x:X,y,'font-size':size,fill:fill||'#1d2730','font-style':style||'normal','font-weight':weight||'normal'});t.textContent=s;return t;};
txt('It Keeps',96,34); txt('the Sun’s Time',136,34);
const body=[
 'A record said to be the water',
 'in a tidal harbour: one reading',
 'an hour for sixty-one days,',
 'wound here one day to a turn,',
 'the first day at the centre.',
 '',
 'Deep colour is high, pale is low.',
 '',
 'A tide comes back about fifty',
 'minutes later every day. Its high',
 'waters would have walked round',
 'the dial along the red spirals.',
 '',
 'This record does not walk.',
 'Its low hours fall in the same',
 'place on every turn: once a day,',
 'every twenty-four hours.'];
body.forEach((s,k)=>txt(s,190+k*21,15.5,k>=13?'#1d2730':'#4a4b4a',k>=13?'italic':'normal'));

// --- the record as it was received, small, for comparison
const SX=X, SY=600, SW=240, SH=70;
el('rect',{x:SX-0.5,y:SY-0.5,width:SW+1,height:SH+1,fill:'#fbf9f4',stroke:'#d8d2c4'});
for(let i=0;i<N;i++){const x=SX+SW*(i+0.5)/N, y=SY+SH-((V[i]-2)/86)*SH;
  el('rect',{x:x-0.45,y:y-0.45,width:0.9,height:0.9,fill:'#1d2730'});}
txt('the record as received',SY+SH+20,12.5,'#6d6a62','italic');
const leg=el('g',{});
el('line',{x1:X,y1:SY+SH+46,x2:X+28,y2:SY+SH+46,stroke:'#c4492f','stroke-width':1.6,'stroke-linecap':'round'},leg);
const lt=el('text',{x:X+36,y:SY+SH+50,'font-size':12.5,fill:'#6d6a62','font-style':'italic'},leg);
lt.textContent='a tide’s high waters (hypothetical)';
</script>
</body>
</html>
'''
open('/tmp/claude-0/s128/mk/m01/work/index.html','w').write(html.replace('__DATA__',data))
