# Optimizador conjunto Econometria II + Microeconomia II (ambas PEP el jue 12-11)
# Extiende opt.py/opt2.py: FSRS-6 con ganancia x g, q por Beta, recocido simulado, Monte Carlo.
import os, math, random, sys, json, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
DEC=0.1542; F=0.9**(-1/DEC)-1
R=lambda t,S:(1+F*max(t,0)/S)**-DEC
def gain(S,Rr,g):
    inc=math.exp(1.8722)*6*S**-0.1666*(math.exp(0.796*(1-Rr))-1)
    return S*(1+g*inc)
# ---------- temas ----------
# id: (materia, peso, S hoy [0=nuevo], dias desde el ultimo repaso, q, n evidencia, min/rep, min extra 1.a vez)
E={'T1':(.85,3,0,.80,35,6),'T2':(.75,2,0,.65,6,6),'T3':(.30,2,0,.80,6,4),'T4':(.35,0,0,.35,2,9),
'T5':(.50,2.5,0,.85,7,6),'T6':(.30,0,0,.30,2,9),'T7':(.80,1.5,0,.65,6,8),'T8':(.25,1,0,.60,4,8),
'T9':(.25,3,0,.85,6,3),'T10':(.80,3,0,.88,8,7),'T11':(.50,1.5,0,.70,4,4),'T12':(.35,2,0,.55,4,6),
'T13':(.20,5,0,.70,5,8),'T14':(.60,2,0,.70,12,6)}

# PEP de DOS bloques (08:15-11:10): pesos de la columna «Dos bloques» y temas nuevos T15/T16
W2={'T1': 0.9, 'T2': 0.85, 'T3': 0.5, 'T4': 0.7, 'T5': 0.75, 'T6': 0.6, 'T7': 0.9, 'T8': 0.35, 'T9': 0.5, 'T10': 0.9, 'T11': 0.75, 'T12': 0.65, 'T13': 0.3, 'T14': 0.8}
for k,w in W2.items(): E[k]=(w,)+E[k][1:]
E['T15']=(.25,0,0,.50,2,6)   # probit a mano con tabla Phi (nuevo)
E['T16']=(.15,0,0,.45,2,4)   # primeras diferencias (Fatalities), conceptual (nuevo)
# Micro: peso = puntos esperados de 60 (prediccion 04-11 §2-§4 normalizada); S/dias/q desde el Control 1 (22-10) y ayudantias
M={'M1':(12.8,3,17,.55,4,30),   # 3.er grado vs precio unico, demanda quebrada, excluir grupo (matematico)
'M2':(8.1,1,15,.30,5,15),       # dos partes y 2.o grado (C2 1/5 en el Control 1)
'M3':(4.4,1,15,.35,4,8),        # 1.er grado, PIE, Pareto (C3 1/5, D1 3/10)
'M4':(7.0,10,15,.88,10,8),      # monopolio, Lerner, elasticidad, monopolio natural (37/40)
'M5':(6.0,1,14,.50,2,10),        # competencia monopolistica CP/LP, exceso de capacidad
'M6':(3.7,1,14,.50,2,8),        # Hotelling: centro vs 1/4-3/4
'M7':(13.8,0,0,.45,2,15),       # juegos estaticos: matriz 3x3, dominancia iterada, EN, dilema, puras
'M8':(2.2,0,0,.35,2,12),        # secuenciales: arbol, induccion hacia atras (peso x0,7: no se sabe si entra)
'M9':(1.1,0,0,.40,2,6)}         # paquetes
LEARN={'T4':18,'T6':18,'T15':18,'T16':18,'M7':45,'M8':25,'M9':10}
TOP={**{k:('E',)+v for k,v in E.items()},**{k:('M',)+v for k,v in M.items()}}
K=list(TOP)
# ---------- franjas: (id, materia, etiqueta, t en dias desde vie 10:00, cupo, dia, sueño despues) ----------
SL=[('A','E','vie 11:10',0.049,60,'vie',0),('Ma','M','vie 17:00',0.292,25,'vie',0),('B','E','vie 16:00',0.25,90,'vie',0),
('C','E','vie 22:30',0.521,15,'vie',1),
('D','E','sab 13:00',1.125,45,'sab',0),('Mb','M','sab 16:00',1.25,90,'sab',0),
('E','E','dom 13:00',2.125,40,'dom',0),('Mc','M','dom 16:00',2.25,60,'dom',0),
('F','E','lun 12:00',3.083,45,'lun',0),('Md','M','lun 20:00',3.417,90,'lun',0),
('G','E','mar 13:00',4.125,65,'mar',0),('Me','M','mar 15:00',4.208,120,'mar',0),
('H','E','mie 12:45',5.115,40,'mie',0),('Mf','M','mie 18:30',5.354,60,'mie',0),
('I','E','mie 22:30',5.521,15,'mie',1),
('J','E','jue 06:45',5.865,30,'jue',0),('Mi','M','jue 13:10',6.132,25,'jue',0)]
SL.sort(key=lambda s:s[3]); ORD=[s[0] for s in SL]
DAYCAP={'vie':150,'sab':140,'dom':120,'lun':130,'mar':170,'mie':105,'jue':115}
if os.environ.get('V3')=='420': DAYCAP['vie']=190   # opcionales del viernes: excede el tope (se avisa)
EXAM={'E':5.96,'M':6.156}
NEWBY={'T4':'E','T6':'E','T15':'E','T16':'E','M7':'Mb','M8':'Md','M9':'Md'}   # nuevo: aprendido a mas tardar en esa franja (Cepeda 2008: 1.a pasada el fin de semana)
def nota_E(p): return 1+3*p/.6 if p<.6 else min(7,4+3*(p-.6)/.4)   # 60 %
def nota_M(p): return 1+3*p/.5 if p<.5 else min(7,4+3*(p-.5)/.5)   # 50 % (42/60 = 5,2)
def evaluar(plan,par,estoc=False,rng=random):
    num={'E':0,'M':0}
    for k in K:
        m=TOP[k][0]; w=TOP[k][1]; S=par['S'][k]; q=par['q'][k]; last=-TOP[k][3]
        for (s,ms,_,t,_,_,zz) in SL:
            if ms!=m or k not in plan[s]: continue
            if S==0: S=1.0*(par['sleep'] if zz else 1); q=q+0.45*(0.95-q); last=t; continue
            Rr=R(t-last,S); p=Rr*q
            Ss=gain(S,Rr,par['g'])*(par['sleep'] if zz else 1); Sf=max(0.4,0.35*S)
            if estoc: S=Ss if rng.random()<p else Sf
            else: S=p*Ss+(1-p)*Sf
            q=q+0.25*(0.95-q); last=t
        Rx=R(EXAM[m]-last,S) if S>0 else 0.0
        num[m]+=w*Rx*q
    pE=num['E']/sum(v[0] for v in E.values())*par['presE']
    pM=num['M']/sum(v[0] for v in M.values())*par['presM']
    return nota_E(pE),nota_M(pM)
