import io, subprocess
viejo = subprocess.run(["git","show","HEAD:datos/agenda/semanas/2026-11-02.md"],capture_output=True,cwd="C:/Proyecto Metodologia de estudio").stdout.decode("utf-8").split("\n")
g = lambda pre: next(l for l in viejo if l.startswith(pre))
cuerpo = lambda l: l[l.index("):")+2:]
mu5 = cuerpo(g("- [ ] Micro · **μ5**"))
mu6 = cuerpo(g("- [ ] Micro · **μ6**")).split(". Después")[0]
p = "C:/Proyecto Metodologia de estudio/datos/agenda/semanas/2026-11-09.md"
L = io.open(p, encoding="utf-8").read().split("\n")
f = lambda pre: next(i for i,l in enumerate(L) if l.startswith(pre))
# --- lunes
iF = f("- [ ] Econometría · **sesión F**"); F = cuerpo(L[iF])
iHc = f("- [ ] Historia (11:15")
L[iHc] = L[iHc].replace("**correo al profesor**", "**correo al profesor de Historia** y, en el mismo rato, **el de Micro** (hora, sala, duración de la PEP y si entran secuenciales; no hay clase el mar 10)", 1)
iD_txt = "A4 a-b (PDO) · 2 amenazas con la dirección del sesgo · WOE e IV de C4 · ATT y tendencias paralelas en voz alta · A1 b-d con la pauta tapada"
L[iF] = "- [ ] Econometría · **sesión D** (12:00-12:35, 35 min, después de la PEP; viene del sáb 7): " + iD_txt
L.insert(iF+1, "- [~] Econometría · **sesión F** → mié 11 (junto con H)")
iHt = f("- [ ] Historia (tarde, ~2 h)")
L[iHt] = L[iHt].replace("Historia (tarde, ~2 h)", "Historia (14:00-16:00, ~2 h)", 1)
i7 = f("- [ ] Micro · **μ7**"); mu7 = cuerpo(L[i7])
L[i7] = "- [ ] Micro · **μ5** (16:15-17:45, 89 min; viene del dom 8):" + mu5
i8 = f("- [ ] Micro · **μ8**"); mu8 = cuerpo(L[i8])
L[i8] = ("- [ ] Micro · **μ6 + μ7** (20:00-21:00, 60 min, juntas por el viernes perdido): matemático del **Control 2026-1** sin mirar (`2026-10-21-control-2026-1-matematico-resuelto.md`, 3.er grado; 25) · la **matriz de la PEP 1 2026-1** sin mirar (10) · **A4 ej. 5** (competencia monopolística, 1.ª vez; viene de μ2, 10) · **C3 del Control 1** (3.er grado y Pareto) y el **D1** en 5 líneas (viene de μ2, 10) · comente **C13** (1.er grado, 5). Se cae: paquete mixto y C10 con otras palabras")
L.insert(i8+1, "- [~] Micro · **μ8** → mié 11 (junto con μ11)")
# --- martes
iG = f("- [ ] Econometría · **sesión G**")
E = cuerpo(g("- [ ] Econometría · **sesión E**"))
L.insert(iG, "- [ ] Econometría · **sesión E** (12:00-12:38, 38 min; viene del dom 8):" + E)
iMq = f("- [ ] Micro II (**no hay clase**")
L[iMq] = L[iMq].replace("- [ ] Micro II (**no hay clase**: escribir hoy o a más tardar el lun 9 al profesor o al ayudante)", "- [ ] Micro II (**no hay clase**; el correo va el lun 9 a las 11:15 junto al de Historia; hoy solo si no salió)", 1)
# --- miércoles
iH = f("- [ ] Econometría · **sesión H**"); H = cuerpo(L[iH])
L[iH] = "- [ ] Econometría · **sesión F + H** (12:45-13:50, 65 min; F viene del lun 9): WOE/IV en frío · Card-Krueger en 3 líneas · A1 con la pauta tapada · A2 a-e (a-c tapada; Gini, KS) · EP de una dummy · DiD 2×2 desde medias (C6) · un PDO con otros números · A1 d) · MPL · lista de fallas"
iF2 = f("- [ ] Historia · **fichas 2** (13:45-14:30")
L[iF2] = L[iF2].replace("(13:45-14:30, **45 min**; antes 90)", "(14:15-15:00, **45 min**; antes 90 y 13:45)", 1)
i11 = f("- [ ] Micro · **μ11**")
L[i11] = ("- [ ] Micro · **μ8 + μ11** (18:30-20:05, 95 min con una pausa; μ8 viene del lun 9): **A4 ej. 3** sin mirar (3.er grado) · **A3 ej. 4** completo (3.er grado con arbitraje y la b de dos partes) · un árbol con amenaza no creíble (*si no entran secuenciales, otra matriz*) · una matriz nueva 3×3 · Hotelling y bienestar · dos partes con dos tipos en 5 líneas · paquetes · PIE y paradoja del 1.er grado en 3 líneas. **Micro queda cerrada aquí**")
io.open(p,"w",encoding="utf-8",newline="\n").write("\n".join(L))
