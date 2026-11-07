import io
p = "C:/Proyecto Metodologia de estudio/datos/agenda/semanas/2026-11-09.md"
L = io.open(p, encoding="utf-8").read().split("\n")
iD = next(i for i,l in enumerate(L) if l.startswith("- [ ] Econometría · **sesión D**"))
iC = next(i for i,l in enumerate(L) if l.startswith("- [ ] Historia (11:15"))
L.insert(iD, L.pop(iC))
io.open(p,"w",encoding="utf-8",newline="\n").write("\n".join(L))

p = "C:/Proyecto Metodologia de estudio/datos/agenda/calendario.md"
s = io.open(p, encoding="utf-8").read()
R = [
 ("Fechas exactas de los demás ramos sin confirmar | por confirmar | dato del estudiante · ficha informe-43 |",
  "Fechas exactas de los demás ramos sin confirmar | hecho (al 6-11 ya están todas: Macro lun 9, Econometría y Micro jue 12, Historia vie 13; ver la fila del 9-11) | dato del estudiante · ficha informe-43 · estudiante 6-11 |"),
 ("Cimientos de la predicción: `material/macroeconomia-ii/2026-11-04-cimientos-prediccion-pep-1.md` | pendiente | correo Droller 7-10; temario y formato dichos en clase (dato del estudiante 4-11) |",
  "Cimientos de la predicción: `material/macroeconomia-ii/2026-11-04-cimientos-prediccion-pep-1.md` · **Predicción final v2 pre-registrada con la guía del ayudante (6-11): `material/macroeconomia-ii/2026-11-06-prediccion-final-pep-1.md`. Meta 6,0 (52/60): `2026-11-06-plan-pep-1-meta-6.md` (M1-M5; reajustado el 7-11 porque el vie 6 no hubo sesiones)** | pendiente | correo Droller 7-10; temario y formato dichos en clase (dato del estudiante 4-11) · guía del ayudante 6-11 |"),
 ("(ese día también va la Lectura 7) | pendiente | calendario de presentaciones |",
  "(ese día también va la Lectura 7). **Semana sin clases (6-11): no se sabe si se mantiene**; se pregunta en el correo al profesor del lun 9, 11:15 | por confirmar | calendario de presentaciones · estudiante 6-11 |"),
 ("Hora, sala y duración sin confirmar; preguntar el jue 5-11 si entran juegos secuenciales.",
  "Hora, sala y duración sin confirmar; **como no hay clase el mar 10, se pregunta por correo el lun 9 (11:15)**: hora, sala, duración y si entran juegos secuenciales. Plan conjunto con Econometría (μ1-μ12, 6-11; reajustado el 7-11): `material/microeconomia-ii/2026-11-06-plan-conjunto-pep1-econometria-micro.md`."),
 ("| 2026-11-13 | 11:25 | Historia Económica Mundial | **PEP 1**. Hora asumida 11:25 (bloque V3 del viernes), sin confirmar | pendiente |",
  "| 2026-11-13 | 11:25 | Historia Económica Mundial | **PEP 1**. Hora asumida 11:25 (bloque V3 del viernes), sin confirmar. Formato, duración, guía y si se puede llevar alguna ficha: se pregunta en el correo del lun 9. Predicción y plan: `material/historia-economica-mundial/2026-11-06-prediccion-pep-1-y-plan-fichas.md` y `2026-11-06-metodo-fichas-pep-1.md` §7 (plan mínimo, 6-11) | pendiente |"),
 ("Celulares adelante | pendiente | correo Riquelme 6-11",
  "Celulares adelante. Plan de repaso v3 (sesiones A-J, 6-11; reajustado el 7-11): `material/econometria-ii/2026-11-06-plan-repaso-espaciado-pep1.md` | pendiente | correo Riquelme 6-11"),
]
for a,b in R:
    assert s.count(a)==1, a[:60]
    s = s.replace(a,b)
io.open(p,"w",encoding="utf-8",newline="\n").write(s)
print("ok")
