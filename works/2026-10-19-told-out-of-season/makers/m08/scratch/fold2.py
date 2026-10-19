from PIL import Image
g=Image.open('/tmp/claude-0/s137/mk/m08/work/record.jpg').convert('L'); px=g.load()
W,H=g.size
x0,x1=2.0,297.0
cs={}
for x in range(2,298):
    ws=[(max(0,170-px[x,y]),y) for y in range(H)]
    s=sum(w for w,_ in ws)
    if s: cs[x]=sum(w*y for w,y in ws)/s
for (a,b) in [(3,130),(136,205),(215,297)]:
    bins={}
    for x in range(a+5,b-5):
        nb=[cs[i] for i in range(x-5,x+6) if i in cs]
        d=-(cs[x]-sum(nb)/len(nb))  # up positive
        h=((x-x0)/(x1-x0)*1463)%24
        bins.setdefault(int(h//2),[]).append(d)
    print(a,b,' '.join(f'{k*2:02d}h:{sum(v)/len(v):+.1f}' for k,v in sorted(bins.items())))
