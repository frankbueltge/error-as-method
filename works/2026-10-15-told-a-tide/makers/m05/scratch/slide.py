import json,math
cols=json.load(open('cols.json'))
x0,x1=2.5,295.5;hpp=1463/(x1-x0)
xs=[((i-x0)*hpp,max(r)) for i,r in enumerate(cols) if r]
P=24.05
for d0 in range(0,61,3):
  w=[(t,v) for t,v in xs if d0*24<=t<(d0+6)*24]
  if len(w)<10: continue
  m=sum(v for _,v in w)/len(w)
  c=sum((v-m)*math.cos(2*math.pi*t/P) for t,v in w);s=sum((v-m)*math.sin(2*math.pi*t/P) for t,v in w)
  print(d0, round(2*math.hypot(c,s)/len(w),1), round(math.degrees(math.atan2(s,c))))
