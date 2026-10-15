from PIL import Image
import math
im=Image.open('/tmp/claude-0/s128/mk/m02/work/record.jpg').convert('L'); px=im.load()
W,H=im.size; x0=2.5; hpp=1463/294.0
for P in (24.0,23.93,24.84,23.5,25.82,12.42):
    best=None
    NB=6; acc=[[0]*H for _ in range(NB)]
    for x in range(W):
        t=(x-x0)*hpp
        b=int((t%P)/P*NB)%NB
        for y in range(H): acc[b][y]+=max(0,235-px[x,y])
    means=[]
    for b in range(NB):
        s=sum(acc[b]); means.append(sum(y*acc[b][y] for y in range(H))/s)
    amp=max(means)-min(means)
    print(P,'amp %.1f'%amp,' '.join('%.0f'%m for m in means))
P=24.0;NB=6;acc=[[0]*H for _ in range(NB)]
for x in range(W):
    t=(x-x0)*hpp; b=int((t%P)/P*NB)%NB
    for y in range(H): acc[b][y]+=max(0,235-px[x,y])
for y in range(0,90,2):
    row=''
    for b in range(NB):
        v=(acc[b][y]+acc[b][y+1]); m=max(max(a) for a in acc)*2
        row+=' .:-=+*#%@'[min(9,int(10*v/m))]*2
    print('%2d '%y+row)
# overall vertical histogram
tot=[sum(max(0,235-px[x,y]) for x in range(W)) for y in range(H)]
T=sum(tot); c=0
for y in range(H):
    c+=tot[y]
    if y%5==4: print(y,'%.2f'%(c/T))
