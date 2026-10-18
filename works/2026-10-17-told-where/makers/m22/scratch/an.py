from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m22/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
d=[[255-px[x,y] for x in range(W)] for y in range(H)]
# column profile of baseline rows
for x in range(W):
    s=sum(d[y][x] for y in (82,83,84,85))
    print(x, s, max(d[y][x] for y in range(H)), min((y for y in range(H) if d[y][x]>80),default=-1))
