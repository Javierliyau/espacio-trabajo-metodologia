# Micro al maximo, respetando Macro (sab 2 h, dom 2 h 15 en la manana) y ~5 h/dia de estudio total
import sys,os,json; sys.argv=['x']; import joint as J, joint2 as J2
NEW=[('Ma','M','vie 17:00',0.292,25,'vie',0),('Mz','M','vie 20:30',0.4375,35,'vie',0),
('Mb','M','sab 15:30',1.229,120,'sab',0),('Mx','M','sab 18:30',1.354,50,'sab',0),
('Mc','M','dom 16:00',2.25,100,'dom',0),('My','M','dom 18:30',2.354,50,'dom',0),
('Mv','M','lun 16:00',3.25,40,'lun',0),('Md','M','lun 20:00',3.417,90,'lun',0),
('Me','M','mar 15:00',4.208,112,'mar',0),('Mw','M','mar 21:30',4.479,30,'mar',1),
('Mf','M','mie 18:30',5.354,80,'mie',0),('Mi','M','jue 13:10',6.132,25,'jue',0)]
J.SL[:]=[s for s in J.SL if s[1]=='E']+NEW; J.SL.sort(key=lambda s:s[3]); J.ORD[:]=[s[0] for s in J.SL]
# tope Econ+Micro = ~300 min - Macro - Historia de ese dia
J.DAYCAP.update({'vie':175,'sab':180,'dom':165,'lun':165,'mar':195,'mie':160,'jue':115})
for s in J.SL: J.CUR.setdefault(s[0],[])
J2.MS[:]=[s for s in J.SL if s[1]=='M']
BM=int(sys.argv_[0]) if False else int(os.environ.get('BM','900'))
best=None
for sd in range(3):
    P=J2.optimizar_M(BM,35000,400+sd); m=J.montecarlo(P,600)
    print('reinicio',sd,m[1][0],flush=True)
    if best is None or m[1][0]>best[0][1][0]: best=(m,P)
P=best[1]; c=J.costo(P); mc=J.montecarlo(P,2000); dd={}
for s in J.SL: dd[s[5]]=dd.get(s[5],0)+c[s[0]]
print(f'BM={BM}: Micro {sum(c[s[0]] for s in J2.MS)} min  Micro {mc[1]}  Econ {mc[0]}  carga {dd}',flush=True)
for s in J2.MS: print(f'  {s[0]:3s} {s[2]} {c[s[0]]:3d}: {", ".join(P[s[0]])}')
json.dump(P,open(f'joint4_{BM}.json','w'))
