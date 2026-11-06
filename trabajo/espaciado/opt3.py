import sys, random, json
sys.argv=['x']; import opt
src=open('opt2.py',encoding='utf-8').read(); exec(src[:src.index('opt.factible=factible')+len('opt.factible=factible')])
from opt import *
# pesos para DOS bloques (prediccion 31-10 §4, columna «Dos bloques»)
W2={'T1':.90,'T2':.85,'T3':.50,'T4':.70,'T5':.75,'T6':.60,'T7':.90,'T8':.35,'T9':.50,'T10':.90,'T11':.75,'T12':.65,'T13':.30,'T14':.80}
for k,w in W2.items(): T[k]=(w,)+T[k][1:]
T['T15']=(.25,0,.50,2,6)   # probit a mano con tabla Φ (nuevo)
T['T16']=(.15,0,.45,2,4)   # primeras diferencias (Fatalities) conceptual (nuevo)
K[:]=list(T); MEAN['S'].update({'T15':0,'T16':0}); MEAN['q'].update({'T15':.5,'T16':.45})
opt.EX=5.96
sys.stdout.reconfigure(encoding='utf-8')
v2={a:b for a,b in json.load(open('opt2_res.json'))['308'].items()}
print('v2 (1 bloque) evaluado con pesos de 2 bloques:',sum(costo(v2).values()),'min',[round(x,2) for x in montecarlo(v2)])
res={}
for B in [307,360,420]:
    cands=[]
    for sd in range(4):
        random.seed(200+sd); P=optimizar(B,30000); cands.append((montecarlo(P,800)[0],P))
    P=max(cands,key=lambda x:x[0])[1]; c=costo(P); mc=montecarlo(P)
    print(f'\nB={B} usa {sum(c.values())} min MC media/p10/p90/P≥5/P≥5.5 {[round(x,2) for x in mc]} reinicios {[round(x[0],2) for x in cands]}')
    for (s,lab,*_) in SL: print(f'  {s} {lab} {c[s]:3d}: {", ".join(P[s])}')
    res[B]=P
json.dump(res,open('opt3_res.json','w'))
