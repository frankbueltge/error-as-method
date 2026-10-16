from PIL import Image; import numpy as np
a=np.asarray(Image.open('/tmp/claude-0/s131/mk/m14/work/record.jpg').convert('L')).astype(float)
m=a<160
cols=np.where(m.any(0))[0]; rowsany=np.where(m.any(1))[0]
print('x',cols.min(),cols.max(),'y',rowsany.min(),rowsany.max())
top=np.array([np.where(m[:,x])[0].min() if m[:,x].any() else np.nan for x in range(300)])
bot=np.array([np.where(m[:,x])[0].max() if m[:,x].any() else np.nan for x in range(300)])
cnt=m.sum(0)
s=np.nan_to_num(bot-np.nanmean(bot))
ac=[np.corrcoef(s[:-k],s[k:])[0,1] for k in range(1,30)]
for k,v in enumerate(ac,1): print(k,round(v,2))
np.save('top.npy',top); np.save('bot.npy',bot)
print(' '.join(str(int(t)) if t==t else '-' for t in top))
print(' '.join(str(int(t)) if t==t else '-' for t in bot))
