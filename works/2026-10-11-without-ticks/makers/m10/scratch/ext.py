W,H=480,220
d=open('births.raw','rb').read()
out=[]
for x in range(W):
  for y in range(H):
    v=d[y*W+x]
    if v<215:
      q=min(15,round((255-v)/255*15))
      out.append(x*H*16+y*16+q)
print(len(out))
open('pix.txt','w').write(','.join(map(str,out)))
