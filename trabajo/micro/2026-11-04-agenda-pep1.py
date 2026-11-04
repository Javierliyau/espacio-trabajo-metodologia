# Inserta las filas del INDICE, actualiza el calendario y el plan de las semanas para la PEP 1 de Micro.
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
P = Path("C:/Proyecto Metodologia de estudio/datos")

def cambiar(ruta, viejo, nuevo):
    t = ruta.read_text(encoding="utf-8")
    assert t.count(viejo) == 1, (ruta.name, viejo[:60], t.count(viejo))
    ruta.write_text(t.replace(viejo, nuevo), encoding="utf-8")
    print("ok", ruta.name, "·", viejo[:50])

ind = P / "material/microeconomia-ii/INDICE.md"
fila = "| `2026-11-01-feedback-control-1.md` |"
t = ind.read_text(encoding="utf-8")
lin = next(l for l in t.splitlines() if l.startswith(fila))
cambiar(ind, lin, lin + "\n"
 "| `2026-11-04-prediccion-pep-1-mundaca.tex/.pdf` | (propio) | **U1, U2 y juegos · PEP 1** | Predicción por pregunta (registrada en el motor antes de la prueba, no retroactiva), respuestas cortas y plan de estudio de ~9 h. Alcance: todo hasta antes de oligopolio |\n"
 "| `2026-11-04-simulacro-pep-1-mundaca.tex/.pdf` | (propio) | **U1, U2 y juegos · PEP 1** | Simulacro de 60 pts y 80 min con el formato de Mundaca: 4 comentes, matriz 3×3 y árbol de entrada, 3.er grado con demanda quebrada; reserva de dos partes. Pauta en `2026-11-04-simulacro-pep-1-PAUTA-no-abrir.md` |")

cal = P / "agenda/calendario.md"
cambiar(cal, "| 2026-11-12 | — | Microeconomía II | PEP 1 | por confirmar | slides de repaso p. 3 |",
 "| 2026-11-12 | — | Microeconomía II | **PEP 1** (35 %). **Entra todo hasta antes de oligopolio**: monopolio, discriminación (1.er, 2.º y 3.er grado, paquetes, dos partes), competencia monopolística, Hotelling y teoría de juegos. El profesor sugirió que el matemático podría ser de discriminación y revisar las ayudantías. Hora, sala y duración sin confirmar; preguntar el jue 5-11 si entran juegos secuenciales. Predicción y plan: `material/microeconomia-ii/2026-11-04-prediccion-pep-1-mundaca.pdf` | por confirmar | slides de repaso p. 3 · dato del estudiante 4-11 |")

s1 = P / "agenda/semanas/2026-11-02.md"
cambiar(s1, "### 2026-11-06 · vie",
 "- [ ] Micro II (13:45, en clase, 5 min): preguntar fecha, hora y duración de la PEP 1, si entran juegos secuenciales (árbol) y el dilema repetido. Anotar la respuesta en `calendario.md`\n\n### 2026-11-06 · vie")

s2 = P / "agenda/semanas/2026-11-09.md"
t = s2.read_text(encoding="utf-8").splitlines()
nuevos = {
 "- [ ] Micro II (noche, ~1 h)": "- [ ] Micro II (noche, ~1,5 h): **diagnóstico** con la PEP 1 2026-1 de Mundaca completa, sin mirar (60 min), corregida con la pauta propuesta (ficha del banco). Solo marcar qué falla. Plan: `material/microeconomia-ii/2026-11-04-prediccion-pep-1-mundaca.pdf` §7",
 "- [ ] Micro II (tarde, ~3 h)": "- [ ] Micro II (tarde, ~3 h): **discriminación en cálculo** (1,5 h): A2 ej. 2, A3 ej. 4 y A4 ej. 3 sin mirar, luego A3 ej. 5 y A4 ej. 4 (dos partes; comparar con atender solo al tipo alto). **Juegos** (1,5 h): slides `2026-11-01-teoria-de-juegos.pdf` pp. 20-76, la matriz de la PEP 1 2026-1 y el árbol de la Suficiencia 2026-1",
 "- [ ] Micro II (mañana, ~3 h)": "- [ ] Micro II (mañana, ~3 h): **simulacro** `2026-11-04-simulacro-pep-1-mundaca.pdf` cronometrado (80 min), corregir con la pauta y volver solo a las fallas; 30 min de competencia monopolística (A4 ej. 5) y Hotelling (slides pp. 58-79)",
 "- [ ] Micro II (mañana, 1 h)": "- [ ] Micro II (antes de la prueba, 1 h): §6 de la predicción y la lista de errores: veredicto en la primera palabra, IMg = P(1 − 1/|ε|), cerrar con ES_CP − ES = PIE, revisar si conviene excluir a un grupo",
}
n = 0
for i, l in enumerate(t):
    for k, v in nuevos.items():
        if l.startswith(k):
            t[i] = v; n += 1
assert n == 4, n
s2.write_text("\n".join(t) + "\n", encoding="utf-8")
print("ok", s2.name, "·", n, "líneas de Micro")
