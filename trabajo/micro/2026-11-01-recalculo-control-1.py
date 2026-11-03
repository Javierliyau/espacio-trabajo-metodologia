# Recalcula la resolucion del Control 1 de Micro con el control original. Solo lee; no escribe en el banco.
import random
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path.home() / ".claude/skills/banco-evaluaciones/scripts"))
import banco as B
import motor as M

RAMO, RID = "Microeconomía II", "20261010-220946-control-1"
ind = B.leer_indice()
temario = M.leer_temario(RAMO)
items = M.leer(M.dir_motor(RAMO) / "items.json")
reg = M.leer_registro(RAMO, RID)
S = reg["alcance"]
c = reg["por_escenario"]["central"]
real = {"U1": 40 / 60, "U2": 20 / 60}  # C1, C4, D2, III = U1 / C2, C3, D1 = U2
fila = {"S": S, "real": real, "p": {u: c[u]["p"] for u in S}, "sh": {u: c[u]["e"] / 100 for u in S}}

ctx = M.ctx_registro(RAMO, ind, temario, items, reg)
previas = sorted(ctx["evs_ramo"] + ctx["evs_prof"], key=M.clave_orden)
bases = M.lineas_base(ctx, previas, S, "Mundaca", f"{reg['semilla']}-{reg['id']}-base", M.WF_CORRIDAS)


def fila_txt(nombre, f):
    m = M.metricas([f])
    print(f"{nombre:14} brier {M.brier_prueba(f):.3f}  cuad {m['cuad']:.3f}  top1 {m['top1']:.2f}  "
          f"p {({u: round(v, 2) for u, v in f['p'].items()})}  sh {({u: round(v, 2) for u, v in f['sh'].items()})}")


fila_txt("motor", fila)
for b, (p, sh) in bases.items():
    fila_txt(b, dict(fila, p=p, sh=sh))

print("\n-- tipo de pregunta: predicho 23/31/46, real 33/33/33")
pred, r = (.23, .31, .46), (1 / 3, 1 / 3, 1 / 3)
print("cuad tipo", round(sum((a - b) ** 2 for a, b in zip(pred, r)), 3))


def brier_items(nombre, xs):
    v = sum((p - o) ** 2 for p, o in xs) / len(xs)
    k = sum(o for _, o in xs)
    plana = k / len(xs)
    pl = sum((plana - o) ** 2 for _, o in xs) / len(xs)
    print(f"{nombre:12} n={len(xs):2} aciertos={k} brier={v:.3f} (plana con la tasa real {plana:.2f}: {pl:.3f})")


print("\n-- prediccion manual 21-10, literal")
comentes = [(.45, 0), (.40, 0), (.35, 0), (.35, 0), (.35, 0), (.35, 0), (.35, 0), (.30, 0), (.30, 0), (.25, 0), (.20, 1), (.15, 0)]
desarrollos = [(.70, 1), (.35, 0), (.35, 0), (.25, 0), (.20, 0), (.15, 1)]
mate = [(.85, 1), (.15, 0), (.65, 1), (.25, 0), (.10, 0)]
brier_items("comentes", comentes)
brier_items("desarrollos", desarrollos)
brier_items("matematico", mate)
brier_items("todo", comentes + desarrollos + mate)
