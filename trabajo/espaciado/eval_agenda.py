import sys,os;sys.argv=['x'];import joint as J
AG={'Ma':['M2','M3'],'Mb':['M7','M5','M9'],'Mc':['M1','M2','M7'],'Md':['M7','M8','M2','M5','M3'],
'Me':['M1','M2','M3','M4','M5','M6','M7','M8','M9'],'Mf':['M1','M7','M6'],'Mi':['M7','M2','M4']}
P={**J.CUR,**AG}; c=J.costo(P); mc=J.montecarlo(P,2000)
print(os.environ.get('V3'),'Micro agenda',sum(c[s] for s in AG),'min',mc, 'factible',J.factible(P,10**4))
d={}
for s in J.SL: d[s[5]]=d.get(s[5],0)+c[s[0]]
print(d)
