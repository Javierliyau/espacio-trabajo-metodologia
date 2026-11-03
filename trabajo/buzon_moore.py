p = "C:/Proyecto Metodologia de estudio/datos/informe-pe/aportes-desde-ramos.md"
s = open(p, encoding="utf-8", newline="").read()
if "2026-10-31 · Macro II" not in s:
    s = s.rstrip("\n") + r"""

## 2026-10-31 · Macro II, lectura JV 5.1 para el Control 2 (caso Moore)

| # | Aporte | Sección | Rigor | Estado |
|---|---|---|---|---|
| 1 | Las ideas cuestan cada vez más: en EE. UU. el esfuerzo de investigación se multiplicó por 23 desde los años 30, mientras su productividad cayó cerca de 5 % anual. En $\dot A = \bar\theta L_A A^\phi$ eso implica $\phi \approx -2{,}1$ agregado y $\approx 0{,}8$ en chips. | PTF | V (Bloom et al. 2020, AER 110(4), p. 1110 y tabla 7; el artículo da 5,1 % y 5,3 % en distintos lugares) | nuevo |
| 2 | Matiz a los aportes del 19-10 sobre $s_R$: el efecto de nivel puede tardar mucho. Con $\lambda = 1$, $\phi = 0$, $n = 1\%$, al duplicar $s_R$ se tardan unos 69 años en lograr la mitad de la ganancia en $A$. «No sube la tasa de largo plazo» no significa «no importa». | políticas | — (derivación propia, cifras ilustrativas) | nuevo |
| 3 | Límite al aplicar Romer a Chile: JV lo plantea para los países avanzados en conjunto y deja la transferencia tecnológica para el capítulo siguiente. Para Chile puede pesar más adoptar que inventar. | método · políticas | V en JV, p. 99 (el alcance); C la lectura para Chile | nuevo |
"""
    open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
