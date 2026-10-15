import json
c=json.load(open('cal.json'))
s=open('template.html').read().replace('__DOTS__',open('dots.txt').read()).replace('__X0__',repr(c['x0'])).replace('__HPP__',repr(c['hpp']))
open('../work/index.html','w').write(s)
