import json,statistics as st
cols=json.load(open('cols.json'))
H=90; N=1464; SPAN=294.3; hpp=N/SPAN; xs0=149.5-SPAN/2; x0,x1=2,297
cent=[];med=[];top=[]
for x in range(x0,x1+1):
    c=cols[x]
    ys=[y for y,d in c for _ in range(max(1,d//50))]
    cent.append((x+0.5-xs0)*hpp); med.append(st.median(ys)); top.append(min(y for y,_ in c))
def interp(t):
    if t<=cent[0]: return med[0]
    if t>=cent[-1]: return med[-1]
    i=int((t-cent[0])//hpp); i=max(0,min(i,len(cent)-2))
    f=(t-cent[i])/hpp; return med[i]*(1-f)+med[i+1]*f
vals=[H-interp(h+0.5) for h in range(N)]  # larger = higher value
lo,hi=sorted(vals)[int(.02*N)],sorted(vals)[int(.98*N)]
q=[max(0,min(255,round((v-lo)/(hi-lo)*255))) for v in vals]
# spikes: columns whose topmost dot stands well above the column median
spikes=[]
for i,(m,t) in enumerate(zip(med,top)):
    if m-t>=14: spikes.append([round(cent[i],1), round((H-t-lo)/(hi-lo),2)])
print(len(spikes),lo,hi)
json.dump({'q':q,'spikes':spikes},open('series.json','w'))
