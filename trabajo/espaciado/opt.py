import math, random, sys, statistics as st
random.seed(7)
# ---------- datos ----------
# tema: (peso P(sale), S hoy [0=nuevo], q hoy (prob. de ejecutarlo bien si se recuerda), n evidencia, min por repeticion)
T={'T1':(.85,3,.80,35,6),'T2':(.75,2,.65,6,6),'T3':(.30,2,.80,6,4),'T4':(.35,0,.35,2,9),
'T5':(.50,2.5,.85,7,6),'T6':(.30,0,.30,2,9),'T7':(.80,1.5,.65,6,8),'T8':(.25,1,.60,4,8),
'T9':(.25,3,.85,6,3),'T10':(.80,3,.88,8,7),'T11':(.50,1.5,.70,4,4),'T12':(.35,2,.55,4,6),
'T13':(.20,5,.70,5,8),'T14':(.60,2,.70,12,6)}
K=list(T); LEARN=18  # minutos extra la primera vez de un tema nuevo (pretest+pauta+criterio)
# franjas (dias desde vie 10:00), cupo maximo en min, sueño despues
SL=[('A','vie 11:00',0.042,60,0),('B','vie 16:00',0.25,90,0),('C','vie 22:30',0.52,15,1),
('D','sab 13:00',1.125,40,0),('E','dom 13:00',2.125,40,0),('F','lun 12:00',3.083,40,0),
('G','mar 13:00',4.125,60,0),('H','mie 12:45',5.115,40,0),('I','mie 22:30',5.52,15,1),('J','jue 06:45',5.865,30,0)]
EX=5.927
CUR={'A':['T1','T2','T5','T7','T10','T11','T14','T8','T3'],'B':['T4','T6','T13','T2'],'C':['T4','T6'],
'D':['T7','T11','T12','T8'],'E':['T2','T14','T4'],'F':['T7','T1','T10','T6'],'G':['T11','T5','T2','T8','T12','T4','T9'],
'H':['T7','T6','T3'],'I':['T14','T8'],'J':['T11','T4']}
DEC=0.1542; F=0.9**(-1/DEC)-1
R=lambda t,S:(1+F*t/S)**-DEC
def gain(S,Rr,g):  # FSRS-6, D=5, incremento escalado por g
    inc=math.exp(1.8722)*6*S**-0.1666*(math.exp(0.796*(1-Rr))-1)
    return S*(1+g*inc)
def nota(p): return 1+3*p/.6 if p<.6 else min(7,4+3*(p-.6)/.4)
def evaluar(plan,par,estoc=False):
    g,pres,sleep=par['g'],par['pres'],par['sleep']
    num=0; W=sum(T[k][0] for k in K)
    for k in K:
        w=T[k][0]; S=par['S'][k]; q=par['q'][k]; last=0.0
        for (s,_,t,_,zz) in SL:
            for _ in range(plan[s].count(k)):
                if S==0: S=1.0*(1.25 if zz else 1); q=q+0.45*(0.95-q); last=t; continue
                Rr=R(t-last,S); p=Rr*q
                Ss=gain(S,Rr,g)*(sleep if zz else 1); Sf=max(0.4,0.35*S)
                if estoc: S=Ss if random.random()<p else Sf
                else: S=p*Ss+(1-p)*Sf
                q=q+0.25*(0.95-q); last=t
        Rx=R(EX-last,S) if S>0 else 0.0
        num+=w*Rx*q
    return nota(num/W*pres), num/W*pres
def costo(plan,par=None):
    vistos=set(); tot={}
    for (s,*_ ) in SL:
        m=0
        for k in plan[s]:
            m+=T[k][4]+(LEARN if T[k][1]==0 and k not in vistos else 0); vistos.add(k)
        tot[s]=m
    return tot
MEAN={'g':0.4,'pres':0.92,'sleep':1.2,'S':{k:T[k][1] for k in K},'q':{k:T[k][2] for k in K}}
def factible(plan,B):
    c=costo(plan)
    if sum(c.values())>B: return False
    for (s,_,_,cap,_) in SL:
        if c[s]>cap: return False
        if any(plan[s].count(k)>2 for k in K): return False
    return True
def optimizar(B,iters=40000):
    plan={s[0]:[] for s in SL}; best=None
    # voraz: agrega la (franja,tema) con mayor ganancia/minuto
    while True:
        base=evaluar(plan,MEAN)[1]; cand=None
        for (s,*_) in SL:
            for k in K:
                p2={a:b[:] for a,b in plan.items()}; p2[s].append(k)
                if not factible(p2,B): continue
                d=(evaluar(p2,MEAN)[1]-base)/(T[k][4]+ (LEARN if T[k][1]==0 else 0))
                if cand is None or d>cand[0]: cand=(d,p2)
        if not cand or cand[0]<=1e-6: break
        plan=cand[1]
    # recocido: mover / quitar / agregar / cambiar
    cur=plan; fc=evaluar(cur,MEAN)[1]; best=(fc,cur); Tt=0.004
    for it in range(iters):
        p2={a:b[:] for a,b in cur.items()}; s=random.choice(SL)[0]; op=random.random()
        if op<.35 and p2[s]: p2[s].pop(random.randrange(len(p2[s])))
        elif op<.7: p2[s].append(random.choice(K))
        else:
            s2=random.choice(SL)[0]
            if p2[s]: p2[s2].append(p2[s].pop(random.randrange(len(p2[s]))))
        if not factible(p2,B): continue
        f2=evaluar(p2,MEAN)[1]
        if f2>fc or random.random()<math.exp((f2-fc)/Tt): cur,fc=p2,f2
        if fc>best[0]: best=(fc,{a:b[:] for a,b in cur.items()})
        Tt*=0.99993
    return best[1]
def montecarlo(plan,n=3000):
    rng=random.Random(1); out=[]
    for _ in range(n):
        par={'g':rng.uniform(.25,.6),'pres':rng.uniform(.85,.97),'sleep':rng.uniform(1.0,1.4),
             'S':{k:(0 if T[k][1]==0 else T[k][1]*math.exp(rng.gauss(0,.4))) for k in K},
             'q':{k:rng.betavariate(T[k][2]*(T[k][3]+2),(1-T[k][2])*(T[k][3]+2)) for k in K}}
        random.seed(rng.random())
        out.append(evaluar(plan,par,estoc=True)[0])
    out.sort(); m=st.mean(out)
    return m,out[int(.1*n)],out[int(.9*n)],sum(x>=5 for x in out)/n,sum(x>=5.5 for x in out)/n
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    Bcur=sum(costo(CUR).values())
    print('plan actual: min modelo',Bcur, 'nota media',round(evaluar(CUR,MEAN)[0],2),'MC',[round(x,2) for x in montecarlo(CUR)])
    import json; res={}
    for B in [Bcur,300,240,180]:
        P=optimizar(B); c=costo(P)
        mc=montecarlo(P)
        print(f'\nB={B} usa {sum(c.values())} min  nota media {evaluar(P,MEAN)[0]:.2f}  MC media/p10/p90/P≥5/P≥5.5 {[round(x,2) for x in mc]}')
        for (s,lab,*_) in SL: print(f'  {s} {lab} {c[s]:3d} min: {", ".join(P[s])}')
        res[B]=P
    json.dump(res,open('opt_res.json','w'))
