from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m07/work/record.jpg').convert('L')
w,h=im.size;p=im.load()
D=lambda x,y:max(0,(250-p[x,y])/250)
x0=3.0; ph=293/1463; P=24*ph
days=[]
for k in range(61):
  a=x0+k*P-0.5*ph; b=a+P
  # fractional column weights
  wts={}
  for x in range(w):
    ov=max(0,min(b,x+0.5)-max(a,x-0.5))
    if ov>0: wts[x]=ov
  prof=[round(sum(wv*D(x,y) for x,wv in wts.items()),3) for y in range(0,82)]
  floor=sum(wv*D(x,y) for x,wv in wts.items() for y in (83,84))
  above=sum(prof[:80])
  top=next((y for y in range(82) if max(D(x,y) for x in wts)>0.3),None)
  days.append(dict(p=prof,f=round(floor,2),t=top))
  print(k,round(floor,2),round(above,1),top)
json.dump(days,open('days.json','w'),separators=(',',':'))
