# Econometria fija (plan v2, sesiones A-J) + Micro optimizado alrededor, con topes diarios y reglas de la literatura
import sys, math, random, json
sys.argv=['x']; import joint as J
from joint import *
MS=[s for s in SL if s[1]=='M']
def optimizar_M(BM,iters,seed):
    rng=random.Random(seed); plan={a:(b[:] if a in [s[0] for s in SL if s[1]=='E'] else []) for a,b in CUR.items()}
    BE=sum(costo(plan).values()); B=BE+BM
    while True:
        base=obj(plan,MEAN); cand=None
        for (s,ms,*_) in MS:
            for k in K:
                if TOP[k][0]!='M' or k in plan[s]: continue
                p2={a:b[:] for a,b in plan.items()}; p2[s].append(k)
                if not factible(p2,B): continue
                d=(obj(p2,MEAN)-base)/(TOP[k][6]+LEARN.get(k,0))
                if cand is None or d>cand[0]: cand=(d,p2)
        if not cand or cand[0]<=1e-7: break
        plan=cand[1]
    cur=plan; fc=obj(cur,MEAN); best=(fc,cur); Tt=0.01
    MK=[k for k in K if TOP[k][0]=='M']
    for _ in range(iters):
        p2={a:b[:] for a,b in cur.items()}; s=rng.choice(MS)[0]; op=rng.random()
        if op<.35 and p2[s]: p2[s].pop(rng.randrange(len(p2[s])))
        elif op<.7:
            k=rng.choice(MK)
            if k in p2[s]: continue
            p2[s].append(k)
        else:
            s2=rng.choice(MS)[0]
            if not p2[s]: continue
            k=p2[s].pop(rng.randrange(len(p2[s])))
            if k in p2[s2]: continue
            p2[s2].append(k)
        if not factible(p2,B): continue
        f2=obj(p2,MEAN)
        if f2>fc or rng.random()<math.exp((f2-fc)/Tt): cur,fc=p2,f2
        if fc>best[0]: best=(fc,{a:b[:] for a,b in cur.items()})
        Tt*=0.9998
    return best[1]
if __name__=='__main__':
    print('econ v2 sola: minutos',sum(c for s,c in costo(CUR).items() if s[0]!='M'))
    out={}
    for BM in [int(a) for a in sys.argv[1:]] if len(sys.argv)>1 else [330,390,450,510]:
        cands=[(montecarlo(P,500),P) for P in (optimizar_M(BM,40000,200+sd) for sd in range(4))]
        print('\nreinicios',[round(x[0][1][0],2) for x in cands])
        P=max(cands,key=lambda x:x[0][1][0])[1]
        c=costo(P); mc=montecarlo(P); tM=sum(c[s[0]] for s in MS)
        dd={}
        for (s,ms,lab,t,cap,d,_) in SL: dd[d]=dd.get(d,0)+c[s]
        print(f'BM={BM}: Micro {tM} min  Econ {mc[0]}  Micro {mc[1]}  prom {round((mc[0][0]+mc[1][0])/2,2)}  carga {dd}')
        for (s,ms,lab,*_) in MS: print(f'  {s:3s} {lab} {c[s]:3d} min: {", ".join(P[s])}')
        out[BM]=P
    json.dump(out,open('joint2_res.json','w'))
