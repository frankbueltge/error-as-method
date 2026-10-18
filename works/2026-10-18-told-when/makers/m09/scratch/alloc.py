import json, math
D=json.load(open('occ.json')); occ=D['occ']; W=len(occ); L=18
x0,x1=3.0,296.0
def at(x):
    i=int(math.floor(x)); f=x-i
    a=occ[max(0,min(W-1,i))]; b=occ[max(0,min(W-1,i+1))]
    return [(1-f)*a[k]+f*b[k] for k in range(L)]
hours=[]
for h in range(1464):
    x=x0+h*(x1-x0)/1463
    v=at(x); m=max(v)
    v=[u if u>0.18*m else 0 for u in v]; t=sum(v)
    hours.append([u/t for u in v])
# mean level per hour (level index, 0 = highest)
ml=[sum(k*f for k,f in enumerate(hv)) for hv in hours]
# fold: detrend by 24h centered mean
fold=[0]*24; n=[0]*24
for h in range(12,1464-12):
    m=sum(ml[h-12:h+12])/24
    fold[h%24]+=ml[h]-m; n[h%24]+=1
print('fold (neg = higher value):',[round(fold[i]/n[i],2) for i in range(24)])
days=[]
for d in range(61):
    s=[sum(hours[h][k] for h in range(24*d,24*d+24)) for k in range(L)]
    fl=[math.floor(u) for u in s]; rem=24-sum(fl)
    order=sorted(range(L),key=lambda k:-(s[k]-fl[k]))
    for k in order[:rem]: fl[k]+=1
    days.append(fl)
for d,f in enumerate(days): print(d, ''.join('.' if c==0 else (str(c) if c<10 else chr(55+c)) for c in f))
json.dump(days,open('days.json','w'))
