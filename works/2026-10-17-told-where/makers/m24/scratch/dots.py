from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m24/work/record.jpg').convert('L')
w,h=im.size;p=im.load()
# darkness
D=[[max(0,255-p[x,y])/255 for x in range(w)] for y in range(h)]
# column darkness excluding baseline rows
tot=[sum(D[y][x] for y in range(0,82)) for x in range(w)]
base=[sum(D[y][x] for y in range(82,86)) for x in range(w)]
print('rows with ink:', [y for y in range(h) if sum(D[y])>1][:3], [y for y in range(h) if sum(D[y])>1][-3:])
print('cols with ink:', [x for x in range(w) if sum(D[y][x] for y in range(h))>0.5][:3],[x for x in range(w) if sum(D[y][x] for y in range(h))>0.5][-3:])
print(''.join('#' if b>2 else ('+' if b>0.8 else '.') for b in base))
# total ink
print('total ink', sum(map(sum,D)), 'baseline ink', sum(base))
