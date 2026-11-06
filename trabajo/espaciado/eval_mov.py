import sys;sys.argv=['x'];import joint as J
from eval_agenda import AG
AG2={**AG,'Ma':[],'Mb':AG['Mb']+['M2','M3']}
for nom,a in [('agenda',AG),('mu1 al sabado',AG2)]:
    P={**J.CUR,**a}; mc=J.montecarlo(P,2000); c=J.costo(P); d={}
    for s in J.SL: d[s[5]]=d.get(s[5],0)+c[s[0]]
    print(nom,mc,d['vie'],d['sab'])
