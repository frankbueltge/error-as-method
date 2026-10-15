import json,math
cols=json.load(open('cols.json'))
x0,x1=2.5,295.5;hpp=1463/(x1-x0)
for P in (24.06,24.84,12.42):
  B=[[] for _ in range(12)];T=[[] for _ in range(12)]
  for i,r in enumerate(cols):
    if not r: continue
    t=(i-x0)*hpp; b=int((t%P)/P*12)
    B[b].append(max(r));T[b].append(min(r))
  print(P,'bot',[round(sum(v)/len(v),1) for v in B],'top',[round(sum(v)/len(v),1) for v in T])
# halves
for lo,hi in ((0,150),(150,300)):
  xs=[((i-x0)*hpp,max(r)) for i,r in enumerate(cols) if r and lo<=i<hi]
  m=sum(v for _,v in xs)/len(xs);best=max(((lambda c,s:c*c+s*s)(sum((v-m)*math.cos(2*math.pi*t/P) for t,v in xs),sum((v-m)*math.sin(2*math.pi*t/P) for t,v in xs)),P) for P in [k/100 for k in range(2000,2800,2)])
  print(lo,hi,best[1])
# spring-neap check: amplitude of spread at 354h
xs=[((i-x0)*hpp,max(r)-min(r)) for i,r in enumerate(cols) if r]
m=sum(v for _,v in xs)/len(xs)
for P in (200,250,300,354,400,500,700):
  c=sum((v-m)*math.cos(2*math.pi*t/P) for t,v in xs);s=sum((v-m)*math.sin(2*math.pi*t/P) for t,v in xs);print('spread',P,round(2*math.hypot(c,s)/len(xs),2))
