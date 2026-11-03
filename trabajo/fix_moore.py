p = "C:/Proyecto Metodologia de estudio/datos/material/macroeconomia-ii/2026-10-31-lectura-control-2-caso-moore.md"
s = open(p, encoding="utf-8").read()
for a, b in [
    ("### 5.1, los elementos básicos (pp. 99-103)", "### 5.1, los elementos básicos (pp. 98-103)"),
    ("**Política (pp. 106-107).**", "**Política (p. 107).**"),
    ("### 5.1.2, efecto tasa contra efecto nivel (pp. 106-107)", "### 5.1.2, efecto tasa contra efecto nivel (p. 107)"),
    ("**El resto del modelo (pp. 109-111).**", "**El resto del modelo (pp. 110-111).**"),
    ("con $\phi = 1$, (5.6) deja de determinar $g_A$ (caso 5.8)", "con $\phi = 1$ y $n > 0$ no hay tasa constante, porque se acelera (caso 5.8)"),
    ("Si los citas, no suman.", "No los necesitas para responder."),
]:
    assert a in s, a
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
