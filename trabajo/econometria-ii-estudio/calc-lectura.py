import warnings; warnings.filterwarnings('ignore')
import numpy as np, statsmodels.api as sm, openpyxl
from scipy.stats import norm
d=sm.datasets.spector.load_pandas().data
print('n',len(d),'mediaY',d.GRADE.mean(), 'PSI', d.PSI.mean(), 'GPA', d.GPA.mean(),'TUCE',d.TUCE.mean())
X=sm.add_constant(d[['GPA','TUCE','PSI']]); m=sm.Logit(d.GRADE,X).fit(disp=0)
print(m.summary2().tables[1].round(4)); print('LL',m.llf,'LL0',m.llnull,'LR',m.llr,'McF',m.prsquared)
L=lambda z:np.exp(z)/(1+np.exp(z))
b=m.params
for psi in (0,1):
    z=b['const']+b['GPA']*3.0+b['TUCE']*25+b['PSI']*psi; print('psi',psi,'z',z,'P',L(z))
xb=np.array([1,d.GPA.mean(),d.TUCE.mean(),d.PSI.mean()]); z=xb@b.values; p=L(z); print('medias z',z,'P',p,'g',p*(1-p),'EPeP GPA',p*(1-p)*b['GPA'],'TUCE',p*(1-p)*b['TUCE'])
ph=m.predict(X); g=ph*(1-ph); print('EPP GPA',(g*b['GPA']).mean(),'TUCE',(g*b['TUCE']).mean(),'g medio',g.mean())
X1=X.copy();X1['PSI']=1;X0=X.copy();X0['PSI']=0; print('EPP PSI discreto',(m.predict(X1)-m.predict(X0)).mean())
for c in (.5,.3,.7):
    yh=(ph>=c).astype(int);tp=((yh==1)&(d.GRADE==1)).sum();fn=((yh==0)&(d.GRADE==1)).sum();fp=((yh==1)&(d.GRADE==0)).sum();tn=((yh==0)&(d.GRADE==0)).sum()
    print('corte',c,'TP',tp,'FN',fn,'FP',fp,'TN',tn,'sens',tp/(tp+fn),'esp',tn/(tn+fp),'prec',tp/(tp+fp),'exac',(tp+tn)/32)
from sklearn.metrics import roc_auc_score,roc_curve
a=roc_auc_score(d.GRADE,ph);f,t,_=roc_curve(d.GRADE,ph);print('AUC',a,'Gini',2*a-1,'KS',(t-f).max())
mp=sm.OLS(d.GRADE,X).fit();pl=mp.predict(X);print('MPL',mp.params.round(4).to_dict(),'min',pl.min(),'max',pl.max(),'fuera',((pl<0)|(pl>1)).sum())
wb=openpyxl.load_workbook('C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-10-15-ejemplo-calculo-woe-iv.xlsx',data_only=True)
for r in wb['GermanCredit'].iter_rows(min_row=1,values_only=True):
    v=[(round(c,4) if isinstance(c,float) else c) for c in r if c is not None]
    if v: print(v)
