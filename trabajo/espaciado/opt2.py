import sys, random, json
sys.argv=['x']; import opt
from opt import *
ORD=[s[0] for s in SL]
def factible(plan,B):
    c=costo(plan)
    if sum(c.values())>B: return False
    vistos={}
    for (s,_,_,cap,_) in SL:
        if c[s]>cap or len(set(plan[s]))<len(plan[s]): return False   # intercalado: 1 vez por sesion
        for k in plan[s]:
            if T[k][1]==0 and k not in vistos and ORD.index(s)>ORD.index('E'): return False  # nuevo: aprenderlo antes del lunes
            if s=='J' and vistos.get(k,0)<2 and T[k][1]<3: return False  # jueves: solo lo ya repasado
            vistos[k]=vistos.get(k,0)+1
    return True
opt.factible=factible
sys.stdout.reconfigure(encoding='utf-8')
Bcur=sum(costo(CUR).values()); res={}
print('actual',Bcur,'min MC',[round(x,2) for x in montecarlo(CUR)])
for B in [Bcur,270,240,210]:
    cands=[]
    for sd in range(4):
        random.seed(100+sd); P=optimizar(B,30000); cands.append((montecarlo(P,800)[0],P))
    P=max(cands,key=lambda x:x[0])[1]; c=costo(P); mc=montecarlo(P)
    print(f'\nB={B} usa {sum(c.values())} min  MC media/p10/p90/P≥5/P≥5.5 {[round(x,2) for x in mc]}  (reinicios: {[round(x[0],2) for x in cands]})')
    for (s,lab,*_) in SL: print(f'  {s} {lab} {c[s]:3d} min: {", ".join(P[s])}')
    res[B]=P
json.dump(res,open('opt2_res.json','w'))
