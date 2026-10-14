import json
cols=json.loads(open('/tmp/claude-0/s124/mk/m09/scratch/px.txt').read().splitlines()[-1])
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=1100">
<title>Forty Widths</title>
<style>
html,body{margin:0;background:#f4f1ea;}
canvas{display:block;}
</style></head><body>
<canvas id="c" width="1100" height="800"></canvas>
<script>
// The 480 grey values of record.jpg, column by column (left to right), top to bottom.
var P=%s;
var c=document.getElementById('c'),x=c.getContext('2d');
var dpr=window.devicePixelRatio||1;c.width=1100*dpr;c.height=800*dpr;c.style.width='1100px';c.style.height='800px';x.scale(dpr,dpr);
x.fillStyle='#f4f1ea';x.fillRect(0,0,1100,800);
var L=70,T=118,CW=20,G=4,CH=46,N=40,R=12;
function cx(i){return L+i*(CW+G);}
// JPEG 8x8 blocks: faint ground where the compressor made its decisions
x.fillStyle='rgba(120,110,95,0.06)';
for(var bx=0;bx<5;bx++)for(var by=0;by<2;by++){if((bx+by)%%2)continue;
  var x0=cx(bx*8)-G/2,x1=cx(Math.min(bx*8+8,N))-G/2,y0=T+by*8*CH,y1=T+Math.min(by*8+8,R)*CH;
  x.fillRect(x0,y0-6,x1-x0,y1-y0+12);}
// the material itself: every pixel, as found
for(var i=0;i<N;i++)for(var j=0;j<R;j++){var v=P[i][j];
  x.fillStyle='rgb('+v+','+v+','+v+')';
  if(v>=246)continue; // white stays the page
  x.fillRect(cx(i),T+j*CH,CW,CH-1);}
// envelope: where each column turns dark (threshold 128, sub-pixel by partial darkness)
function edges(col){var t=null,b=null;
  for(var j=0;j<R;j++)if(col[j]<128){t=j-(j>0?(255-col[j-1])/255:0);break;}
  for(var j=R-1;j>=0;j--)if(col[j]<128){b=j+1+(j<R-1?(255-col[j+1])/255:0);break;}
  return [t,b];}
var E=P.map(edges);
x.strokeStyle='#c2391b';x.lineWidth=1.25;
[0,1].forEach(function(k){x.beginPath();
  for(var i=0;i<N;i++){var y=T+E[i][k]*CH;x.moveTo(cx(i)-1,y);x.lineTo(cx(i)+CW+1,y);
    if(i<N-1){var y2=T+E[i+1][k]*CH;x.moveTo(cx(i)+CW+1,y);x.lineTo(cx(i+1)-1,y2);}}
  x.stroke();});
// width of the swing, column by column, as a quiet bar row beneath
var B=T+R*CH+40;
for(var i=0;i<N;i++){var wv=E[i][1]-E[i][0];x.fillStyle='#c2391b';
  x.fillRect(cx(i)+CW/2-1,B,2,wv*5);}
// words
x.fillStyle='#2a2622';x.font='600 22px Georgia, "Times New Roman", serif';
x.fillText('Forty Widths',L,62);
x.fillStyle='#6d665c';x.font='italic 14px Georgia, "Times New Roman", serif';
x.fillText('A record too dense for its picture: each of the 40 columns holds many values, and only their reach survives.',L,86);
x.font='12px Georgia, serif';
x.fillText('grey: the 480 pixels of the file, as found      red: where each column turns dark',L,B+68);
x.fillText('below: how far each column swings',L+640,B+68);
</script></body></html>'''%json.dumps(cols,separators=(',',':'))
open('/tmp/claude-0/s124/mk/m09/work/index.html','w').write(html)
