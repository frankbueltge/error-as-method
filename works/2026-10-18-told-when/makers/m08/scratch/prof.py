from PIL import Image
im=Image.open('/tmp/claude-0/s135/mk/m08/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
for y in range(H):
    s=sum(255-p[x,y] for x in range(W))
    print(y, s, '*'*(s//300))
