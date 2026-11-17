from itertools import combinations
# Brechas NO cubiertas por la versión final: (nombre, prob. de aparecer, pts típicos)
G={
'G1 logit con x^2 (EM y máximo)':(.35,5),'G2 x en log (EM=gβ/x)':(.25,4),'G3 APE vs PEA':(.30,2),
'G4 matriz desde lista de P̂':(.40,4),'G5 ROC/AUC como prob. de orden':(.30,4),'G6 KS desde tabla de deciles':(.35,4),
'G7 construir scorecard (puntos por atributo)':(.50,6),'G8 leer scorecard / no monótono':(.40,3),'G9 conceptos (validación, PSI, rechazados)':(.30,2),
'G10 placebo que FALLA':(.35,4),'G11 DiD no significativo / IC':(.30,2),'G12 sesgo de selección numérico':(.30,4),
'G13 output DiD con controles y FE':(.30,3),'G14 BP / VIF':(.15,4),'G15 logit con interacción':(.20,3),
'G16 RV anidado (q restricciones)':(.30,3),'G17 WOE con tramo sin malos':(.15,2),'G18 sobremuestreo / prior':(.10,3)}
w={k:p*q for k,(p,q) in G.items()}
k=list(G)
R={'R1 logit edad, edad² y ln(ing)':[0,1,2],'R2 diez clientes: matriz, ROC, AUC, KS':[3,4,5],'R3 tabla de deciles: KS':[5],
'R4 construir y usar scorecard':[6,7],'R5 leer scorecard + conceptos':[7,8],'R6 DiD placebo que falla + IC':[9,10],
'R7 resultados potenciales numérico':[11],'R8 output DiD con controles':[12,10],'R9 RV anidado + interacción':[15,14],
'R10 BP/VIF':[13],'R11 WOE sin malos + sobremuestreo':[16,17],'R12 experimento: sesgo + no signif.':[11,10]}
R={n:{k[i] for i in s} for n,s in R.items()}
tot=sum(w.values())
must={x for x in G if G[x][0]>=.35}   # brechas probables: cubrir sí o sí
print(f"Peso total de brechas: {tot:.2f} pts esperados")
best={}
for n in range(1,len(R)+1):
    for S in combinations(R,n):
        cov=set().union(*(R[s] for s in S)); v=sum(w[x] for x in cov)
        if n not in best or v>best[n][0]: best[n]=(v,S,cov)
for n,(v,S,cov) in best.items():
    print(f"{n:2d} ejercicios: {v:5.2f} pts ({v/tot:5.1%}) | obligatorias ok: {must<=cov} | {S}")
# Óptimo: mínimo n con todas las obligatorias y >=85% del peso
for n,(v,S,cov) in best.items():
    ok=[ (sum(w[x] for x in set().union(*(R[s] for s in T))),T) for T in combinations(R,n)
         if must<=set().union(*(R[s] for s in T)) and sum(w[x] for x in set().union(*(R[s] for s in T)))>=.85*tot]
    if ok: print("\nÓPTIMO:",n,max(ok)); break
