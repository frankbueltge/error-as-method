from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m10/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
d=[[255-p[x,y] for x in range(W)] for y in range(H)]
# baseline profile
base=[ (d[83][x]+d[84][x])/2 for x in range(W)]
print(''.join('#' if b>150 else ('+' if b>80 else '.') for b in base))
# first/last dark column overall
cols=[sum(d[y][x] for y in range(H)) for x in range(W)]
print([x for x in range(W) if cols[x]>200][:5],[x for x in range(W) if cols[x]>200][-5:])
rows=[sum(d[y][x] for x in range(W)) for y in range(H)]
print([ (y,rows[y]) for y in range(H) if rows[y]>800])
