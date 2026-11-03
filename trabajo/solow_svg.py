import math
X=lambda k:60+115*k
Yf=lambda k:420-120*math.sqrt(k)
Yi=lambda k:420-60*math.sqrt(k)
Yd=lambda k:420-24*k
Yn=lambda k:420-36*k
def path(f,a,b,n=22):
    pts=[(X(a+(b-a)*j/n),f(a+(b-a)*j/n)) for j in range(n+1)]
    return "M"+" L".join(f"{x:.0f},{y:.0f}" for x,y in pts)
K=[4,4.1,4.1962,4.2887]
ks,ksn=6.25,25/9
o=[]
A=o.append
A('<svg viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg" role="img"><title>Modelo de Solow: dinamica de k y aumento de n</title><desc>Curvas f(k), s f(k), (n+d)k con n=0,02 y n=0,07; k de los anos 0 a 3 y estados estacionarios 6,25 y 2,78</desc>')
A('<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>')
ax='stroke="var(--text-primary)" stroke-width="1.5" fill="none"'
A(f'<path d="M60,420 L870,420" {ax} marker-end="url(#ar)"/><path d="M60,420 L60,40" {ax} marker-end="url(#ar)"/>')
A('<text class="ts" x="872" y="440" text-anchor="end">k (capital por trabajador)</text><text class="ts" x="70" y="42">y, i, (n+δ)k</text>')
A(f'<path d="{path(Yf,0,6.9)}" stroke="var(--text-secondary)" stroke-width="2" fill="none"/>')
A(f'<path d="{path(Yi,0,6.9)}" stroke="var(--text-accent)" stroke-width="2.5" fill="none"/>')
A(f'<path d="M60,420 L{X(6.9):.1f},{Yd(6.9):.1f}" stroke="var(--text-success)" stroke-width="2.5" fill="none"/>')
A(f'<path d="M60,420 L{X(6.6):.1f},{Yn(6.6):.1f}" stroke="var(--text-danger)" stroke-width="2.5" stroke-dasharray="8 5" fill="none"/>')
L=[("var(--text-secondary)","","y = f(k) = k^0,5"),("var(--text-accent)","","i = s·f(k) = 0,25·k^0,5"),("var(--text-success)","","(n+δ)k = (0,02+0,08)k = 0,10k"),("var(--text-danger)",' stroke-dasharray="8 5"',"(n'+δ)k = (0,07+0,08)k = 0,15k")]
for j,(c,d,t) in enumerate(L):
    yy=70+22*j
    A(f'<path d="M90,{yy} L125,{yy}" stroke="{c}" stroke-width="2.5"{d}/><text class="ts" x="133" y="{yy+4}">{t}</text>')
g='stroke="var(--text-muted)" stroke-width="1" stroke-dasharray="3 3"'
for j,k in enumerate(K):
    A(f'<path d="M{X(k):.1f},420 L{X(k):.1f},{Yf(k):.1f}" {g}/>')
    A(f'<circle cx="{X(k):.1f}" cy="{Yi(k):.1f}" r="3" style="fill:var(--text-accent)"/><circle cx="{X(k):.1f}" cy="{Yd(k):.1f}" r="3" style="fill:var(--text-success)"/><circle cx="{X(k):.1f}" cy="{Yf(k):.1f}" r="3" style="fill:var(--text-secondary)"/>')
    yy=438 if j%2==0 else 456
    A(f'<text class="ts" x="{X(k):.1f}" y="{yy}" text-anchor="middle">k{"₀₁₂₃"[j]}</text>')
A(f'<text class="ts" x="468" y="366" text-anchor="end">k̇₀ = 0,1</text><path d="M470,360 L514,316" stroke="var(--text-muted)" stroke-width="1"/>')
A(f'<path d="M{X(4)-4:.1f},{Yi(4)+2:.1f} L{X(4)-4:.1f},{Yd(4)-2:.1f}" stroke="var(--text-primary)" stroke-width="1"/>')
A(f'<text class="ts" x="{X(K[1]):.0f}" y="478" text-anchor="middle">4 · 4,10 · 4,20 · 4,29</text>')
A(f'<path d="M{X(4.35):.1f},405 L{X(6.1):.1f},405" stroke="var(--text-success)" stroke-width="2" marker-end="url(#ar)"/>')
A(f'<path d="M{X(3.95):.1f},405 L{X(2.95):.1f},405" stroke="var(--text-danger)" stroke-width="2" marker-end="url(#ar)"/>')
for kk,col,lab,yl in [(ks,'success',"E: k* = 6,25",Yi(ks)+26),(ksn,'danger',"E': k*' = 2,78",Yi(ksn)-22)]:
    A(f'<path d="M{X(kk):.1f},420 L{X(kk):.1f},{Yf(kk):.1f}" stroke="var(--text-{col})" stroke-width="1" stroke-dasharray="4 3"/>')
    A(f'<path d="M60,{Yi(kk):.1f} L{X(kk):.1f},{Yi(kk):.1f}" stroke="var(--text-{col})" stroke-width="1" stroke-dasharray="4 3"/>')
    A(f'<circle cx="{X(kk):.1f}" cy="{Yi(kk):.1f}" r="5" style="fill:var(--text-{col})"/>')
    A(f'<text class="ts" x="{X(kk)+(10 if kk>5 else 0):.1f}" y="{yl:.0f}" text-anchor="{'start' if kk>5 else 'middle'}" style="fill:var(--text-{col})">{lab}</text>')
    A(f'<text class="ts" x="{X(kk):.1f}" y="{438 if kk>5 else 438}" text-anchor="middle" style="fill:var(--text-{col})">{"k*" if kk>5 else "k*\'"}</text>')
A(f'<text class="ts" x="54" y="{Yi(ks)+4:.0f}" text-anchor="end">0,625</text><text class="ts" x="54" y="{Yi(ksn)+4:.0f}" text-anchor="end">0,417</text>')
A('</svg>')
open(r"C:/Espacio de trabajo Metodologia de estudio/trabajo/solow-n007.svg","w",encoding="utf-8").write("".join(o))
print(len("".join(o)))
