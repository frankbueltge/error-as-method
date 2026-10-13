from PIL import Image
im=Image.open('../work/record.jpg').convert('L'); w,h=im.size; px=im.load()
# column mean height of ink (value proxy): mean (90-y) weighted by darkness
col=[]
for x in range(w):
    s=sum(max(0,220-px[x,y]) for y in range(h)); col.append(sum((h-y)*max(0,220-px[x,y]) for y in range(h))/s if s else None)
xs=[x for x in range(4,296)]
def score(P,nb=34):
    bins=[[] for _ in range(nb)]
    for x in xs:
        bins[int(((x/P)%1)*nb)].append(col[x])
    m=[sum(b)/len(b) for b in bins if b]
    g=sum(m)/len(m); return sum((v-g)**2 for v in m)/len(m)
best=sorted((score(P/100),P/100) for P in range(3300,3550,5))[-6:]
print(best)
bestd=sorted((score(P/1000,10),P/1000) for P in range(4700,5100,10))[-6:]
print(bestd)
P=4.82; nb=10
bins=[[] for _ in range(nb)]
for x in xs: bins[int(((x/P)%1)*nb)].append(col[x])
print([round(sum(b)/len(b),1) for b in bins])
W=33.74; nb=14
bins=[[] for _ in range(nb)]
for x in xs: bins[int(((x/W)%1)*nb)].append(col[x])
print([round(sum(b)/len(b),1) for b in bins])
