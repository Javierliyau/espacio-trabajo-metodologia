# peso, S_hoy, calidad_al_recordar (q), q_si_no_se_practica
T={'T1':(.85,3,.85,.85),'T2':(.75,2,.75,.65),'T3':(.30,2,.85,.80),'T4':(.35,0,.85,.35),
'T5':(.50,2.5,.90,.85),'T6':(.30,0,.80,.30),'T7':(.80,1.5,.80,.65),'T8':(.25,1,.80,.60),
'T9':(.25,3,.85,.85),'T10':(.80,3,.90,.90),'T11':(.50,1.5,.80,.70),'T12':(.35,2,.70,.55),
'T13':(.20,5,.75,.70),'T14':(.60,2,.75,.70)}
Rplan={'T1':.95,'T2':.93,'T3':.97,'T4':.98,'T5':.96,'T6':1.0,'T7':.95,'T8':1.0,'T9':.97,'T10':.95,'T11':.96,'T12':1.0,'T13':.95,'T14':.99}
R=lambda t,S:(1+19/81*t/S)**-0.5 if S>0 else 0.0
def nota(p): return 1+3*p/.6 if p<.6 else 4+3*(p-.6)/.4
W=sum(v[0] for v in T.values())
for nombre,fR,fq in [('sin repasar (6 dias)',lambda k,v:R(6,v[1]) if v[1] else 1,lambda v:v[3]),
                     ('solo repaso, sin ampliar',lambda k,v:Rplan[k],lambda v:v[3]),
                     ('plan completo',lambda k,v:Rplan[k],lambda v:v[2])]:
    p=sum(v[0]*fR(k,v)*fq(v) for k,v in T.items())/W
    for presion in (.95,.88):
        print(f"{nombre:26s} presion {presion}: {p*presion:.0%} -> nota {nota(p*presion):.1f}")
