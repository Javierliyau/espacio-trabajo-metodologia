import sys, pathlib
P = pathlib.Path("C:/Proyecto Metodologia de estudio/datos")
def rep(path, old, new):
    t = path.read_text(encoding="utf-8")
    assert t.count(old) == 1, (path.name, old[:60], t.count(old))
    path.write_text(t.replace(old, new), encoding="utf-8")
cal = P/"agenda/calendario.md"
rep(cal, "| 2026-11-09 | 09:50 | Macroeconomía II | **PEP 1** (35 %). Hora = inicio de la clase, sin confirmar | pendiente | correo Droller 7-10 |",
 "| 2026-11-09 | 09:50 | Macroeconomía II | **PEP 1** (35 %). Hora = inicio de la clase, sin confirmar. **Entra todo hasta antes del modelo schumpeteriano (U1–U6, Romer completo JV 5.1–5.5); Schumpeter no entra.** Formato anunciado: **verdaderos y falsos + matemáticos con demostraciones algebraicas**. Cimientos de la predicción: `material/macroeconomia-ii/2026-11-04-cimientos-prediccion-pep-1.md` | pendiente | correo Droller 7-10; temario y formato dichos en clase (dato del estudiante 4-11) |")
t = cal.read_text(encoding="utf-8")
anchor = "| 2026-11-06 | 13:45 | Econometría II |"
assert t.count(anchor) == 1
cal.write_text(t.replace(anchor, "| 2026-11-06 | 09:50 | Macroeconomía II | **Ayudantía de repaso para la PEP 1** («una buena ayudantía», según Droller). Después se cierra la predicción final | pendiente | dato del estudiante 4-11 |\n" + anchor), encoding="utf-8")

w = P/"agenda/semanas/2026-11-02.md"
t = w.read_text(encoding="utf-8")
i = t.index("- [ ] Macro II (09:50, ayudantía)")
j = t.index("- [ ] Econometría (13:45, asumida)")
t = t[:i] + """- [ ] Macro II (09:50, ayudantía de repaso): ir y anotar qué ejercicios hacen y qué destaca el ayudante (¿toca $s_R$ de equilibrio, regla de oro, MRW?)
- [ ] Macro II (tarde, después de la PEP de Econometría, 20 min): **cerrar aquí la predicción final** con lo de la ayudantía (`material/macroeconomia-ii/2026-11-04-cimientos-prediccion-pep-1.md` §5): pre-registro con `motor manual` y simulacro (V/F + demostraciones)
""" + t[j:]
i = t.index("- [ ] Macro II (mañana, ~2,5 h): **Solow**")
j = t.index("- [ ] Historia (metro o noche, si queda energía)")
t = t[:i] + """- [ ] Macro II (~2 h): **demostraciones sin mirar**, solo las de la predicción final. Solow S1-S5 y extensiones E1-E2 (1 h) · Romer R1-R4 (1 h). Corregir con las pautas oficiales (Ay. 1, 2 y 4) y el análisis del Control 2
""" + t[j:]
i = t.index("- [ ] Macro II (mañana, ~2 h): **simulacro de PEP 1**")
j = t.index("- [ ] Macro II (lun 9-11, antes de clase, 20 min)")
t = t[:i] + """- [ ] Macro II (~2 h): **simulacro de PEP 1** cronometrado (80 min), sin mirar, y corrección (40 min) solo de lo que falló; los 14 V/F de los cimientos en voz alta
- [ ] Macro II (15 min): **hoja de memoria** de una página: $k^*$, $y^*(t)$, regla de oro, contabilidad, MRW, $g_A=\lambda n/(1-\phi)$, CPO de Romer, $p=r/\alpha$, $\pi$, $P_A$, $s_R$
""" + t[j:]
w.write_text(t, encoding="utf-8")

idx = P/"material/macroeconomia-ii/INDICE.md"
t = idx.read_text(encoding="utf-8")
anchor = "| `2026-11-04-control-2-analisis.md` |"
k = t.index(anchor); e = t.index("\n", k)
t = t[:e+1] + "| [`2026-11-04-cimientos-prediccion-pep-1.md`](2026-11-04-cimientos-prediccion-pep-1.md) | 04-11-2026 | **U1–U6** (PEP 1, lun 9-11; Schumpeter no entra) | Cimientos de la predicción: temario y formato anunciados (V/F + demostraciones algebraicas), reparto por bloque, 11 demostraciones candidatas con p, 14 V/F con clave, qué falta para cerrarla el vie 6-11 | — |\n" + t[e+1:]
idx.write_text(t, encoding="utf-8")
print("ok")