def obj(plan,par): a,b=evaluar(plan,par); return (a+b)/2
def costo(plan):
    vistos=set(); tot={}
    for (s,*_) in SL:
        c=0
        for k in plan[s]:
            c+=TOP[k][6]+(LEARN.get(k,0) if k not in vistos else 0); vistos.add(k)
        tot[s]=c
    return tot
def factible(plan,B):
    c=costo(plan)
    if sum(c.values())>B: return False
    day={}; vistos={}
    for (s,ms,_,t,cap,d,_) in SL:
        if c[s]>cap: return False
        day[d]=day.get(d,0)+c[s]
        for k in plan[s]:
            if TOP[k][0]!=ms: return False
            if TOP[k][2]==0 and k not in vistos and ORD.index(s)>ORD.index(NEWBY[k]): return False
            if d=='jue' and ((vistos.get(k,0)<2 and TOP[k][2]<3) or TOP[k][6]>15): return False   # jueves: solo calentamiento corto (Sievertsen 2016)
            vistos[k]=vistos.get(k,0)+1
    return all(day[d]<=DAYCAP[d] for d in day)
MEAN={'g':0.4,'presE':0.90,'presM':0.86,'sleep':1.2,'S':{k:TOP[k][2] for k in K},'q':{k:TOP[k][4] for k in K}}
def vacio(): return {s[0]:[] for s in SL}
def optimizar(B,iters,seed):
    rng=random.Random(seed); plan=vacio()
    while True:
        base=obj(plan,MEAN); cand=None
        for (s,ms,*_) in SL:
            for k in K:
                if TOP[k][0]!=ms or k in plan[s]: continue
                p2={a:b[:] for a,b in plan.items()}; p2[s].append(k)
                if not factible(p2,B): continue
                d=(obj(p2,MEAN)-base)/(TOP[k][6]+LEARN.get(k,0))
                if cand is None or d>cand[0]: cand=(d,p2)
        if not cand or cand[0]<=1e-7: break
        plan=cand[1]
    cur=plan; fc=obj(cur,MEAN); best=(fc,cur); Tt=0.01
    for _ in range(iters):
        p2={a:b[:] for a,b in cur.items()}; s=rng.choice(SL); op=rng.random()
        if op<.35 and p2[s[0]]: p2[s[0]].pop(rng.randrange(len(p2[s[0]])))
        elif op<.7:
            k=rng.choice([k for k in K if TOP[k][0]==s[1]])
            if k in p2[s[0]]: continue
            p2[s[0]].append(k)
        else:
            s2=rng.choice([x for x in SL if x[1]==s[1]])
            if not p2[s[0]]: continue
            k=p2[s[0]].pop(rng.randrange(len(p2[s[0]])))
            if k in p2[s2[0]]: continue
            p2[s2[0]].append(k)
        if not factible(p2,B): continue
        f2=obj(p2,MEAN)
        if f2>fc or rng.random()<math.exp((f2-fc)/Tt): cur,fc=p2,f2
        if fc>best[0]: best=(fc,{a:b[:] for a,b in cur.items()})
        Tt*=0.9998
    return best[1]
