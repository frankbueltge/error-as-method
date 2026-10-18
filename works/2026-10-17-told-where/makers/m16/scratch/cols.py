from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m16/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
ink=[[255-px[x,y] for y in range(H)] for x in range(W)]
bot=[ink[x][83]+ink[x][84] for x in range(W)]
dk=[x for x in range(W) if bot[x]>150]
print('bottom first/last',dk[0],dk[-1])
print(''.join(str(min(9,b//50)) for b in bot))
# ink above row 81
up=[sum(ink[x][y] for y in range(0,81)) for x in range(W)]
print(''.join(str(min(9,b//150)) for b in up))
# top-most dark per column
top=[next((y for y in range(81) if ink[x][y]>90),None) for x in range(W)]
print(top)
