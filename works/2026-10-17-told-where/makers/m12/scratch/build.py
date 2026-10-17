from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m12/work/record.jpg').convert('L')
W,H=im.size
px=[[255-im.getpixel((x,y)) for x in range(W)] for y in range(H)]
pk=json.load(open('peaks.json'))
P=4.82; k=P/24; C0=-0.93; X0=2.4; X1=X0+1463*k
FL=83.5; SC=78.0; HW=0.97
fl=[px[82][x]*0.3+px[83][x]+px[84][x] for x in range(W)]
def cross(c):
  lo=max(0,int(c-2.4)); hi=min(W-1,int(c+2.4)+1)
  cols=list(range(lo,hi+1))
  m=max(fl[x] for x in cols); h=m/2
  ci=max(cols,key=lambda x:fl[x])
  L=ci
  while L>lo and fl[L-1]>=h: L-=1
  Lx = L-0.5 if L==lo else (L-1)+(h-fl[L-1])/(fl[L]-fl[L-1])
  R=ci
  while R<hi and fl[R+1]>=h: R+=1
  Rx = R+0.5 if R==hi else R+(fl[R]-h)/(fl[R]-fl[R+1])
  return Lx+HW, Rx-HW   # centres of first and last zero hour
nights={}
for n in range(1,62):
  c=C0+n*P; nights[n]=cross(c)
rings=[]
for d in range(62):
  noon=C0+d*P+P/2
  start=max(C0+d*P, X0-0.5*k); end=min(C0+(d+1)*P, X1+0.5*k)
  # lit span in hours from noon
  rise = (nights[d][1]-noon)/k+1 if d in nights else (X0-noon)/k
  sett = (nights[d+1][0]-noon)/k-1 if (d+1) in nights else (X1-noon)/k
  marks=[]
  for p in pk:
    if p['y']<82 and C0+d*P<=p['x']<C0+(d+1)*P and X0-0.6<=p['x']<=X1+0.6:
      v=max(0,min(1,(FL-p['y'])/SC))
      m=max(1,round(p['ink']/420))
      marks.append([round((p['x']-noon)/k,2),round(v,3),m])
  marks.sort()
  rings.append(dict(d=d,a=round((start-noon)/k,2),b=round((end-noon)/k,2),rise=round(rise,2),set=round(sett,2),m=marks))
for r in rings: print(r['d'],r['a'],r['b'],r['rise'],r['set'],len(r['m']),max([q[1] for q in r['m']],default=0))
json.dump(rings,open('rings.json','w'),separators=(',',':'))
