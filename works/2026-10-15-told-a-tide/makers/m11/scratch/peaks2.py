import json, math
pts=json.load(open('peaks.json'))
xs=[p[0] for p in pts]; print('x extent',min(xs),max(xs),'y extent',min(p[1] for p in pts),max(p[1] for p in pts))
x0,x1=min(xs),max(xs)
def t(x): return (x-x0)/(x1-x0)*1463
# weighted value per peak: v = 89 - y ; weight = mass
W=sum(p[2] for p in pts); mv=sum((89-p[1])*p[2] for p in pts)/W
res=[]
for i in range(300):
  P=22.5+i*0.01
  re=sum(p[2]*((89-p[1])-mv)*math.cos(2*math.pi*t(p[0])/P) for p in pts)
  im=sum(p[2]*((89-p[1])-mv)*math.sin(2*math.pi*t(p[0])/P) for p in pts)
  res.append((re*re+im*im,P))
res.sort(reverse=True); print([(round(P,2)) for _,P in res[:5]])
# peak at 24 exactly power ratio
d=dict((round(P,2),p) for p,P in res); print('pow 24.00 / best', d[24.0]/res[0][0])
