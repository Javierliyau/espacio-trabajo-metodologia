base = "C:/Proyecto Metodologia de estudio/datos/"
# 1. nota en la prediccion
p = base + "material/macroeconomia-ii/2026-10-29-prediccion-control-2.md"
s = open(p, encoding="utf-8").read()
ancla = "**2. Alza de $s_R$** ($\lambda=1,\ \phi=0$"
assert ancla in s
if "Figura del libro (control de lectura)" not in s:
    i = s.index("\n", s.index(ancla))
    nota = "\n\n*Figura del libro (control de lectura): JV usa el eje $L_A/A$ y una recta fija de pendiente $\theta$; al subir $s_R$ se salta a X sobre la recta y se vuelve por ella. Ver [`2026-10-31-lectura-control-2-caso-moore.md`](2026-10-31-lectura-control-2-caso-moore.md).*"
    s = s[:i] + nota + s[i:]
    open(p, "w", encoding="utf-8", newline="").write(s)
# 2. indice
p = base + "material/macroeconomia-ii/INDICE.md"
s = open(p, encoding="utf-8").read()
ancla = "| `2026-10-29-traduccion-jones-vollrath-cap5-control.pdf` |"
assert ancla in s
fila = "| `2026-10-31-lectura-control-2-caso-moore.pdf` + [`.md`](2026-10-31-lectura-control-2-caso-moore.md) | 31-10-2026 | **6. Ideas y Crecimiento Económico** (Control 2, lun 2-11: JV 5.1, 5.2.1, 5.2.2) | Caso real (chips y Ley de Moore): lectura pasiva completa con cifras verificadas, y preguntas de desarrollo respondidas en orden de probabilidad (simulación propia, modelo de juicio) | sí |\n"
if "caso-moore.pdf" not in s:
    i = s.index("\n", s.index(ancla)) + 1
    s = s[:i] + fila + s[i:]
    open(p, "w", encoding="utf-8", newline="").write(s)
# 3. buzon del informe
p = base + "informe-pe/aportes-desde-ramos.md"
s = open(p, encoding="utf-8").read()
if "Chile 0,39" not in s:
    filas = [
     "| 7 | En Romer-Jones ($\phi<1$), un subsidio a la I+D sube el **nivel** del PIB tendencial, no su tasa de largo plazo: la tasa sube solo en la transición. Con $\lambda=1,\ \phi=0,\ n=1\%$ (cifras ilustrativas), duplicar la fracción en I+D lleva unos 69 años para lograr la mitad de la ganancia en $A$: «no sube la tasa» no significa «no importa». | políticas · PTF | V en JV 2013, pp. 107-109 (el teorema); el cálculo de 69 años es derivación propia | nuevo |",
     "| 8 | Cuidado al aplicar Romer a Chile: JV describe a los países avanzados **en conjunto** (la frontera), y la transferencia tecnológica es el capítulo siguiente. Para Chile, la PTF depende más de adoptar que de inventar. | método · políticas | V en JV, p. 99 (el alcance); la lectura para Chile es propia | nuevo |",
     "| 9 | Gasto en I+D, % del PIB (Banco Mundial, GB.XPD.RSDV.GD.ZS): Chile 0,39 % (2022), EE. UU. 3,45 % (2023), Corea 4,94 % (2023). | políticas | V (API del Banco Mundial, consulta 31-10-2026) | nuevo |",
     "| 10 | Las ideas cuestan cada vez más: en EE. UU. el esfuerzo de investigación se multiplicó por 23 desde los años 30 mientras la productividad investigadora cayó cerca de 5 % anual; implica $\phi \approx -2{,}1$ agregado y $\approx 0{,}8$ en chips. | PTF | V (Bloom et al. 2020, AER 110(4), pp. 1110 y tabla 7; el artículo da 5,1 % y 5,3 % en distintos lugares) | nuevo |",
    ]
    s = s.rstrip("\n") + "\n" + "\n".join(filas) + "\n"
    open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
