# Integra la d) ampliada de la P1 en la pauta completa con formato de libro.
import pathlib
d = pathlib.Path(r"C:/Proyecto Metodologia de estudio/datos/material/econometria-ii")
p1 = (d / "2026-11-04-simulacro-final-pep1-pauta-p1-libro.tex").read_text(encoding="utf-8")
full_path = d / "2026-11-04-simulacro-final-pep1-pauta-libro.tex"
full = full_path.read_text(encoding="utf-8")
ini, fin = r"\sub{d) Odds}", r"\sub{e) Matriz"
bloque = p1[p1.index(ini):p1.index(fin)]
a, b = full.index(ini), full.index(fin)
if "Cómo se calcula el 200" not in full[a:b]:
    full = full[:a] + bloque + full[b:]
    full_path.write_text(full, encoding="utf-8")
print("ok")
