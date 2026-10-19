import json,sys
Y=[90-v for v in json.load(open('/tmp/claude-0/s137/mk/m17/scratch/q.json'))]
data=','.join(str(round(v*10)) for v in Y)
P=dict(R0=sys.argv[1] if len(sys.argv)>1 else '362', R1=sys.argv[2] if len(sys.argv)>2 else '62', K=sys.argv[3] if len(sys.argv)>3 else '0.95')
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Run-out Groove</title>
<style>
html,body{margin:0;height:100%;background:#eee8dc}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
svg{display:block;width:100vw;height:100vh;max-width:1100px;max-height:800px}
</style></head><body>
<svg id="w" viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg" role="img"
 aria-label="Sixty-one days of hourly readings drawn as one spiral groove, one turn per day, from the outer edge inward; the groove is as wide as the reading is large."></svg>
<script>
// 1,464 hourly values re-traced from the source dot plot (tenths of a pixel of its height; larger = higher).
const V=[__DATA__].map(v=>v/10);
const NS='http://www.w3.org/2000/svg', svg=document.getElementById('w');
const PAPER='#eee8dc', INK='#1b1a17', FAINT='#b9b0a0';
const el=(n,a)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);svg.appendChild(e);return e};
el('rect',{x:0,y:0,width:1100,height:800,fill:PAPER});
const CX=550, CY=388, R0=__R0__, R1=__R1__, N=V.length;
const pitch=(R0-R1)/(N/24);           // radial distance between successive days
const K=__K__*pitch/84;               // groove width per unit of reading
const SUB=6;
// angle: one full turn per 24 readings, clockwise, the first reading at twelve o'clock
const ang=t=>-Math.PI/2+2*Math.PI*t/24, rad=t=>R0-pitch*t/24;
function val(t){const i=Math.floor(t),f=t-i;const a=V[Math.min(N-1,i)],b=V[Math.min(N-1,i+1)];
  // cubic Hermite (Catmull-Rom) between hours
  const p0=V[Math.max(0,i-1)],p3=V[Math.min(N-1,i+2)];
  const m1=(b-p0)/2,m2=(p3-a)/2,f2=f*f,f3=f2*f;
  return (2*f3-3*f2+1)*a+(f3-2*f2+f)*m1+(-2*f3+3*f2)*b+(f3-f2)*m2;}
// faint guide: the bare spiral, so the groove's path is legible where it is thin
let g='';for(let s=0;s<=(N-1)*SUB;s++){const t=s/SUB,r=rad(t),a=ang(t);g+=(s?'L':'M')+(CX+r*Math.cos(a)).toFixed(2)+' '+(CY+r*Math.sin(a)).toFixed(2);}
el('path',{d:g,fill:'none',stroke:FAINT,'stroke-width':0.45});
// the groove: one closed outline, outer edge forward, inner edge back
const outer=[],inner=[];
for(let s=0;s<=(N-1)*SUB;s++){const t=s/SUB,r=rad(t),a=ang(t),w=Math.max(0.35,K*Math.max(0,val(t)-2))/2;
  outer.push([CX+(r+w)*Math.cos(a),CY+(r+w)*Math.sin(a)]);inner.push([CX+(r-w)*Math.cos(a),CY+(r-w)*Math.sin(a)]);}
const pts=outer.concat(inner.reverse());
el('path',{d:'M'+pts.map(p=>p[0].toFixed(2)+' '+p[1].toFixed(2)).join('L')+'Z',fill:INK});
const font='Georgia, "Times New Roman", serif';
const t1=el('text',{x:40,y:772,fill:INK,'font-family':font,'font-size':14,'letter-spacing':'0.3'});t1.textContent='Run-out Groove';
const t2=el('text',{x:1060,y:772,fill:'#6f685c','text-anchor':'end','font-family':font,'font-size':11.5,'font-style':'italic'});
t2.textContent='61 days, one turn each, read from the rim inward · the groove widens with the reading';
</script>
</body></html>
'''
for k,v in P.items(): html=html.replace('__%s__'%k,v)
open('/tmp/claude-0/s137/mk/m17/work/index.html','w').write(html.replace('__DATA__',data))
