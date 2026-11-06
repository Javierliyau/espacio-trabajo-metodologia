exec(open('opt3.py',encoding='utf-8').read().split("v2={a:b")[0])
import json
v2=json.load(open('opt2_res.json'))['308']
def aumentar(plan,B):
    plan={a:b[:] for a,b in plan.items()}
    while True:
        base=evaluar(plan,MEAN)[1]; cand=None
        for (s,*_) in SL:
            for k in K:
                p2={a:b[:] for a,b in plan.items()}; p2[s].append(k)
                if not opt.factible(p2,B): continue
                d=(evaluar(p2,MEAN)[1]-base)/(T[k][4]+(LEARN if T[k][1]==0 and all(k not in v for v in plan.values()) else 0))
                if cand is None or d>cand[0]: cand=(d,p2,s,k)
        if not cand or cand[0]<=1e-6: return plan
        plan=cand[1]
for B in [360,420]:
    P=aumentar(v2,B); c=costo(P); mc=montecarlo(P)
    print(f'v2+agregados B={B}: {sum(c.values())} min MC {[round(x,2) for x in mc]}')
    for (s,lab,*_) in SL:
        extra=[k for k in P[s] if k not in v2[s]]
        print(f'  {s} {c[s]:3d} min  +{extra}')
    json.dump(P,open(f'v3_{B}.json','w'))
