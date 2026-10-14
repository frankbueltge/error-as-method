import json, sys
f=json.load(open('fit.json')); pts=open('blobs.txt').read()
P=295/61.0
B=[d['b'] for d in f['days']]
prm=dict(MODE=1,PH0=0.33,K=7.0,DOT=1.6,AL=0.55)
if len(sys.argv)>2: prm.update(json.loads(sys.argv[2]))
html=open('tpl3.html').read()
html=(html.replace('__PTS__',pts).replace('__B__',json.dumps(B)).replace('__P__',repr(P)).replace('__PRM__',json.dumps(prm)))
open(sys.argv[1],'w').write(html)
