import os
os.chdir(r"C:/Proyecto Metodologia de estudio/datos")
M9 = "`material/historia-economica-mundial/2026-11-06-metodo-fichas-pep-1.md` §9"
PP = "`agenda/plan-paro.md` §12"


def rd(p):
    s = open(p, encoding="utf-8", newline="").read()
    return s, ("\r\n" if "\r\n" in s else "\n")


def wr(p, s):
    open(p, "w", encoding="utf-8", newline="").write(s)


def edit(p, pairs):
    s, nl = rd(p)
    for old, new in pairs:
        old = old.replace("\n", nl); new = new.replace("\n", nl)
        assert old in s, (p, old[:70])
        s = s.replace(old, new, 1)
    wr(p, s)


def insert_after(p, header, item):
    s, nl = rd(p)
    i = s.index(header); j = s.index(nl, i) + len(nl)
    if s.startswith(nl, j):
        j += len(nl)
    wr(p, s[:j] + item + nl + s[j:])


sec12 = """
## 12. Historia: fichas para llevar a la PEP (13-11, recalibrado)

**Por qué cambia:** el profesor permite llevar a la PEP los apuntes en hojas de notas bibliográficas (dato del estudiante, 13-11). Para Historia ya no se trata de mantener lo aprendido: hay que **construir** las fichas, y eso no cabe en la sesión de las 10:00, que está hecha para recuperar. Por eso Historia tiene su propio **bloque de fichas en la tarde** (como el informe del §11) y en la sesión de la mañana solo hace recuperaciones y ensayos con reloj. Cómo es cada ficha y cómo se usa en la prueba: """ + M9 + """.

**Cuánto es (estimación realista):**

| Parte | Tiempo |
|---|---:|
| Fichas: R1 y R2 (~45 c/u, las primeras son lentas) · R4 (30) · R3 y R7 (45) · P de R5, R6, R8 y R9 (20) · 12 C (36) · índice y pestañas (10) | **~3 h 50** |
| Lecturas que faltan, solo para sacar las citas: L6 O'Rourke y L7 Lindert y Williamson (30 c/u) · *opcional:* L5 Clark cap. 13 (30) | **1 h a 1 h 30** (0 si ya las leíste) |
| Recuperaciones y ensayos con reloj (R1, R2, pregunta sorpresa) y repaso final | **~2 h 10** |
| **Total** | **~6 h a 7 h 30** (~6 h sin la L5; ~5 h si ya leíste la L6 y la L7) |

**Calendario (PEP tentativa: vie 27):**

| Día | Mañana (sesión de las 10:00, bloque de Historia) | Tarde (bloque de fichas, 15:00) |
|---|---|---|
| **vie 13** | — | **R1**: P + A-01 a A-04 (45). Foto al chat |
| sáb 14 | — | **R2**: P + A-05 a A-08 (45) |
| dom 15 | Libre | Libre |
| lun 16 | R1 y R2 tapadas: tesis y cadenas en 60 s por A (25) | **L6 y L7**: lectura dirigida, solo las citas para A-09 a A-12 (60) |
| mar 17 | — | **R4**: P + A-09 a A-12 (30) · P de R5 y R6 (10) |
| **mié 18** | **R1 con reloj y fichas en la mano** (14 + 6 de corrección, 25) | **R3 y R7**: 2-3 A cada una (45; R7 desde el trabajo de la L8 y el tema 5) |
| jue 19 | — | **12 fichas C** + P de R8 y R9 (45). *Opcional:* L5 Clark (30) |
| **vie 20** | — | Bloque B del §8.1: **R2 con reloj y fichas** (20) + índice y pestañas (10) |
| sáb 21 a mar 24 | Sin Historia: Macro, Econometría y Micro | — |
| **mié 25** | — | **Pregunta sorpresa** con fichas: esquema en 5 min y 14 de escritura (30) |
| jue 26 | — | Noche: ordenar el mazo y leer las tesis (15) |
| vie 27 | 08:45: hojear las tesis (15). **Llevar el mazo y el índice** | — |

- **Con el informe de Política Económica (§11):** de lun a jue, la tarde parte con Historia y el informe sigue después, si hay ganas. Las fichas tienen prioridad porque van a la nota en dos semanas.
- **Regla de recorte:** primero sale la L5, después R6, después C-10 a C-12 y después R8 y R9. **No se recortan nunca:** R1, R2, R4 ni los tres ensayos con reloj.
- **Si cambia la fecha (D = día de la PEP):** las fichas se terminan en D−7, R1 con reloj va en D−9 o antes, R2 en D−7 y la pregunta sorpresa en D−2. El tablero (Hi1-Hi15) queda en pausa: el repaso de Historia es esta tabla.
- **Por confirmar con Robles:** cuántas fichas, tamaño, si deben ser manuscritas y si pueden traer la respuesta armada.
"""

