# Micro hacia 5,2-5,4: franjas extra y topes mas altos; Econometria v3 fija
import sys,os,json; sys.argv=['x']; import joint as J
EXTRA=[('Mx','M','sab 10:30',1.02,60,'sab',0),('My','M','dom 10:30',2.02,60,'dom',0),
('Mz','M','vie 20:30',0.44,30,'vie',0),('Mw','M','mar 21:30',4.48,30,'mar',1),('Mv','M','lun 16:00',3.25,40,'lun',0)]
def setup(extra,cap,slotcap):
    J.SL[:]=[s for s in J.SL if s[0] not in [e[0] for e in EXTRA]]+[e for e in EXTRA if e[0] in extra]
    J.SL.sort(key=lambda s:s[3]); J.ORD[:]=[s[0] for s in J.SL]
    for d in J.DAYCAP: J.DAYCAP[d]=cap.get(d,J.DAYCAP[d])
    J.SL[:]=[(a,b,c,t,slotcap.get(a,k),d,z) for (a,b,c,t,k,d,z) in J.SL]
    for s in J.SL: J.CUR.setdefault(s[0],[])
import joint2 as J2
def run(tag,extra,cap,slotcap,BM):
    setup(extra,cap,slotcap); J2.MS[:]=[s for s in J.SL if s[1]=='M']
    best=None
    for sd in range(3):
        P=J2.optimizar_M(BM,30000,300+sd); m=J.montecarlo(P,600)
        if best is None or m[1][0]>best[0][1][0]: best=(m,P)
    P=best[1]; c=J.costo(P); mc=J.montecarlo(P,2000); dd={}
    for s in J.SL: dd[s[5]]=dd.get(s[5],0)+c[s[0]]
    tM=sum(c[s[0]] for s in J.SL if s[1]=='M')
    print(f'\n{tag} BM={BM}: Micro {tM} min  Micro {mc[1]}  Econ {mc[0][0]}  carga {dd}',flush=True)
    for s in J.SL:
        if s[1]=='M': print(f'  {s[0]:3s} {s[2]} {c[s[0]]:3d}: {", ".join(P[s[0]])}',flush=True)
    return P
if __name__=='__main__':
    sc=sys.argv_orig if False else None
    cfg=os.environ.get('CFG','a')
    hi={'vie':160,'sab':200,'dom':200,'lun':160,'mar':200,'mie':160,'jue':115}
    if cfg=='a': run('topes 160-200, sin franjas nuevas',[],hi,{'Mb':120,'Mc':120,'Mf':80,'Md':100},700)
    if cfg=='b': run('topes + franjas sab/dom manana',['Mx','My'],hi,{'Mb':120,'Mc':120,'Mf':80,'Md':100},700)
    if cfg=='c': run('todo',['Mx','My','Mz','Mw','Mv'],hi,{'Mb':120,'Mc':120,'Mf':80,'Md':100},800)
if os.environ.get('CFG')=='d':
    run('franjas sab/dom manana, topes 180',['Mx','My'],{'vie':160,'sab':180,'dom':180,'lun':160,'mar':170,'mie':160,'jue':115},{'Mb':100,'Mc':100,'Mf':80,'Md':100,'Mx':50,'My':50},640)
