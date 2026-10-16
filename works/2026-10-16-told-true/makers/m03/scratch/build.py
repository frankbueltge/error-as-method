import sys
d=open('/tmp/claude-0/s130/mk/m03/scratch/data.txt').read()
t=open('/tmp/claude-0/s130/mk/m03/scratch/tpl.html').read()
R0,S,A,DOT,out=sys.argv[1:6]
open(out,'w').write(t.replace('%%DATA%%',d).replace('%%R0%%',R0).replace('%%S%%',S).replace('%%A%%',A).replace('%%DOT%%',DOT))
