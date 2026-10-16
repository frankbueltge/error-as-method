from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m11/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
d=[[max(0,255-p[x,y]) for y in range(H)] for x in range(W)]
# row histogram
rows=[sum(d[x][y] for x in range(W)) for y in range(H)]
for y in range(H):
    print(y, rows[y], '*'*(rows[y]//400))
tot=sum(sum(c) for c in d)
print('total ink',tot, 'per value', tot/1464)
