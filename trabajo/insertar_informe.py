import re, sys
base = "C:/Proyecto Metodologia de estudio/datos/agenda/semanas/"
P = "- [ ] *(opcional)* **Informe de Política Económica** (15:00-17:00, `plan-paro.md` §11; en `C:\\Proyecto Informe PIB Tendencial` con `/retomar informe-43`): "
tareas = {
    "2026-11-09.md": {
        "2026-11-11": "anotar el feedback de Salas y Alex del 26-10 en §9 y pasar los aportes «nuevo» de `informe-pe/aportes-desde-ramos.md`; reajustar el calendario del informe",
        "2026-11-12": "S6: bajar los datos del BCCh y del INE (PIB, FBCF, stock de capital, empleo y horas)",
        "2026-11-13": "S6: terminar los datos y armar la planilla de contabilidad K-L-PTF",
    },
    "2026-11-16.md": {
        "2026-11-16": "S6: contabilidad K-L-PTF → **Tabla 2** (fuentes del crecimiento)",
        "2026-11-17": "S6: cerrar la Tabla 2 y escribir su párrafo",
        "2026-11-18": "S7: **triángulo de vintages** con las actas 2002-2026",
        "2026-11-19": "S7: terminar el triángulo; si hay clases, el bloque se reajusta al horario",
        "2026-11-20": "S7: **4.1 en borrador**",
    },
}
for f, dias in tareas.items():
    lines = open(base + f, encoding="utf-8").read().split("\n")
    out, dia = [], None
    for ln in lines:
        out.append(ln)
        m = re.match(r"### (\d{4}-\d{2}-\d{2})", ln)
        if m:
            dia = m.group(1)
        if dia in dias and ln.startswith("- [ ] **Sesión de paro**"):
            out.append(P + dias[dia])
            dias.pop(dia)
    if dias:
        sys.exit(f"faltó insertar en {f}: {list(dias)}")
    open(base + f, "w", encoding="utf-8").write("\n".join(out))
print("ok")
