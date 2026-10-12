import json
d=json.load(open('series.json')); pix=open('pix.txt').read().strip()
t=open('template.html').read()
t=t.replace('/*V*/',','.join(f'{x:g}' for x in d['v'])).replace('/*PIX*/',pix).replace('/*HW*/',f"{d['hw']:.3f}").replace('/*ENV*/',','.join(map(str,d['env'])))
open('../work/index.html','w').write(t)
print(len(t))
