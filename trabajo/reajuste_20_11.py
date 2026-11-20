f = "C:/Proyecto Metodologia de estudio/datos/agenda/semanas/2026-11-16.md"
s = open(f, encoding="utf-8").read()
P = "(`agenda/plan-pep-noviembre.md`)"
for a, b in [
    ("- [ ] **Base 10:00** (65): μ1 · M4 (ítem 0 de la cola; reajuste 19-11, §3 bis)",
     "- [~] **Base 10:00** (65): μ1 · M4 → a medias: errores del 18 (E1) hechos y C1 empezado; sigue el vie 20 a las 17:30 (ítem 0 de la cola; reajuste 19-11, §3 bis)"),
    ("- [ ] **Informe I2** (11:30-12:45",
     "- [~] **Informe I2** → no se hizo (el chat del informe dejó una propuesta autónoma el 19 en la noche, para revisar) (11:30-12:45"),
    ("- [ ] **Base 15:00** (65): E3 · M5 " + P,
     "- [~] **Base 15:00** (65): E3 · M5 → pasa al sáb 21 a las 10:00 " + P),
    ("- [ ] **Base 10:00** (65): μ2 · H1 = ficha R1",
     "- [ ] **Base 17:30** (65): terminar μ1 (C1-C2) · M4 (Principal II d-f), atrasado del jue 19 " + P + "\n- [~] **Base 10:00** (65): μ2 · H1 = ficha R1 → μ2 pasa al sáb 21 en la tarde; H1 queda en la cola (reajuste 20-11)"),
    ("- [ ] **Informe I3** (11:30-12:45",
     "- [~] **Informe I3** → no se hizo (11:30-12:45"),
    ("- [ ] **Base 15:00** (65): E4 · M6 " + P,
     "- [~] **Base 15:00** (65): E4 · M6 → M6 pasa al sáb 21 en la tarde; E4 queda en la cola (reajuste 20-11) " + P),
    ("- [ ] **Base 10:00** (65): μ3 · M7 (E5 pasa al lun 23)",
     "- [ ] **Base 10:00** (65): E3 · M5 (atrasado del jue 19; reajuste 20-11)\n- [ ] **Base 15:00** (65, se usa el comodín de la tarde): μ2 · M6 (atrasado del vie 20) " + P + "\n- [~] μ3 · M7 → quedan en la cola, junto con E4 y H1 (reajuste 20-11; E5 pasa al lun 23)"),
]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(f, "w", encoding="utf-8").write(s)
print("ok")
