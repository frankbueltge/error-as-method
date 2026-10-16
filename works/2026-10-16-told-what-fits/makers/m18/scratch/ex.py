from PIL import Image; import numpy as np, json
a=np.array(Image.open('/tmp/claude-0/s131/mk/m18/work/record.jpg').convert('L')).astype(float)
d=a<128
xs=[x for x in range(300) if d[:,x].any()]
x0,x1=xs[0],xs[-1]; print(x0,x1)
seq=[];last=None
for x in range(x0,x1+1):
    ys=list(np.where(d[:,x])[0].astype(float))
    if not ys: continue
    asc=sorted(ys); desc=asc[::-1]
    if last is None: o=desc
    else: o=asc if abs(asc[0]-last)<=abs(desc[0]-last) else desc
    for y in o: seq.append((x,y))
    last=o[-1]
print(len(seq))
# resample to 1464 by index
s=np.array([p[1] for p in seq]); t=np.linspace(0,1,len(s))
v=np.interp(np.linspace(0,1,1464),t,s)
v=(89-v)  # up = larger
v=(v-v.min())/(v.max()-v.min())
d24=v.reshape(61,24)
print(np.round(d24.mean(0),2))
print(np.argmax(d24.mean(0)),np.argmin(d24.mean(0)))
print(np.round(d24.mean(1),2))
json.dump([round(float(q),3) for q in v],open('v.json','w'))
