import json,math
from PIL import Image,ImageDraw
D=json.load(open('embed.json'))
L=2*D['p'];FX0,FW,TOP,PITCH=170,760,92,10
S=2
def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
stops=[(-18,(222,206,166)),(0,(110,150,158)),(18,(18,40,63))]
def col(v):
  if v>21: return lerp((176,72,44),(120,30,20),min(1,(v-21)/30))
  if v<=stops[0][0]: return stops[0][1]
  for (a,ca),(b,cb) in zip(stops,stops[1:]):
    if v<=b: return lerp(ca,cb,(v-a)/(b-a))
  return stops[-1][1]
im=Image.new('RGBA',(1100*S,800*S),(243,239,230,255))
ov=Image.new('RGBA',im.size,(0,0,0,0));dr=ImageDraw.Draw(ov)
pts=sorted(D['pts'],key=lambda q:-q[1])  # low values first
vals=[]
for xi,yi,v in pts:
  x,y=xi/100,yi/100;t=(x-D['x_start'])/L;r=math.floor(t);u=t-r
  val=D['mean']-y; vals.append(val)
  for uu in (u,u-1,u+1):
    px=FX0+uu*FW
    if px<FX0-20 or px>FX0+FW+20: continue
    py=TOP+r*PITCH-max(-4,min(4,val*0.2))
    w=13;h=3.4
    c=col(val)
    dr.rounded_rectangle([(px-w)*S,(py-h)*S,(px+w)*S,(py+h)*S],radius=h*S,fill=c+(200,))
im=Image.alpha_composite(im,ov)
# clip margins
d2=ImageDraw.Draw(im)
d2.rectangle([0,0,(FX0-1)*S,800*S],fill=(243,239,230,255));d2.rectangle([(FX0+FW+1)*S,0,1100*S,800*S],fill=(243,239,230,255))
im.convert('RGB').resize((1100,800),Image.LANCZOS).save('prev2.png')
vals.sort();print(vals[:5],vals[len(vals)//20],vals[len(vals)//2],vals[-len(vals)//20],vals[-15:])
