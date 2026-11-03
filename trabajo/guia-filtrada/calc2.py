from math import log
T=[("<1",300,150),("1-3",900,250),("3-5",700,120),("5-10",1100,150),("10+",1000,180)]
B=sum(t[1] for t in T); M=sum(t[2] for t in T); print("B",B,"M",M,"tasa",round(M/(B+M),4))
iv=0
for n,b,m in T:
    pb,pm=b/B,m/M; w=log(pb/pm); iv+=(pb-pm)*w
    print(n, round(pb,4), round(pm,4), "WOE*100", round(100*w,1), "iv", round((pb-pm)*w,4), "tasa", round(m/(b+m),3))
print("IV",round(iv,4))
F=T[:3]+[("5+",2100,330)]; iv2=0
for n,b,m in F:
    pb,pm=b/B,m/M; w=log(pb/pm); iv2+=(pb-pm)*w
    print(n, round(100*w,1), round((pb-pm)*w,4), "tasa", round(m/(b+m),3))
print("IV fus", round(iv2,4))
