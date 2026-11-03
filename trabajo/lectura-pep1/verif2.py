import numpy as np, statsmodels.api as sm
from math import log, exp
d=sm.datasets.spector.load_pandas().data
X=sm.add_constant(d[['GPA','TUCE','PSI']]); y=d['GRADE']
mpl=sm.OLS(y,X).fit(); ph=mpl.predict(X); print('MPL',mpl.params.round(4).tolist(),'neg',(ph<0).sum(),ph.min().round(4))
m=sm.Logit(y,X).fit(disp=0); p=m.predict(X)
from sklearn.metrics import roc_auc_score
