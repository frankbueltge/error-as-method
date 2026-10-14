import json
f=json.load(open('fit.json'))
h=open('tpl_final.html').read()
h=(h.replace('__PX__',open('pts.txt').read()).replace('__DT__',open('blobs.txt').read())
 .replace('__LV__',json.dumps([d['b'] for d in f['days']])).replace('__P__',repr(295/61.0)).replace('__PH0__','0.33'))
open('/tmp/claude-0/s124/mk/m10/work/index.html','w').write(h)
