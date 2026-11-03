import numpy as np, statsmodels.api as sm
from math import log, exp
d=sm.datasets.spector.load_pandas().data
X=sm.add_constant(d[['GPA','TUCE','PSI']]); y=d['GRADE'].values
mpl=sm.OLS(y,X).fit(); ph=mpl.predict(X); print('MPL',mpl.params.round(4).tolist(),'neg',(ph<0).sum(),round(ph.min(),4))
m=sm.Logit(y,X).fit(disp=0); p=m.predict(X).values
pos=p[y==1]; neg=p[y==0]; auc=np.mean([(a>b)+0.5*(a==b) for a in pos for b in neg]); print('AUC',auc,'Gini',2*auc-1)
# calculator path with rounded means
z0=-13.0213+2.8261*3.117+0.0952*21.938; z1=z0+2.3787
for z in (z0,z1): print('z %.4f e^-z %.4f P %.4f'%(z,exp(-z),1/(1+exp(-z))))
P0=1/(1+exp(-z0));P1=1/(1+exp(-z1)); print('diff',P1-P0, 'g0',P0*(1-P0),'g1',P1*(1-P1),'me0',P0*(1-P0)*2.8261,'me1',P1*(1-P1)*2.8261)
print('2.8261 x 3.117=',2.8261*3.117,' 0.0952 x 21.938=',0.0952*21.938)
# German credit cuenta
B=[99,111,34,237];M=[94,82,13,30];TB,TM=sum(B),sum(M);iv=0
for b,mm in zip(B,M):
  pb,pm=b/TB,mm/TM; w=log(pb/pm); iv+=(pb-pm)*w; print('GC %.4f %.4f rate %.3f WOE100 %.1f iv %.4f'%(pb,pm,mm/(b+mm),100*w,(pb-pm)*w))
print('GC IV',iv,TB,TM,TM/(TB+TM))
# Siddiqi
S=[('Perdido',860,140),('18-22',3040,960),('23-26',4920,1080),('27-29',8100,900),('30-34',9500,500),('35-43',6800,200),('44+',2940,60)]
TB=sum(s[1] for s in S);TM=sum(s[2] for s in S);iv=0
for n,b,mm in S:
  pb,pm=b/TB,mm/TM; w=log(pb/pm); iv+=(pb-pm)*w; print('%s pb %.4f pm %.4f share %.3f rate %.3f WOE %.3f WOE100 %.1f iv %.4f'%(n,pb,pm,(b+mm)/40000,mm/(b+mm),w,100*w,(pb-pm)*w))
print('Sidd IV',iv,TB,TM)
print('30-34 ratio',0.2627/0.1302, log(0.2627/0.1302)*100)
print('T59',(101*0.26+257*0.33)/358, 101*.26,257*.33)
# scorecard lamina 7
print('sc',85+80+93+55)
# DiD CK
print('CK',(21.03-20.44)-(21.17-23.33),2.75/1.34, 20.44-2.16)
# SLEP invented
Ts,Ts2,Cs,Cs2=255,262,249,254
did=(Ts2-Ts)-(Cs2-Cs); print('SLEP did',did,'b0',Cs,'b1',Ts-Cs,'b2',Cs2-Cs,'post gap',Ts2-Cs2,'t',did/2.5, 'cf',Ts+(Cs2-Cs))
print('odds50',1/51)
