base = "C:/Proyecto Metodologia de estudio/datos/"
for rel in ("informe-pe/aportes-desde-ramos.md", "material/macroeconomia-ii/2026-10-29-prediccion-control-2.md"):
    p = base + rel
    s = open(p, encoding="utf-8", newline="").read()
    n = s.count(chr(7)) + s.count(chr(9) + "heta")
    s = s.replace(chr(7) + "pprox", "\\" + "approx").replace(chr(9) + "heta", "\\" + "theta")
    open(p, "w", encoding="utf-8", newline="").write(s)
    print(rel, "corregidos:", n, "quedan:", s.count(chr(7)), s.count(chr(9) + "heta"))
