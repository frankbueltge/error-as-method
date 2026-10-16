from PIL import Image; import numpy as np, json
a=np.asarray(Image.open('/tmp/claude-0/s131/mk/m17/work/record.jpg').convert('L')).astype(float)
H,W=a.shape
d=a<140
cent=[np.where(d[:,x])[0].mean() if d[:,x].any() else np.nan for x in range(W)]
cent=np.array(cent)
seq=[]
for x in range(W):
    ys=list(np.where(d[:,x])[0])
    if not ys: continue
    p=cent[x-1] if x>0 and not np.isnan(cent[x-1]) else cent[x]
    n=cent[x+1] if x<W-1 and not np.isnan(cent[x+1]) else cent[x]
    # value up = y down. if moving to smaller y, order descending y
    ys.sort(reverse=bool(n<p))
    for k,y in enumerate(ys):
        seq.append((x+(k+0.5)/len(ys), y))
seq=np.array(seq)
print(len(seq), 'cols with ink', np.sum(~np.isnan(cent)))
# resample to 1464 by index
idx=np.linspace(0,len(seq)-1,1464)
y=np.interp(idx,np.arange(len(seq)),seq[:,1])
v=(H-1-y)  # value in px units, up=high
# period check via autocorrelation
vv=v-v.mean()
ac=[np.corrcoef(vv[:-l],vv[l:])[0,1] for l in range(1,60)]
print('best lag', 1+int(np.argmax(ac[10:]))+10, [round(c,2) for c in ac[18:30]])
json.dump([round(float(t),2) for t in v],open('series.json','w'))
dd=v.reshape(61,24)
print('daily mean range',dd.mean(1).min(),dd.mean(1).max())
print('mean hour profile',np.round(dd.mean(0)-dd.mean(),1))
print('daily amp', np.round(dd.max(1)-dd.min(1),0))
xi=(np.arange(1464)+0.5)*W/1464
y2=np.interp(xi,seq[:,0],seq[:,1])
v2=H-1-y2
dd=v2.reshape(61,24)
print('profile2',np.round(dd.mean(0)-dd.mean(),1))
print('day means',np.round(dd.mean(1)))
print('min/max',v2.min(),v2.max())
json.dump([round(float(t),2) for t in v2],open('series2.json','w'))
for x0,x1 in [(2,297),(1.5,297),(2.5,296.5)]:
    xi=x0+(np.arange(1464)+0.5)*(x1-x0)/1464
    v3=H-1-np.interp(xi,seq[:,0],seq[:,1])
    dd=v3.reshape(61,24)
    pr=dd.mean(0)-dd.mean(); print(x0,x1,'profile amp',round(pr.max()-pr.min(),1))
xi=2+(np.arange(1464)+0.5)*295/1464
v3=H-1-np.interp(xi,seq[:,0],seq[:,1])
dd=v3.reshape(61,24)
print(np.round(dd.mean(0)-dd.mean(),1))
json.dump([round(float(t),1) for t in v3],open('series3.json','w'))
