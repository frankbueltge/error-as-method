import json, math
from PIL import Image, ImageDraw, ImageChops
Q=json.load(open('series.json')); N=len(Q); vmax=max(Q); SM=1.2
S=2; W,H=1100*S,800*S
cx,cy,r0,step=610,400,56,5.0
def val(t):
  i=math.floor(t); f=t-i
  a=Q[max(0,min(N-1,i))]; b=Q[max(0,min(N-1,i+1))]; u=f*f*(3-2*f); return (a+(b-a)*u)/vmax
stops=[(0,(70,28,12)),(0.25,(150,62,20)),(0.5,(222,128,44)),(0.75,(245,200,118)),(1,(255,246,226))]
def col(v,al):
  v=max(0,min(1,v));k=0
  while k<len(stops)-2 and v>stops[k+1][0]: k+=1
  p,c1=stops[k];q,c2=stops[k+1];u=(v-p)/(q-p)
  return tuple(int((c1[j]+(c2[j]-c1[j])*u)*al) for j in range(3))
def pos(t,off):
  turns=(t-SM)/24; th=turns*2*math.pi; r=r0+step*turns+off
  return ((cx-r*math.sin(th))*S,(cy+r*math.cos(th))*S)
base=Image.new('RGB',(W,H),(10,12,17)); d=ImageDraw.Draw(base)
pts=[pos(t/10,0) for t in range(0,(N-1)*10)]
d.line(pts,fill=(28,32,40),width=1)
light=Image.new('RGB',(W,H),(0,0,0)); dl=ImageDraw.Draw(light)
sub=10
for s in range((N-1)*sub):
  t0=s/sub;t1=(s+1)/sub;v0=val(t0);v1=val(t1)
  if v0<0.004 and v1<0.004: continue
  w0=0.35+4.9*v0**0.75; w1=0.35+4.9*v1**0.75
  v=(v0+v1)/2
  dl.polygon([pos(t0,-w0/2),pos(t1,-w1/2),pos(t1,w1/2),pos(t0,w0/2)],fill=col(v,0.35+0.6*min(1,v*1.4)))
out=ImageChops.add(base,light).resize((1100,800),Image.LANCZOS)
out.save('preview.png')
