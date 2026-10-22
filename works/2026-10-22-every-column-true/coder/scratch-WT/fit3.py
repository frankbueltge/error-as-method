import sys,subprocess
src=open('fit.py').read().split('img=sys.argv')[0]
exec(src)
img=sys.argv[1]; kys=range(int(sys.argv[2]),int(sys.argv[3]),4); x0s=range(int(sys.argv[4]),int(sys.argv[5]),2); y0s=range(int(sys.argv[6]),int(sys.argv[7]),2)
w,h=1100,800
raw=subprocess.run(['convert',img,'-depth','8','rgb:-'],capture_output=True).stdout
bg=raw[15:18]
ink=set()
for y in range(h):
  for x in range(0,400):
    i=(y*w+x)*3
    if sum(abs(raw[i+k]-bg[k]) for k in range(3))>60: ink.add((x,y))
best=None
for ky in kys:
  for x0 in x0s:
    for y0 in y0s:
      kx=ky*0.775; hit=0
      for la,lo in pts:
        X=int(x0+(75.5186-lo)*kx); Y=int(y0+(39.6889-la)*ky)
        if any((X+dx,Y+dy) in ink for dx in (-1,0,1) for dy in (-3,-2,-1,0,1)): hit+=1
      if best is None or hit>best[0]: best=(hit,ky,x0,y0)
print(img,best)
