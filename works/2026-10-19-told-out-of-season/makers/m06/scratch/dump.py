from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m06/work/record.jpg').convert('L')
W,H=im.size; print(W,H)
px=im.load()
chars=' .:-=+*#%@'
for y in range(H):
    print(''.join(chars[min(9,(255-px[x,y])//26)] for x in range(W)))
