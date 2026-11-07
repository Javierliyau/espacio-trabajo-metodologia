import io
p = "C:/Proyecto Metodologia de estudio/datos/agenda/semanas/2026-11-02.md"
s = io.open(p, encoding="utf-8").read()
L = s.split("\n")
def find(prefix):
    for i, l in enumerate(L):
        if l.startswith(prefix): return i
    raise SystemExit("no " + prefix)
iA = find("- [ ] Econometría · **sesión A**")
iB = find("- [ ] Econometría · **sesión B**")
i1 = find("- [ ] Micro · **μ1**")
i2 = find("- [ ] Micro · **μ2**")
iC = find("- [ ] Econometría · **sesión C**")
iM1 = find("- [ ] Macro · **M1** ")
iM1b = find("- [ ] Macro · **M1b**")
iM2 = find("- [ ] Macro · **M2**")
iD = find("- [ ] Econometría · **sesión D**")
i3 = find("- [ ] Micro · **μ3**")
i4 = find("- [ ] Micro · **μ4**")
iH = find("- [ ] Historia (metro o noche")
iM3 = find("- [ ] Macro · **M3**")
iM4 = find("- [ ] Macro · **M4**")
iE = find("- [ ] Econometría · **sesión E**")
i5 = find("- [ ] Micro · **μ5**")
i6 = find("- [ ] Micro · **μ6**")
def body(i):  # texto después del primer paréntesis de hora
    l = L[i]; return l[l.index("):")+2:]
A, B, C = body(iA), body(iB), body(iC)
mu1, M1, M1b, M2 = body(i1), body(iM1), body(iM1b), body(iM2)
mu3, mu4, M3, M4 = body(i3), body(i4), body(iM3), body(iM4)
B = B.split(". Opcional")[0]
viejo_vie = [L[iA], L[iB], L[i1], L[i2], L[iC], L[iM1], L[iM1b]]
nuevo_vie = [
 "- [x] **Hecho el viernes (planificación; ninguna sesión de estudio):** Econometría: plan de repaso v1 → v3 (dos bloques) y hoja de ampliación A1-A7 · Micro: plan conjunto μ1-μ12 · Macro: guía subida, predicción final v2 pre-registrada, plan meta 6,0, diagnóstico B1 corregido (B2 a mitad) y comentes de convergencia con casos africanos · Historia: slides 5, 6A y 7 ordenados, predicción PEP 1, método de fichas y plan mínimo",
 "- [~] Econometría · **sesión A** → sáb 7 (13:45)",
 "- [~] Econometría · **sesión B** → dom 8 (13:00), sin el opcional",
 "- [~] Micro · **μ1** → sáb 7 (17:30), con lo nuevo de paquetes de μ2",
 "- [~] Micro · **μ2** → se reparte: paquetes → μ1 (sáb 7) · A4 ej. 5, C3 del Control 1 y D1 → μ6-7 (lun 9)",
 "- [~] Econometría · **sesión C** → sáb 7 (22:30)",
 "- [~] Macro · **M1** y **M1b** → sáb 7 (11:30 y 12:10)",
]
# reconstruir viernes
iSab = find("### 2026-11-07 · sáb")
vie = [l for l in L[:iSab] if l not in viejo_vie]
pos = vie.index(next(l for l in vie if l.startswith("- [~] Econometría · paso 11"))) + 1
vie[pos:pos] = nuevo_vie
sab = [
 "### 2026-11-07 · sáb", "",
 "**Reajuste (sáb 7, 11:15), solo con lo del viernes:** el vie 6 se fue en planificar y no se hizo ninguna sesión (A, B, C, μ1, μ2, M1, M1b). Todo se corre desde ahora, con Macro primero hasta el lun 9 y tope ~5 h por día. Para que quepa: μ2 se reparte (paquetes → μ1; A4 ej. 5, C3 y D1 → μ6-7), μ6 y μ7 se juntan el lun 9, μ8 se junta con μ11 el mié 11, Econometría D-G se corre un día y F se junta con H el mié 11. Fechas de prueba sin cambios.", "",
 "- [ ] Macro · **M1** (11:30-12:00, 30 min):" + M1,
 "- [ ] Macro · **M1b** (12:10-12:55, 45 min; **meta 6,0**):" + M1b,
 "- [ ] (12:55-13:45) almuerzo, sin pantalla",
 "- [ ] Econometría · **sesión A** (13:45-14:45, 60 min):" + A,
 "- [ ] Macro · **M2** (15:00-17:00, 120 min; meta 6,0):" + M2.split("; meta 6,0):",1)[-1] if "; meta 6,0):" in L[iM2] else "- [ ] Macro · **M2** (15:00-17:00, 120 min):" + M2,
 "- [ ] Micro · **μ1** (17:30-18:10, 40 min):" + mu1 + " · **+15: paquetes, nuevo** (slides de juegos pp. 41-44 y comente C11; M9; viene de μ2)",
 "- [ ] Econometría · **sesión C** (22:30, 14 min, antes de dormir):" + C,
 L[iH],
 "- [~] Econometría · **sesión D** → lun 9 (12:00)",
 "- [~] Micro · **μ3** y **μ4** → dom 8 (15:00 y 17:30)",
 "",
]
iDom = find("### 2026-11-08 · dom")
dom_head = L[iDom:iDom+3]  # encabezado, línea vacía, nota Etapa 3
resto = L[i6+1:]  # líneas después de μ6 (hoja de memoria, lun 9)
dom = dom_head + [""] + [
 L[iM3], L[iM4],
 "- [ ] Econometría · **sesión B** (13:00-13:45, 45 min; viene del vie 6, sin el opcional):" + B,
 "- [ ] Micro · **μ3** (15:00-16:50, 97 min en bloques de 25 + 5; viene del sáb):" + mu3,
 "- [ ] Micro · **μ4** (17:30-18:20, 48 min; viene del sáb):" + mu4 + ". Después, nada más: a dormir temprano por Macro",
 "- [~] Econometría · **sesión E** → mar 10 (12:00)",
 "- [~] Micro · **μ5** → lun 9 (16:15) · **μ6** → lun 9 (20:00, junto con μ7)",
] + resto
# M2: dejar texto limpio
for k, l in enumerate(sab):
    if l.startswith("- [ ] Macro · **M2**") or ("Solow de la guía en frío" in l and not l.startswith("- [ ] Macro")):
        sab[k] = "- [ ] Macro · **M2** (15:00-17:00, 120 min; meta 6,0):" + L[iM2].split("meta 6,0):",1)[1]
out = "\n".join(vie + sab + dom)
io.open(p, "w", encoding="utf-8", newline="\n").write(out)
print(out[out.index("### 2026-11-06"):][:200])