def montecarlo(plan,n=2000):
    rng=random.Random(1); a=[];b=[]
    for _ in range(n):
        par={'g':rng.uniform(.25,.6),'presE':rng.uniform(.83,.96),'presM':rng.uniform(.78,.92),'sleep':rng.uniform(1.0,1.4),
             'S':{k:(0 if TOP[k][2]==0 else TOP[k][2]*math.exp(rng.gauss(0,.4))) for k in K},
             'q':{k:rng.betavariate(TOP[k][4]*(TOP[k][5]+2),(1-TOP[k][4])*(TOP[k][5]+2)) for k in K}}
        x,y=evaluar(plan,par,True,rng); a.append(x); b.append(y)
    def res(v): v=sorted(v); return [round(st.mean(v),2),round(v[int(.1*n)],2),round(v[int(.9*n)],2),round(sum(x>=5 for x in v)/n,2)]
    return res(a),res(b)
import os
V3=json.load(open('v3_'+os.environ.get('V3','360')+'.json'))
# plan actual: econ v2 (opt2) + Micro 8,5 h aproximado en las franjas
CUR={'A':['T6','T4'],'B':['T7','T14','T1'],'C':['T2','T3'],'D':['T8','T12','T7','T11'],'E':['T2','T8','T3','T7','T5'],
'F':['T7','T11','T4','T6','T2'],'G':['T11','T14','T9','T13','T1','T2','T12','T8'],'H':['T6','T10','T8','T4','T3'],
'I':['T1','T5','T9'],'J':['T14','T7','T2','T12','T11'],
'Ma':[],'Mb':[],'Mc':[],'Md':['M1','M2','M3','M4','M5','M6','M7'],'Me':['M1','M2','M7','M8'],'Mf':['M1','M5','M6','M7','M2','M4','M3'],
'Mi':['M1','M4','M3']}
CUR.update(V3)
if __name__=='__main__':
    def show(P,tag):
        c=costo(P); mc=montecarlo(P); tE=sum(c[s[0]] for s in SL if s[1]=='E'); tM=sum(c[s[0]] for s in SL if s[1]=='M')
        print(f'\n{tag}: {sum(c.values())} min (E {tE}, M {tM})  Econ MC media/p10/p90/P≥5 {mc[0]}  Micro {mc[1]}  prom {round((mc[0][0]+mc[1][0])/2,2)}')
        dd={}
        for (s,ms,lab,t,cap,d,_) in SL: dd[d]=dd.get(d,0)+c[s]
        print('  carga diaria', dd)
        for (s,ms,lab,*_) in SL: print(f'  {s:3s} {lab} {c[s]:3d} min: {", ".join(P[s])}')
        return mc
    print('actual (sin topes)'); show(CUR,'ACTUAL')
    budgets=[int(a) for a in sys.argv[1:]] or [700,600,520,450,380]
    out={}
    for B in budgets:
        cands=[(montecarlo(P,500),P) for P in (optimizar(B,40000,100+sd) for sd in range(4))]
        P=max(cands,key=lambda x:x[0][0][0]+x[0][1][0])[1]
        print('reinicios',[round(x[0][0][0]+x[0][1][0],2) for x in cands])
        show(P,f'B={B}'); out[B]=P
    json.dump(out,open('joint_res.json','w'))
