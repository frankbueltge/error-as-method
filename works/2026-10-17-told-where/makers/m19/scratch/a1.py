from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m19/work/record.jpg').convert('L'); p=im.load()
W,H=im.size
# floor ink per column
fl=[sum(255-p[x,y] for y in range(82,86)) for x in range(W)]
up=[sum(max(0,200-p[x,y]) for y in range(0,81)) for x in range(W)]
# blocks: runs where fl > half of max
mx=max(fl); thr=mx*0.5
runs=[];x=0
while x<W:
  if fl[x]>thr:
    s=x
    while x<W and fl[x]>thr: x+=1
    # subpixel width via ink sum / plateau
    ink=sum(fl[s-1:x+1]); runs.append((s,x-1,ink/mx))
  else: x+=1
print(len(runs), 'max',mx)
for i,r in enumerate(runs): print(i,r[0],r[1],round(r[2],2), round((r[0]+r[1])/2,1))
