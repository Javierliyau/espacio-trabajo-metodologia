# -*- coding: utf-8 -*-
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
a, s, n, g, d = 1/3, 0.23, 0.01, 0.02, 0.05
ng = n + g + d
ks = (s/ng)**(1/(1-a)); destr = 0.07
t0, dt = 2010.16, 0.01
ts, lny, lny_cf, gy = [], [], [], []
k = ks; t = 2000.0; lnA0 = 0.0
while t <= 2040:
    if abs(t - t0) < dt/2: k = k*(1-destr)
    lnA = lnA0 + g*(t-2000)
    ts.append(t); lny.append(lnA + a*math.log(k)); lny_cf.append(lnA + a*math.log(ks))
    gk = s*k**(a-1) - ng
    gy.append(100*(g + a*gk))
    k += k*gk*dt; t += dt
k1 = ks*(1-destr)
fig = plt.figure(figsize=(12, 8.5))
A1 = fig.add_subplot(2, 2, 1); A2 = fig.add_subplot(2, 2, 2); A3 = fig.add_subplot(2, 1, 2)
# Diagrama de Solow
xs = [i*ks*1.5/400 for i in range(1, 401)]
A1.plot(xs, [s*x**a for x in xs], color="#1f4e79", lw=2, label=r"$s\,\tilde k^{\alpha}$")
A1.plot(xs, [ng*x for x in xs], color="#c0392b", lw=2, label=r"$(n+g+\delta)\,\tilde k$")
for x, lab in ((ks, r"$\tilde k^{*}$"), (k1, r"$\tilde k_{t_0}$")):
    A1.axvline(x, color="black", ls="--", lw=0.8); A1.text(x, -0.005, lab, ha="center", va="top", fontsize=11)
A1.annotate("", xy=(ks*0.985, s*k1**a*0.93), xytext=(k1*1.005, s*k1**a*0.93), arrowprops=dict(arrowstyle="->", lw=1.5))
A1.annotate("", xy=(k1, s*k1**a+0.05), xytext=(ks, s*k1**a+0.05), arrowprops=dict(arrowstyle="->", lw=1.5, color="#c0392b"))
A1.text((k1+ks)/2, s*k1**a+0.07, "27-F: salto", ha="center", fontsize=9, color="#c0392b")
A1.set_xlim(0, ks*1.5); A1.set_ylim(0, s*max(xs)**a*1.25)
A1.set_xlabel(r"$\tilde k = K/(AL)$"); A1.set_ylabel("por trabajador efectivo")
A1.set_title(r"Diagrama de Solow en $\tilde k$: el terremoto mueve el punto, no las curvas", fontsize=11); A1.legend(fontsize=9, loc="upper left"); A1.set_xticks([]); A1.set_yticks([])
# Zoom
z = [x for x in xs if 0.85*ks < x < 1.1*ks]
A2.plot(z, [s*x**a for x in z], color="#1f4e79", lw=2); A2.plot(z, [ng*x for x in z], color="#c0392b", lw=2)
A2.axvline(ks, color="black", ls="--", lw=0.8); A2.axvline(k1, color="black", ls="--", lw=0.8)
A2.fill_between([k1, k1], [ng*k1], [s*k1**a], color="green")
A2.plot([k1, k1], [ng*k1, s*k1**a], color="green", lw=4, label=r"$\dot{\tilde k}>0$")
A2.text(k1, ng*k1*0.995, r"$\tilde k_{t_0}$", ha="center", va="top"); A2.text(ks, ng*k1*0.995, r"$\tilde k^{*}$", ha="center", va="top")
A2.set_title(r"Zoom: en $t_0$ la inversión supera la reposición", fontsize=11); A2.legend(fontsize=9); A2.set_xticks([]); A2.set_yticks([])
# ln y contra t
A3.plot(ts, lny_cf, color="gray", ls="--", lw=1.5, label="sin terremoto (senda balanceada, pendiente $g$)")
A3.plot(ts, lny, color="#1f4e79", lw=2.2, label="con terremoto")
A3.axvline(t0, color="#c0392b", ls=":", lw=1); A3.text(t0+0.3, min(lny)+0.02, "27-F ($t_0$)", color="#c0392b")
A3.set_xlabel("año (modelo)"); A3.set_ylabel(r"$\ln y$"); A3.set_xlim(2004, 2040)
A3.set_title(r"$\ln y$ contra el tiempo", fontsize=11); A3.legend(fontsize=9, loc="upper left"); A3.grid(alpha=0.3)
ins = A3.inset_axes([0.62, 0.08, 0.35, 0.38])
ins.plot(ts, gy, color="#1f4e79"); ins.axhline(100*g, color="gray", ls="--"); ins.set_xlim(2005, 2040)
ins.set_title(r"$\dot y/y$ (%)", fontsize=9); ins.tick_params(labelsize=8)
fig.suptitle("Solow calibrado a Chile: el 27-F destruye ~7 % de $K$\n"
             r"$\alpha=1/3,\ s=0{,}23,\ n=1\%,\ g=2\%,\ \delta=5\%$ (calibración ilustrativa)", fontsize=12)
fig.tight_layout(rect=(0, 0, 1, 0.94)); fig.savefig("2026-10-25-solow-chile-terremoto.png", dpi=150)
i0 = min(range(len(ts)), key=lambda i: abs(ts[i]-t0-0.02))
print("caida ln y impacto %", round(100*(lny[i0]-lny_cf[i0]), 2), "gy impacto", round(gy[i0], 3))
for yr in (2015, 2023, 2040):
    i = min(range(len(ts)), key=lambda j: abs(ts[j]-yr)); print(yr, "brecha %", round(100*(lny[i]-lny_cf[i]), 2))
