import json
from PIL import Image, ImageDraw
H=[o['hours'] for o in json.load(open('fold.json'))]
stops=[[0,[22,25,40]],[0.06,[52,30,48]],[0.2,[120,40,36]],[0.4,[188,84,34]],[0.6,[228,142,52]],[0.8,[246,204,120]],[1,[255,246,222]]]
def col(v):
  v=max(0,min(1,v))
  for i in range(1,len(stops)):
    if v<=stops[i][0]:
      a,b=stops[i-1],stops[i];t=(v-a[0])/(b[0]-a[0]);return tuple(round(c+(b[1][j]-c)*t) for j,c in enumerate(a[1]))
  return tuple(stops[-1][1])
def val(row,h):
  i=int(h//1);t=h-i;p=lambda k:row[max(0,min(23,k))]
  p0,p1,p2,p3=p(i-1),p(i),p(i+1),p(i+2)
  return max(0,0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
L,R,T,B=170,930,128,642;n=len(H);rowH=(B-T)/n;gap=max(1.4,rowH*0.2)
im=Image.new('RGB',(1100,800),(11,12,18));d=ImageDraw.Draw(im)
for r in range(n):
  y=T+r*rowH;h=rowH-gap
  for x in range(L,R):
    sh=(x-L+0.5)/(R-L)*24
    if (r==0 and sh<16.5) or (r==n-1 and sh>16.5): continue
    d.rectangle([x,round(y),x,round(y+h)-1],fill=col(val(H[r],sh)))
im.save('preview.png')
