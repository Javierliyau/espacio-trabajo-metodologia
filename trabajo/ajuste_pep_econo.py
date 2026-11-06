import re, pathlib
P = pathlib.Path("C:/Proyecto Metodologia de estudio/datos")
# 1) calendario
f = P/"agenda/calendario.md"; L = f.read_text(encoding="utf-8").split("\n")
i = next(k for k,l in enumerate(L) if l.startswith("| 2026-11-06 | 13:45 | Econometría II"))
old = L.pop(i)
new = ("| 2026-11-12 | 08:15 | Econometría II | **PEP 1** (35 %), **escrita**, **un solo bloque (~80 min)**. "
       "**Cambia por el paro del vie 6-11** (correo de Jorge Riquelme, 6-11 02:35); antes vie 6-11 13:45 y antes jue 5-11 08:15 en EF307. "
       "**Hora asumida 08:15 (bloque J1-J2 del jueves) y sala sin confirmar.** **Mismo día que la PEP 1 de Micro II.** "
       "**Entra hasta diferencias en diferencias; panel no.** **Traer calculadora**: preguntas «de este estilo [scoring], con los datos ahí», "
       "quizá calcular un WOE (clase 5, 22-10) y un DiD desde las medias (clase 6). Celulares adelante | pendiente | "
       "correo Riquelme 6-11 · dato del estudiante 3-11 · correo Pfeng 2-11 · clase 6 (29-10) [B2 00:26:44] |")
j = next(k for k,l in enumerate(L) if l.startswith("| 2026-11-12 |"))
L.insert(j, new); f.write_text("\n".join(L), encoding="utf-8")
# 2) protocolo
f = P/"programas/econometria-ii-protocolo-chat.md"; s = f.read_text(encoding="utf-8")
k = s.index("| **PEP 1: jue 5-11 o vie 6-11"); e = s.index("\n", k)
s = s[:k] + ("| **PEP 1: jue 12-11, escrita, un bloque (~80 min); hora asumida 08:15 (J1-J2), sala sin confirmar.** Pasó del jue 5-11 al vie 6-11 (dato del estudiante 3-11) "
     "y del vie 6-11 al jue 12-11 por el paro (correo de Jorge Riquelme, 6-11). Mismo día que la PEP 1 de Micro II. **Entra hasta DiD; panel no.** | V (correo 6-11) |") + s[e:]
f.write_text(s, encoding="utf-8")
# 3) semana actual
f = P/"agenda/semanas/2026-11-02.md"; s = f.read_text(encoding="utf-8")
rep = [
 ("**Fecha:** Econometría II: **PEP 1** (35 %), un bloque, hora asumida 13:45 (V4), sala sin confirmar",
  "**Paro confirmado:** la PEP 1 de Econometría pasa al **jue 12-11** (correo de Jorge Riquelme, 02:35). Confirmar si hay ayudantía de Macro y clase de Historia"),
 ("- [ ] Econometría · paso 11 (mañana, 30 min): en frío, un ejercicio de cada tipo + «Las 15 frases» (5 min)",
  "- [~] Econometría · paso 11 → jue 12-11, antes de la PEP\n- [ ] Econometría · paso 8 (hoy, 1 h, con el simulacro fresco): corregir el simulacro de anoche con `material/econometria-ii/2026-11-04-simulacro-final-pep1-pauta-libro.pdf` y anotar en una lista solo las fallas (son la base de los pasos 9 y 10)"),
 ("- [ ] Macro II (tarde, después de la PEP de Econometría, 20 min)", "- [ ] Macro II (tarde, 20 min)"),
 ("- [ ] Econometría (13:45, asumida): **PEP 1**", "- [~] Econometría: **PEP 1** → jue 12-11 08:15 (asumida)"),
 ("- [ ] Econometría · paso 8 (1 h): corregir y volver solo a las fallas, incluidas las de teoría",
  "- [~] Econometría · paso 8 → vie 6-11"),
 ("- [ ] Econometría · paso 9 (1 h; clase J1-J2 si no hay, o 12:45-13:45)", "- [~] Econometría · paso 9 → mar 10-11 (1 h; antes: clase J1-J2 si no hay, o 12:45-13:45)"),
 ("- [ ] Econometría · paso 10 (noche, 30 min)", "- [~] Econometría · paso 10 → mié 11-11 (noche, 30 min)"),
]
for a,b in rep:
    assert a in s, a; s = s.replace(a,b,1)
s = s.replace("- [ ] Macro II (15 min): **hoja de memoria** de una página",
  "- [ ] Econometría (15 min, no-cero): el núcleo de teoría (12 ítems, 8 min) en voz alta + releer la lista de fallas del paso 8; nada nuevo\n- [ ] Macro II (15 min): **hoja de memoria** de una página",1)
f.write_text(s, encoding="utf-8")
# 4) semana siguiente
f = P/"agenda/semanas/2026-11-09.md"; s = f.read_text(encoding="utf-8")
rep = [
 ("- [ ] Micro II (tarde, ~3 h): **discriminación en cálculo**",
  "- [ ] Econometría · paso 9 (13:00-14:00, antes de Micro): **ayudantía 5, P2-P4** cronometradas (~30 min, `material/econometria-ii/2026-11-05-ayudantia-5-ejercicios-pauta.pdf`) y corregir solo las fallas; reemplaza el simulacro corto (es el material con más probabilidad de calcado)\n- [ ] Micro II (tarde, ~3 h): **discriminación en cálculo**"),
 ("- [ ] Historia (13:45-15:15): **L5**",
  "- [ ] Econometría · pasos 6 y 10 (12:45-13:30): teoría, la ficha Dicom con la columna tapada y el núcleo de 12 ítems; los 5 huecos de las ayudantías (Youden, corte por utilidad +100/−500, EP de dummy y de término cuadrático, signo del WOE, MPL ≈ β/4) con la hoja de calcados C1-C6. Nada nuevo\n- [ ] Historia (13:45-15:15): **L5**"),
 ("**Fecha:** Microeconomía II: PEP 1\n",
  "**Fecha:** Econometría II: **PEP 1** (08:15 asumida, un bloque ~80 min, sala sin confirmar; traer calculadora) · Microeconomía II: PEP 1\n\n"
  "- [ ] Econometría · paso 11 (06:45-07:30): en frío, un ejercicio de cada tipo (logit + EM, matriz y corte, WOE ×100 e IV, DiD desde medias) + «Las 15 frases» (5 min) + la lista de fallas del paso 8\n"
  "- [ ] Econometría (08:15, asumida): **PEP 1**\n"),
 ("- [ ] Micro II (antes de la prueba, 1 h):", "- [ ] Micro II (12:45-13:45, después de Taller, 1 h):"),
]
for a,b in rep:
    assert a in s, a; s = s.replace(a,b,1)
f.write_text(s, encoding="utf-8")
print("ok")
