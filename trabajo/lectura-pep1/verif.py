import numpy as np, statsmodels.api as sm
d=sm.datasets.spector.load_pandas().data
X=sm.add_constant(d[['GPA','TUCE','PSI']]); y=d['GRADE']
m=sm.Logit(y,X).fit(disp=0); b=m.params; print(b.round(4)); print(m.bse.round(4)); print('n',len(y),'y1',y.sum())
gm,tm,pm=d.GPA.mean(),d.TUCE.mean(),d.PSI.mean(); print('means',gm,tm,pm)
L=lambda z:1/(1+np.exp(-z))
z0=b.const+b.GPA*gm+b.TUCE*tm; z1=z0+b.PSI
P0,P1=L(z0),L(z1); print('z0 %.4f z1 %.4f e^-z0 %.4f e^-z1 %.4f P0 %.4f P1 %.4f diff %.4f'%(z0,z1,np.exp(-z0),np.exp(-z1),P0,P1,P1-P0))
for P in (P0,P1): print('g %.4f ME %.4f ME01 %.4f'%(P*(1-P),P*(1-P)*b.GPA,P*(1-P)*b.GPA*0.1))
# exact 0.1 change
for ps in (0,1):
  za=z0+ps*b.PSI; print('exact +0.1 GPA ps',ps, L(za+0.1*b.GPA)-L(za))
zb=b.const+b.GPA*gm+b.TUCE*tm+b.PSI*pm; Pb=L(zb); print('EPeP g %.4f me %.4f Pbar %.4f'%(Pb*(1-Pb),Pb*(1-Pb)*b.GPA,Pb))
p=m.predict(X); print('EPP g %.4f me %.4f'%((p*(1-p)).mean(),(p*(1-p)).mean()*b.GPA))
print('odds',np.exp(b.PSI),100*(np.exp(b.PSI)-1),'odds0',P0/(1-P0),'odds1',P1/(1-P1),(P1/(1-P1))/(P0/(1-P0)))
print('z PSI',b.PSI/m.bse.PSI)
for c in (0.3,0.5,0.7):
  yh=(p>=c).astype(int); VP=((yh==1)&(y==1)).sum(); FN=((yh==0)&(y==1)).sum(); FP=((yh==1)&(y==0)).sum(); VN=((yh==0)&(y==0)).sum()
  S=VP/(VP+FN); E=VN/(VN+FP); Pr=VP/(VP+FP); A=(VP+VN)/32; F1=2*Pr*S/(Pr+S)
  print(c,VP,FN,FP,VN,'S %.3f E %.3f P %.3f A %.4f F1 %.3f err %.4f'%(S,E,Pr,A,F1,1-A))
print('base',21/32)
# strict >0.5
print('strict', ((p>0.5)!=(p>=0.5)).sum())
