from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m20/work/record.jpg').convert('L')
w,h=im.size; px=im.load()
P=4.820057; c0=3.884
# for each column, phase relative to night center
bins=[[0,0,0] for _ in range(24)]
for x in range(w):
    ph=((x-c0)/P)%1.0
    b=int(ph*24)
    for y in range(0,81):
        d=max(0,255-px[x,y]-30)
        bins[b][0]+=d; bins[b][1]+=d*(83.5-y)
    bins[b][2]+=1
for i,(s,m,n) in enumerate(bins):
    print(i, round(s/n), round(m/s,1) if s else '-')