# plan-paro
edit("agenda/plan-paro.md", [
    ("| Semana del 16-11 | Historia + Macro | Econometría + Política Económica | Micro + Historia | Macro + Econometría | Micro + Política Económica | Jefe final |",
     "| Semana del 16-11 | Historia + Macro | Econometría + Política Económica | Micro + Historia | Macro + Econometría | Micro + Política Económica | Jefe final |\n\n**Historia (13-11):** además de la rotación, tiene un bloque de fichas en la tarde hasta el vie 20 (§12). En la mañana solo hace recuperaciones y ensayos."),
    ("| vie 20 | **Macro: simulacro del 8-11, Partes I y II con reloj** (90, D−3) | — |",
     "| vie 20 | **Macro: simulacro del 8-11, Partes I y II con reloj** (90, D−3) | **Historia: R2 con reloj y fichas + índice** (30; §12) |"),
    ("- Si una fecha se confirma distinta, se rehace solo esa fila con el protocolo de arriba. Si el jue 26 tiene una sola PEP, la otra libera su bloque para Historia.",
     "- Si una fecha se confirma distinta, se rehace solo esa fila con el protocolo de arriba. Si el jue 26 tiene una sola PEP, la otra libera su bloque para Historia.\n- Historia (fichas para llevar) tiene su calendario propio en el §12."),
    ("- **Meta:** unas 10 h por semana,",
     "- **Del 13 al 20-11:** el bloque de la tarde parte con las fichas de Historia (§12) y el informe sigue después.\n- **Meta:** unas 10 h por semana,"),
])
s, nl = rd("agenda/plan-paro.md")
if not s.endswith(nl):
    s += nl
wr("agenda/plan-paro.md", s + sec12.replace("\n", nl))

# método §9
p = "material/historia-economica-mundial/2026-11-06-metodo-fichas-pep-1.md"
s, nl = rd(p)
a = s.index("### Calendario (para la PEP tentativa del vie 27)"); b = s.index("**C-7 a C-12:**")
s = (s[:a] + "### Calendario y tiempos" + nl + nl + "Recalibrado el 13-11 y movido a " + PP
     + ": un bloque de fichas en la tarde hasta el vie 20 y ensayos con reloj (R1 el mié 18, R2 el vie 20 y la pregunta sorpresa el mié 25). **Total realista: ~6 h a 7 h 30**, contando las lecturas L6 y L7 si no están leídas." + nl + nl + s[b:])
old = "**Regla de recorte:** primero sale R6, después C-10 a C-12, después R8 y R9."
assert old in s
s = s.replace(old, "**Regla de recorte:** primero sale la L5, después R6, después C-10 a C-12 y después R8 y R9.")
wr(p, s)

# semana del 9
w9 = "agenda/semanas/2026-11-09.md"
edit(w9, [
    ("- [ ] Historia · fichas para llevar a la PEP (30, reemplaza Hi1-Hi4): **R1**, P + A-01 a A-04 a mano; foto al chat (" + M9 + ")",
     "- [ ] Historia · fichas para llevar a la PEP (tarde, 45; reemplaza Hi1-Hi4): **R1**, P + A-01 a A-04 a mano; foto al chat (" + PP + ")"),
    ("- [ ] Historia · fichas para llevar (30): **R2**, P + A-05 a A-08 (" + M9 + ")\n", ""),
])
insert_after(w9, "### 2026-11-14 · sáb", "- [ ] Historia · fichas para llevar (tarde, 45): **R2**, P + A-05 a A-08 (" + PP + ")")

# semana del 16
w = "agenda/semanas/2026-11-16.md"
edit(w, [
    ("**Historia** (fichas para llevar, 30: **R4**, P + A-09 a A-12; verificar A-12 en la L6; " + M9 + ")",
     "**Historia** (25: R1 y R2 tapadas, tesis y cadenas en 60 s por A; " + PP + ")"),
    ("**Historia** (35: **R1 con reloj y con las fichas en la mano** + fichas P de R5 y R6; " + M9 + ")",
     "**Historia** (25: **R1 con reloj y con las fichas en la mano**, 14 + 6 de corrección; " + PP + ")"),
    ("- [ ] Historia · fichas para llevar (30): **R3 y R7**, 2-3 A cada una (R7 desde el trabajo de la L8 y el tema 5; " + M9 + ")",
     "- [ ] Historia · fichas (tarde, 40): **R4**, P + A-09 a A-12 · P de R5 y R6 (" + PP + ")"),
    ("- [ ] Historia · fichas para llevar (20): **C-1 a C-6** (" + M9 + ")",
     "- [ ] Historia · fichas (tarde, 45): **12 fichas C** + P de R8 y R9 · *opcional:* L5 Clark (30) (" + PP + ")"),
    ("- [ ] Historia (40): **R2 con reloj y con las fichas** (14 + corrección) · ficha índice y pestañas de color (" + M9 + ")",
     "- [ ] Historia (30): **R2 con reloj y con las fichas** (14 + 6 de corrección) · ficha índice y pestañas de color (" + PP + ")"),
    ("- [ ] Historia (25): **C-7 a C-12** + fichas P de R8 y R9 (" + M9 + ")\n", ""),
])
insert_after(w, "### 2026-11-16 · lun", "- [ ] Historia · fichas (tarde, 60): **L6 O'Rourke y L7 Lindert y Williamson**, lectura dirigida solo para las citas de A-09 a A-12 (si ya están leídas, se salta) (" + PP + ")")
insert_after(w, "### 2026-11-18 · mié", "- [ ] Historia · fichas (tarde, 45): **R3 y R7**, 2-3 A cada una (R7 desde el trabajo de la L8 y el tema 5; " + PP + ")")
print("ok")
