from math import exp,log
L=lambda z:1/(1+exp(-z))
print("R1"); z=3.0-0.12*40+0.0012*1600-0.8*log(10); P=L(z); g=P*(1-P)
print(f" z={z:.4f} P={P:.4f} g={g:.4f} EMedad={(-0.12+2*0.0012*40)*g:.5f} min={0.12/0.0024:.0f}")
print(f" EMing/100mil={-0.8*g/10:.5f} EM 1%={-0.8*g*0.01:.5f}")
z60=3.0-0.12*60+0.0012*3600-0.8*log(10); P60=L(z60); print(f" edad60 z={z60:.4f} P={P60:.4f} EMedad={(-0.12+2*0.0012*60)*P60*(1-P60):.5f}")
print("R2"); d=[(.92,1),(.81,1),(.74,0),(.66,1),(.55,0),(.47,1),(.38,0),(.29,0),(.18,0),(.07,0)]
M=[p for p,y in d if y];B=[p for p,y in d if not y]
print(" AUC",sum(m>b for m in M for b in B)/(len(M)*len(B)))
tp=fp=0;ks=0
for p,y in d:
    tp+=y;fp+=1-y;print(f"  corte {p}: TPR={tp/4:.3f} FPR={fp/6:.3f} dif={tp/4-fp/6:.3f}")
print("R4"); F=30/log(2);O=620-F*log(40);b0=-1.8;bc=-0.95;ba=-0.8
wc={'0':log(.4/.25),'1':log(.25/.2),'2-5':log(.275/.3),'6+':log(.075/.25),'4-5 sin fusionar':log(1.5)}
wa={'<1':-0.60,'1-5':0.05,'>5':0.55}
base=O/2-b0/2*F; print(f" F={F:.2f} O={O:.2f} base={base:.2f}")
for k,v in wc.items(): print(f"  cons {k}: WOE={v:.3f} pts={base-bc*v*F:.1f}")
for k,v in wa.items(): print(f"  antig {k}: pts={base-ba*v*F:.1f}")
for nm,c,a in [('A',wc['1'],wa['1-5']),('B',wc['0'],wa['>5']),('C',wc['6+'],wa['<1'])]:
    z=b0+bc*c+ba*a; print(f"  {nm}: z={z:.4f} P={L(z):.4f} score={O-F*z:.1f}")
print("R6"); print(" DiD",(47.5-43)-(62.5-61)," placebo",(43-40)-(61-60)," t",3/1.6," IC",3-1.96*1.6,3+1.96*1.6)
print("R9 RV",2*(-605.1+612.4))
for nm,z in [('H solt',-.5),('M solt',-.2),('H cas',.1),('M cas',-.5)]: print(f"  {nm} P={L(z):.4f}")
print("  ef casarse H",L(.1)-L(-.5)," M",L(-.5)-L(-.2)," dif",(L(-.5)-L(-.2))-(L(.1)-L(-.5)))
print("R12"); Y=[(12,10,1),(11,9,1),(10,9,1),(8,7,0),(7,6,0),(6,6,0)]
ate=sum(a-b for a,b,_ in Y)/6; att=sum(a-b for a,b,d in Y if d)/3
obs=sum(a for a,b,d in Y if d)/3-sum(b for a,b,d in Y if not d)/3
sel=sum(b for a,b,d in Y if d)/3-sum(b for a,b,d in Y if not d)/3
print(f" ATE={ate:.4f} ATT={att:.4f} obs={obs:.4f} sesgo={sel:.4f} check={att+sel:.4f}")
