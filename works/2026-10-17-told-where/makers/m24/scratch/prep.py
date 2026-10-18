import json, math
f=json.load(open('fit_2.1_0.85.json')); ys=f['ys']
Z=84.0; TOP=6.0
v=[max(0.0,(Z-y)/(Z-TOP)) for y in ys]
v=[0.0 if a<0.6/(Z-TOP) else min(1,a) for a in v]
# solar noon index from circular centroid of mean profile
prof=[sum(v[h::24])/len(v[h::24]) for h in range(24)]
sx=sum(p*math.cos(2*math.pi*h/24) for h,p in enumerate(prof)); sy=sum(p*math.sin(2*math.pi*h/24) for h,p in enumerate(prof))
noon=(math.atan2(sy,sx)/(2*math.pi)*24)%24
print('noon index',noon)
# solar time
t=[i-noon+12 for i in range(len(v))]  # hours from solar midnight of day0
days={}
for i,a in enumerate(v):
    d=math.floor(t[i]/24); days.setdefault(d,[]).append((t[i]-24*d,a))
ds=sorted(days)
print('days',ds[0],ds[-1],len(ds))
nz=[(d,sum(1 for _,a in days[d] if a>0)) for d in ds if len(days[d])==24]
n=len(nz);mx=sum(d for d,_ in nz)/n;my=sum(c for _,c in nz)/n
b=sum((d-mx)*(c-my) for d,c in nz)/sum((d-mx)**2 for d,_ in nz);a0=my-b*mx
print('nz fit',a0,b,'-> start',a0,'end',a0+b*60)
# daily peak envelope (upper)
pk=[(d,max(a for _,a in days[d])) for d in ds if len(days[d])==24]
# noon-hours mean of top 3
top=[(d,sorted([a for _,a in days[d]])[-3:]) for d in ds if len(days[d])==24]
for d,tt in top[::5]: print(d,['%.2f'%x for x in tt])
json.dump({'v':[round(a*99) for a in v],'noon':noon,'nzA':a0,'nzB':b},open('data.json','w'))
