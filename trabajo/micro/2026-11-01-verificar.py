# Compara campeon.json con el respaldo y revisa la resolucion vigente del Control 1.
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path.home() / ".claude/skills/banco-evaluaciones/scripts"))
import banco as B
import motor as M

AQUI = Path(__file__).parent
SC = Path.home() / ".claude/skills/banco-evaluaciones/scripts"
RESP = next((AQUI / "respaldo-motor-2026-11-01").rglob("campeon.json"))
a, b = json.loads(RESP.read_text(encoding="utf-8")), json.loads((SC / "campeon.json").read_text(encoding="utf-8"))


def corto(x, n=900):
    t = json.dumps(x, ensure_ascii=False)
    return t if len(t) <= n else t[:n] + " ..."


print("claves:", list(b))
print("campeon antes/ahora:", a.get("campeon"), "/", b.get("campeon"))
for k in b:
    if a.get(k) != b.get(k):
        print(f"\n--- {k}\nantes: {corto(a.get(k))}\nahora: {corto(b.get(k))}")

print("\nversiones:", sorted(f.name for f in (SC / "versiones").glob("*.json")))
for v in ("v1.0", "v1.1", "v1.2"):
    f = SC / "versiones" / f"{v}.json"
    if f.exists():
        print(v, corto(json.loads(f.read_text(encoding="utf-8")), 500))

RAMO, ID = "Microeconomía II", "microeconomia-ii/2026-2-control-1-mundaca"
ind = B.leer_indice()
r = next(x for x in M.resoluciones(RAMO) if x["evaluacion_id"] == ID)
print("\nvigente:", {k: round(v, 3) for k, v in r["metricas"].items()}, "· modelo del registro:", r["version_modelo"])
print("bases:", {k: (round(v["brier"], 3), round(v["cuad"], 3)) for k, v in r["bases"].items()})
print("original:", {k: round(v, 3) for k, v in r["original"]["metricas"].items()})
print("deriva:", r["deriva"], "· real:", r["real"], "· dominio:", r["dominio"])
f = M.dir_motor(RAMO) / "Resueltas" / f"{r['id_registro']}.json"
print("sha Resueltas:", hashlib.sha1(f.read_bytes()).hexdigest().upper())
d = M.leer(M.dir_motor(RAMO) / "dominio.json")
print("dominio:", {u: d[u] for u in ("U1", "U2")}, d.get("_fuentes"))
print("correcciones:", [x.name for x in (M.dir_motor(RAMO) / "Correcciones").glob("*")])
