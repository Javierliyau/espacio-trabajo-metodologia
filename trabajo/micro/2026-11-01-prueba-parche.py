# Prueba el parche sobre una copia del banco (BANCO_DIR). No llama a ciclo: campeon.json vive fuera del banco.
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).parent
REAL = Path.home() / "OneDrive" / "BancoEvaluaciones"
tmp = Path(tempfile.mkdtemp(prefix="banco-prueba-"))
COPIA = tmp / "banco"
shutil.copytree(REAL, COPIA)
os.environ["BANCO_DIR"] = str(COPIA)
sys.path.insert(0, str(Path.home() / ".claude/skills/banco-evaluaciones/scripts"))
import banco as B
import motor as M

assert str(B.BANCO) == str(COPIA) and str(COPIA) in str(M.dir_motor("Microeconomía II"))
RAMO, ID = "Microeconomía II", "microeconomia-ii/2026-2-control-1-mundaca"
RID = "20261010-220946-control-1"
ORIG = M.dir_motor(RAMO) / "Resueltas" / f"{RID}.json"
sha = lambda f: hashlib.sha1(f.read_bytes()).hexdigest().upper()
assert sha(ORIG) == "6396563E00A958F5EA1E842B3396551225A76898"


def ok(nombre, cond, extra=""):
    print(("OK  " if cond else "MAL ") + nombre, extra)
    if not cond:
        sys.exit(1)


def carga():
    ind = B.leer_indice()
    tem = M.leer_temario(RAMO)
    items, _ = M.construir_items(RAMO, ind, tem)
    return ind, tem, items


# 1. parcial: la ficha de memoria queda marcada y fuera de la historia
ind, tem, items = carga()
print("parciales en todos los ramos:")
for r in sorted({m["ramo"] for m in ind["evaluaciones"].values()}):
    try:
        t = M.leer_temario(r)
    except SystemExit:
        continue
    it, _ = M.construir_items(r, ind, t)
    for i, e in it["evaluaciones"].items():
        if e["parcial"]:
            print("   ", r, i, "->", e["parcial"][:90])
ok("control 1 de memoria es parcial", bool(items["evaluaciones"][ID]["parcial"]))
ok("evaluar no resuelve una parcial", M.evaluar(RAMO, ind, tem, items, ID) is None)
reg = M.leer_registro(RAMO, RID)
ctx = M.ctx_registro(RAMO, ind, tem, items, reg)
ok("ctx_registro repite lo que vio el registro", True)
from datetime import date
ctx2 = M.contexto(RAMO, ind, tem, items, date(2026, 11, 12), "Mundaca", "PEP 1")
ok("contexto no usa la parcial", ID not in [e["id"] for e in ctx2["evs_ramo"] + ctx2["evs_prof"]])

# 2. ficha real
subprocess.run([sys.executable, str(AQUI / "2026-11-01-datos-control-1.py"), "ficha"], check=True, env=os.environ)
ind, tem, items = carga()
e = items["evaluaciones"][ID]
ok("ficha real no es parcial", e["parcial"] is None)
ok("7 items, 60 puntos", len(e["items"]) == 7 and sum(i["puntos"] for i in e["items"]) == 60)
v = M.verdad(e)
ok("reparto real U1 2/3, U2 1/3", abs(v.get("U1", 0) - 2 / 3) < .01 and abs(v.get("U2", 0) - 1 / 3) < .01, v)

# 3. dominio: la migracion y el retorno temprano
subprocess.run([sys.executable, str(AQUI / "2026-11-01-datos-control-1.py"), "dominio"], check=True, env=os.environ)
ok("resolver de nuevo no duplica", M.evaluar(RAMO, ind, tem, items, ID) is None)
d = M.leer(M.dir_motor(RAMO) / "dominio.json")
print("    dominio tras el retorno temprano:", {u: d[u] for u in ("U1", "U2")}, d.get("_fuentes"))
ok("el dominio sumo el control", ID in d["_fuentes"] and abs(d["U1"]["logrado"] - (2.325 + 3.7)) < .01
   and abs(d["U2"]["logrado"] - 1.4) < .01)
ok("U1 ~ 0,585", abs((d["U1"]["logrado"] + 1) / (d["U1"]["posible"] + 2) - .585) < .08,
   (d["U1"]["logrado"] / d["U1"]["posible"]))
