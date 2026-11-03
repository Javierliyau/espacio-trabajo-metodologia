# De donde sale el paso de v1.1 sobre v1.0: compuerta por ramo y efecto de la correccion del Control 1. No escribe nada.
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path.home() / ".claude/skills/banco-evaluaciones/scripts"))
import motor as M

datos = M.cargar_datos()
print("ramos:", [(d["ramo"], len(d["items"]["evaluaciones"])) for d in datos])
c = M.walk_forward(M.cargar_version("1.0"), datos)
r = M.walk_forward(M.cargar_version("1.1"), datos)
print("claves de fila:", sorted(c[0]))


def ramo_de(f):
    return f.get("ramo") or "?"


def mostrar(nombre, fc, fr):
    if not fc:
        print(f"{nombre}: sin filas")
        return
    g = M.compuerta(fc, fr)
    ic = f"[{g['ic90'][0]:+.4f}, {g['ic90'][1]:+.4f}]" if g["ic90"] else "—"
    print(f"{nombre:28} n={g['n']:2} dBrier {g['dif_brier']:+.4f} IC90 {ic} cuad {g['cuad_retador']:.4f} vs "
          f"{g['cuad_campeon']:.4f} pasa={g['pasa']}")


mostrar("todos", c, r)
for x in sorted({ramo_de(f) for f in c}):
    mostrar(x, [f for f in c if ramo_de(f) == x], [f for f in r if ramo_de(f) == x])
sin = lambda fs: [f for f in fs if ramo_de(f) != "Mate 2"]
mostrar("sin Mate 2", sin(c), sin(r))

print("\nfilas en que cambia el Brier (v1.0 -> v1.1):")
for a, b in zip(c, r):
    x, y = M.brier_prueba(a), M.brier_prueba(b)
    if abs(x - y) > 1e-9:
        print(f"  {ramo_de(a):20} {str(a.get('id') or a.get('evaluacion'))[:44]:44} {x:.3f} -> {y:.3f}")
