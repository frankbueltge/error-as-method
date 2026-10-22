import sys,subprocess
src=open('fit.py').read().split('img=sys.argv')[0]
exec(src)
img=sys.argv[1]; w,h=1100,800
raw=subprocess.run(['convert',img,'-depth','8','rgb:-'],capture_output=True).stdout
bg=raw[15:18]
ink=set()
for y in range(h):
  for x in range(0,380):
    i=(y*w+x)*3
    if sum(abs(raw[i+k]-bg[k]) for k in range(3))>60: ink.add((x,y))
best=None
for ky in range(470,540,6):
  for x0 in range(140,170,2):
    for y0 in range(110,140,2):
      kx=ky*0.775; hit=0
      for la,lo in pts:
        X=int(x0+(75.5186-lo)*kx); Y=int(y0+(39.6889-la)*ky)
        if any((X+dx,Y+dy) in ink for dx in (-1,0,1) for dy in (-3,-2,-1,0,1)): hit+=1
      if best is None or hit>best[0]: best=(hit,ky,x0,y0)
print(img,best)
