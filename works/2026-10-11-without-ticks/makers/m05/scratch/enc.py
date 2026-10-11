import base64
W,H=480,220
b=open('births.raw','rb').read()
X0,X1,Y0,Y1=5,475,24,198
out=bytearray()
for y in range(Y0,Y1):
  for x in range(X0,X1):
    v=255-b[y*W+x]
    v=0 if v<28 else v
    out.append(v)
open('ink.b64','w').write(base64.b64encode(bytes(out)).decode())
print(X1-X0,Y1-Y0,len(out))
