import base64
d=open('px.raw','rb').read();W,H=480,220
b=bytearray()
n=0
for y in range(H):
  for x in range(3,477):
    v=d[y*W+x]
    if v<215:
      w=255-v
      p=(x<<15)|(y<<7)|(w>>1); b+=p.to_bytes(3,'big'); n+=1
open('pts.b64','w').write(base64.b64encode(bytes(b)).decode()); print(n)
