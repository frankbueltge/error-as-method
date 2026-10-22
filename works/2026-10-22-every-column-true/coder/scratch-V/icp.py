import sys,pickle,csv
n=sys.argv[1]
def dms(t): return int(t[:-6])+int(t[-6:-4])/60+int(t[-4:])/360000
r=list(csv.DictReader(open('data/bridges.csv')))
B=[(dms(b['LONG_017']),dms(b['LAT_016']),b) for b in r]
comps=[c for c in pickle.load(open('comps_%s.pkl'%n,'rb')) if c[4]<150]
G=[((c[0]+c[2])/2,c[3],c) for c in comps]
a,bb,c,d=-392,177+392*75.5186,-523.3,110+523.3*39.689
def fit(xs,ys):
  n=len(xs);mx=sum(xs)/n;my=sum(ys)/n
  sxx=sum((x-mx)**2 for x in xs);sxy=sum((x-mx)*(y-my) for x,y in zip(xs,ys))
  k=sxy/sxx;return k,my-k*mx
for it in range(15):
  pairs=[]
  for gx,gy,cc in G:
    best=min(B,key=lambda t:(a*t[0]+bb-gx)**2+(c*t[1]+d-gy)**2)
    e=((a*best[0]+bb-gx)**2+(c*best[1]+d-gy)**2)**.5
    pairs.append((gx,gy,best,e,cc))
  good=[p for p in pairs if p[3]<6]
  a,bb=fit([p[2][0] for p in good],[p[0] for p in good])
  c,d=fit([p[2][1] for p in good],[p[1] for p in good])
  print(it,len(good),round(a,1),round(c,1),sum(p[3] for p in good)/len(good))
pickle.dump((a,bb,c,d,pairs),open('icp_%s.pkl'%n,'wb'))
