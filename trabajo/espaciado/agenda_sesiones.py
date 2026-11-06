import pathlib
P=pathlib.Path("C:/Proyecto Metodologia de estudio/datos/agenda/semanas")
PL="`material/econometria-ii/2026-11-06-plan-repaso-espaciado-pep1.md`"
def edit(fn,reps):
    f=P/fn; s=f.read_text(encoding="utf-8")
    for a,b in reps:
        assert a in s,(fn,a[:60]); s=s.replace(a,b,1)
    f.write_text(s,encoding="utf-8")
edit("2026-11-02.md",[
 ("- [ ] Econometría · paso 8 (hoy, 1 h, con el simulacro fresco): corregir el simulacro de anoche con `material/econometria-ii/2026-11-04-simulacro-final-pep1-pauta-libro.pdf` y anotar en una lista solo las fallas (son la base de los pasos 9 y 10)",
  f"- [ ] Econometría · **sesión A** (11:00, 60 min): corregir el simulacro de anoche con la pauta (`2026-11-04-simulacro-final-pep1-pauta-libro.pdf`) y armar la **lista de fallas** + C5 (PDO) + MPL y β/4 de memoria. Plan: {PL}\n"
  "- [ ] Econometría · **sesión B** (16:00, 90 min): ampliar con la hoja `2026-11-06-hoja-ampliacion-pep1.md` (A1 salida de glm/RV/McFadden, A2 Youden/utilidad/ROC/KS, A3 cuadrático, A5) + preguntas de la lectura M2 en frío (Econometría I)\n"
  "- [ ] Econometría · **sesión C** (22:30, 10 min, antes de dormir): A1 b-c y A2 a-b sin mirar"),
 ("- [ ] Historia (metro o noche, si queda energía): seguir con la L1-L3 en el Kindle",
  "- [ ] Econometría · **sesión D** (13:00, 25 min): 3A con otros números (WOE ×100) · 4 casos de amenazas con la dirección del sesgo · A4 (PDO)\n- [ ] Historia (metro o noche, si queda energía): seguir con la L1-L3 en el Kindle"),
 ("- [ ] Econometría (15 min, no-cero): el núcleo de teoría (12 ítems, 8 min) en voz alta + releer la lista de fallas del paso 8; nada nuevo",
  "- [ ] Econometría · **sesión E** (13:00, 25 min): C1 c) · núcleo de 12 V/F en voz alta (8 min) · A1 con la pauta tapada"),
])
edit("2026-11-09.md",[
 ("- [ ] Historia (tarde, ~2 h): armar la presentación",
  "- [ ] Econometría · **sesión F** (12:00, 30 min, después de la PEP): C4 (WOE/IV) · C2 a) · 2×2 de C6 · A2 c-e\n- [ ] Historia (tarde, ~2 h): armar la presentación"),
 ("- [ ] Econometría · paso 9 (13:00-14:00, antes de Micro): **ayudantía 5, P2-P4** cronometradas (~30 min, `material/econometria-ii/2026-11-05-ayudantia-5-ejercicios-pauta.pdf`) y corregir solo las fallas; reemplaza el simulacro corto (es el material con más probabilidad de calcado)",
  "- [ ] Econometría · **sesión G** (13:00-14:00, antes de Micro): mini-simulacro mezclado: **ayudantía 5, P2-P4** cronometradas (30 min) + C3 (matriz y Youden) + 3 V/F de scoring conceptual; corregir solo las fallas"),
 ("- [ ] Econometría · pasos 6 y 10 (12:45-13:30): teoría, la ficha Dicom con la columna tapada y el núcleo de 12 ítems; los 5 huecos de las ayudantías (Youden, corte por utilidad +100/−500, EP de dummy y de término cuadrático, signo del WOE, MPL ≈ β/4) con la hoja de calcados C1-C6. Nada nuevo",
  "- [ ] Econometría · **sesión H** (12:45-13:15): rehacer cada error de la lista de fallas con otros números · A5 · WOE e IV (T7) y Youden/KS (T6) en frío"),
 ("- [ ] Historia (noche, después de Sociología, ~2 h):",
  "- [ ] Econometría · **sesión I** (22:30, 15 min, antes de dormir): núcleo de 12 V/F (8 min) · A4 c). Después, nada nuevo: dormir 7-8 h\n- [ ] Historia (noche, después de Sociología, ~2 h):"),
 ("- [ ] Econometría · paso 11 (06:45-07:30): en frío, un ejercicio de cada tipo (logit + EM, matriz y corte, WOE ×100 e IV, DiD desde medias) + «Las 15 frases» (5 min) + la lista de fallas del paso 8",
  "- [ ] Econometría · **sesión J** (06:45-07:15): calentamiento: «Las 15 frases» (5 min), un logit de 2 líneas, la RV de A1, tendencias paralelas y ATT en una frase. Nada nuevo"),
])
print("ok")
