from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m07/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cols=[]
for x in range(2,298):
    ys=[y for y in range(H) if px[x,y]<140]
    if ys: cols.append(((x-2)*1463/295, H-max(ys)))
res=[]
P=23.5
while P<24.5:
    nb=24; b=[[] for _ in range(nb)]
    for t,v in cols: b[int((t%P)/P*nb)].append(v)
    m=[sum(a)/len(a) for a in b if a]
    mu=sum(m)/len(m); var=sum((a-mu)**2 for a in m)/len(m)
    lo=min(range(len(m)),key=lambda i:m[i])
    res.append((var,round(P,3),lo*P/nb))
    P+=0.01
print([(round(v),p) for v,p,_ in res if abs(p-round(p*10)/10)<0.006])