M.evaluar(RAMO, ind, tem, items, ID)
d2 = M.leer(M.dir_motor(RAMO) / "dominio.json")
ok("el dominio no se suma dos veces", d2["U1"]["logrado"] == d["U1"]["logrado"])

# 4. corregir: original intacta, vigente con lo nuevo
r = M.corregir_resolucion(RAMO, ind, tem, items, ID, "Prueba del parche.")
ok("Resueltas intacta", sha(ORIG) == "6396563E00A958F5EA1E842B3396551225A76898")
vig = next(x for x in M.resoluciones(RAMO) if x["evaluacion_id"] == ID)
print("    vigente:", {k: round(x, 3) for k, x in vig["metricas"].items() if x is not None})
print("    bases:", {b: (round(x["brier"], 3), round(x["cuad"], 3)) for b, x in vig["bases"].items()})
print("    deriva:", vig["deriva"])
ok("trae el original", round(vig["original"]["metricas"]["brier"], 3) == 0.477, vig["correccion"])
ok("Brier .312 y cuad .200", round(vig["metricas"]["brier"], 3) == .312 and round(vig["metricas"]["cuad"], 3) == .2)
ok("sin deriva de 2 preguntas", not any("2 preguntas" in str(x) for x in vig["deriva"]))
cs = list((M.dir_motor(RAMO) / "Correcciones").glob("*.json"))
ok("correccion inmutable", len(cs) == 1 and not os.access(cs[0], os.W_OK))
pm = (M.postmortem(RAMO, tem, vig))
print("    postmortem:", pm)

# 5. dominio de practica
class A: pass
a = A(); a.unidad, a.obtenido, a.puntaje, a.preguntas, a.motivo = "U2", 8, 10, 1.0, "prueba"
antes = M.leer(M.dir_motor(RAMO) / "dominio.json")["U2"]["logrado"]
M.anotar_dominio(RAMO, tem, a)
ok("practica en la misma escala", abs(M.leer(M.dir_motor(RAMO) / "dominio.json")["U2"]["logrado"] - antes - .8) < 1e-6)

# 6. manual
subprocess.run([sys.executable, str(AQUI / "2026-11-01-datos-control-1.py"), "manual-json"], check=True, env=os.environ)
a = A(); a.evaluacion, a.periodo = "Control 1", "2026-2"
a.archivo = str(AQUI / "2026-11-01-manual-control-1.json")
M.registrar_manual(RAMO, a)
a.archivo = str(AQUI / "2026-11-01-manual-control-1-aciertos.json")
M.resolver_manual(RAMO, a)
i = M.id_manual("Control 1", "2026-2")
m = M.leer(M.dir_motor(RAMO) / "Manuales" / "Resueltas" / f"{i}.json")
ok("manual .143 / .170", round(m["total"]["brier"], 3) == .143 and round(m["total"]["plana"], 3) == .17)
ok("comentes .157", round(m["bloques"]["comentes"]["brier"], 3) == .157)
ok("desarrollos .193", round(m["bloques"]["desarrollos"]["brier"], 3) == .193)
ok("matematico .048", round(m["bloques"]["matemático"]["brier"], 3) == .048)
ok("retroactiva", m["retroactiva"] is True)

# 7. tablero en la copia
antes_tablero = sha(M.CAMPEON_FILE)
print("    tablero:", M.tablero())
ok("campeon.json sin tocar", sha(M.CAMPEON_FILE) == antes_tablero)
t = (COPIA / "Tablero.md")
if t.exists():
    x = t.read_text(encoding="utf-8")
    ok("el tablero muestra correccion y manual", "corregida" in x and "Predicciones manuales" in x)
print("    seccion manuales:", len(M.seccion_manuales([{"ramo": RAMO}])), "lineas")

# 8. los otros ramos siguen funcionando con el campo nuevo
for r_ in ("Macroeconomía II",):
    try:
        t = M.leer_temario(r_)
        it = M.leer_items(r_, B.leer_indice(), t) if M.leer_items.__code__.co_argcount == 3 else None
        print("    ", r_, "ok" if it is not None else "firma distinta")
    except SystemExit as ex:
        print("    ", r_, "sin temario:", ex)

real_ok = sha(REAL / "Microeconomía II" / "Motor" / "Resueltas" / f"{RID}.json") == "6396563E00A958F5EA1E842B3396551225A76898"
ok("banco real sin tocar", real_ok and not (REAL / "Microeconomía II" / "Motor" / "Correcciones").exists())
print("copia en", tmp)
