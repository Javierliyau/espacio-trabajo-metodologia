# Calendario de repasos con el modelo FSRS (curva de potencia + estabilidad)
import math, sys
from datetime import datetime as dt
sys.stdout.reconfigure(encoding="utf-8")
DECAY=-0.5; FACTOR=19/81                      # FSRS-4.5/5: R(S)=0.9
w8,w9,w10,w15=1.6474,0.1367,1.0461,0.2272     # parámetros por defecto FSRS-4.5
def R(t,S): return (1+FACTOR*t/S)**DECAY
GAIN=0.4
def S_up(S,D,r,hard): return S*(1+GAIN*math.exp(w8)*(11-D)*S**(-w9)*(math.exp(w10*(1-r))-1)*(w15 if hard else 1))
EX=dt(2026,11,12,8,15)
# id: (nombre, S días, D 1-10, último repaso, minutos de repaso, peso = prob. de salir, nuevo)
T={
"T1":("Logit: P̂, signo, odds y 100(e^β−1)",3,5,dt(2026,11,5,22),7,.85,0),
"T2":("Efectos parciales: continua, dummy, cuadrático, máx 0,25β",2,7,dt(2026,11,5,22),8,.75,0),
"T3":("MPL: 4 problemas, β en pp, MPL≈β/4",2,5,dt(2026,11,3,18),4,.30,0),
"T4":("Salida de glm: z, p, RV=2(Lnr−Lr)~χ², McFadden",1.4,7,None,8,.35,1),
"T5":("Matriz de confusión: 4 métricas y mover el corte",2.5,6,dt(2026,11,5,22),6,.50,0),
"T6":("Youden, corte por utilidad, ROC/AUC, Gini=2AUC−1, KS",1.4,7,None,7,.30,1),
"T7":("WOE ×100, signo, IV, monotonía/fusión, valor del cliente",1.5,8,dt(2026,11,5,22),8,.80,0),
"T8":("Scorecard: Factor=PDO/ln2, Offset, puntos, política de corte",1.0,8,dt(2026,11,3,21),7,.25,0),
"T9":("Scoring conceptual: malo, ventana, exclusiones, KGB, train/test, PSI",3,4,dt(2026,11,5,12),4,.25,0),
"T10":("DiD 2×2 desde medias + β0-β3 + t",3,5,dt(2026,11,5,22),7,.80,0),
"T11":("DiD conceptos: tendencias paralelas, ATT, Card-Krueger",1.5,7,dt(2026,11,5,22),5,.50,0),
"T12":("Amenazas a la validez interna/externa + dirección del sesgo",2,7,dt(2026,11,5,15),5,.35,0),
"T13":("Base de Econometría I: β log/dummy, t, F, R²aj, VIF, BP, robustos",5,5,dt(2026,10,24,16),5,.20,0),
"T14":("Teoría: núcleo de 12 V/F + refuerzo fallado",2,6,dt(2026,11,5,22),8,.60,0),
}
# sesiones disponibles (inicio, minutos, etiqueta)
SL=[(dt(2026,11,6,11),60,"A vie 11:00 corrección simulacro (paso 8)"),
    (dt(2026,11,6,16),90,"B vie 16:00 ampliar + intercalado"),
    (dt(2026,11,6,22,30),15,"C vie 22:30 antes de dormir"),
    (dt(2026,11,7,13),25,"D sáb 13:00"),
    (dt(2026,11,8,13),25,"E dom 13:00"),
    (dt(2026,11,9,12),30,"F lun 12:00 (tras PEP Macro)"),
    (dt(2026,11,10,13),60,"G mar 13:00 mini-simulacro"),
    (dt(2026,11,11,12,45),45,"H mié 12:45"),
    (dt(2026,11,11,22,30),20,"I mié 22:30 antes de dormir"),
    (dt(2026,11,12,6,45),40,"J jue 06:45 calentamiento")]
st={k:{"S":v[1],"last":v[3],"new":v[6]} for k,v in T.items()}
plan={}
for i,(tm,cap,lab) in enumerate(SL):
    nxt=SL[i+1][0] if i+1<len(SL) else EX
    cands=[]
    for k,v in T.items():
        s=st[k]
        if s["new"]:
            if i==1: cands.append((9,k,0.0))          # se aprenden en la sesión B
            continue
        if s["last"] is None: continue
        rn=R((tm-s["last"]).total_seconds()/86400,s["S"])
        rnext=R((nxt-s["last"]).total_seconds()/86400,s["S"])
        rex=R((EX-s["last"]).total_seconds()/86400,s["S"])
        if i==0 and k in("T1","T2","T5","T7","T10","T11","T14"): cands.append((8,k,rn)); continue  # la pauta revisa todo el simulacro
        need = rnext<0.90 or (i>=len(SL)-2 and rex<0.95)
        if need and rn<0.93: cands.append((v[5]*(1-rn)*10,k,rn))
    cands.sort(reverse=True); used=0; plan[lab]=[]
    for pr,k,rn in cands:
        m=T[k][4]*(2.5 if st[k]["new"] else 1)
        if used+m>cap: continue
        used+=m; s=st[k]
        if s["new"]: s["S"]=T[k][1]; s["new"]=0
        else: s["S"]=S_up(s["S"],T[k][2],rn,T[k][2]>=7)
        s["last"]=tm; plan[lab].append((k,round(rn,2),round(s["S"],1)))
    plan[lab].append(("min",used))
for lab,it in plan.items(): print(lab,"|",it)
print("\nR el jueves 08:15:")
for k,v in T.items():
    s=st[k]; print(k,v[0][:40],round(R((EX-s['last']).total_seconds()/86400,s['S']),2),"S=",round(s['S'],1))
