from math import exp, log, sqrt
L=lambda z:1/(1+exp(-z))
print("== 1A Spector")
for psi in (0,1):
    z=-13.0213+2.8261*3.117+0.0952*21.938+2.3787*psi; p=L(z)
    print(psi, round(z,4), round(p,4), "EM GPA", round(p*(1-p)*2.8261,4), "x0.1", round(p*(1-p)*2.8261*0.1,4))
    zb=z+0.2826; print("  exact +0.1 GPA", round(L(zb)-p,4))
print("odds", round(exp(2.3787),3))
print("== 1B atletas")
for s in (5,10):
    z=-1.17+0.24*3+0.00058*1200+0.073*s; p=L(z); print(s, round(z,3), round(p,4), "EM", round(p*(1-p)*0.073,4))
print("odds study +1", round(100*(exp(0.073)-1),2))
print("== 2A clasif")
P=[0.92,0.81,0.66,0.58,0.47,0.41,0.36,0.33,0.27,0.22,0.15,0.08]
Y=[1,1,0,1,1,0,1,0,0,0,0,0]
for c in (0.5,0.3):
    vp=sum(p>c and y==1 for p,y in zip(P,Y)); fn=sum(p<=c and y==1 for p,y in zip(P,Y))
    fp=sum(p>c and y==0 for p,y in zip(P,Y)); vn=sum(p<=c and y==0 for p,y in zip(P,Y))
    print(c, "VP",vp,"FN",fn,"FP",fp,"VN",vn,"exact",round((vp+vn)/12,3),"sens",round(vp/(vp+fn),3),"esp",round(vn/(vn+fp),3),"prec",round(vp/(vp+fp),3))
print("== 3A WOE antiguedad")
T=[("<1",300,150),("1-3",900,250),("3-5",700,120),("5-10",1100,150),("10+",1000,130)]
B=sum(t[1] for t in T); M=sum(t[2] for t in T); print("B",B,"M",M,"tasa malos",round(M/(B+M),4))
iv=0
for n,b,m in T:
    pb,pm=b/B,m/M; w=log(pb/pm); iv+=(pb-pm)*w
    print(n, round(pb,4), round(pm,4), "WOE*100", round(100*w,1), "iv", round((pb-pm)*w,4), "tasa malos", round(m/(b+m),3))
print("IV",round(iv,4))
b,m=1100+1000,150+130; pb,pm=b/B,m/M; w=log(pb/pm); print("fusion 5+",round(100*w,1),round((pb-pm)*w,4),"tasa",round(m/(b+m),3))
iv2=sum((b/B-m/M)*log((b/B)/(m/M)) for n,b,m in T[:3])+(pb-pm)*w; print("IV fusionado",round(iv2,4))
print("== 3B scorecard")
base=450
for pts in (base+52+43+20, base+62+65+35):
    print(pts)
d=(450+62+65+35)-(450+52+43+20); print("diff",d,"odds ratio PDO20",round(2**(d/20),3))
print("== 4A SLEP")
did=(270-262)-(261-255); print("DiD",did,"t",round(did/3.1,3))
