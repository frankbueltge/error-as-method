from PIL import Image
g=Image.open('/tmp/claude-0/s133/mk/m15/work/record.jpg').convert('L'); W,H=g.size
P=[[255-g.getpixel((x,y)) for x in range(W)] for y in range(H)]
# darkness in bottom band rows 83-84
bot=[ (P[83][x]+P[84][x])/2 for x in range(W)]
print(' '.join('%d'%(b//26) for b in bot))
# find runs > threshold
runs=[];x=0
while x<W:
  if bot[x]>100:
    s=x
    while x<W and bot[x]>100: x+=1
    runs.append((s,x-1, sum(bot[s-1 if s>0 else 0:x+1])/255))
  else: x+=1
print(len(runs)); print(runs)
