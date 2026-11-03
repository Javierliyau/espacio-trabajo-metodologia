"""Probabilidad de cada pregunta del Control 2 de Macro II (JV 5.1, 5.2.1, 5.2.2).

Modelo de juicio, no calibrado (solo existe un control de Droller en el ramo):
- Cada pregunta candidata tiene rasgos MEDIDOS (lineas del texto, ecuaciones/figuras,
  laminas de Droller, lineas de clase que la mencionan) y rasgos CODIFICADOS a mano
  (parecido al Control 1 por tipo de lugar, senal explicita del libro).
- Se sortean los pesos (incertidumbre del modelo) y el formato; se llenan los lugares
  sin repetir pregunta. Un desarrollo puede encadenar incisos, y una cuota asegura
  (con probabilidad alta, no siempre) una pregunta de 5.2 porque el temario la nombra.
Semilla fija: los numeros son reproducibles.
"""
import re
import numpy as np

SEED = 7
N_BETA, N_EXAM = 2000, 300
TXT = "C:/Espacio de trabajo Metodologia de estudio/trabajo/jv5-traduccion.txt"
CLASES = "C:/Proyecto Metodologia de estudio/datos/clases/"
FILES = ["2026-10-16-macroeconomia-ii-clase-6.md", "2026-10-19-macroeconomia-ii-clase-7.md",
         "2026-10-21-macroeconomia-ii-clase-8.md"]

lines = open(TXT, encoding="latin-1").read().split("\n")
clase = "\n".join(open(CLASES + f, encoding="utf-8", errors="replace").read() for f in FILES).lower()


def nonblank(ranges):
    return sum(1 for a, b in ranges for l in lines[a - 1:b] if l.strip())


# id, enunciado, rangos de lineas, ec/fig, laminas, regex de clase,
# iso (parecido al Control 1 segun el lugar D/A/C), libro (0-1), afinidad D/A/C
Q = [
 ("g_A", "Derivar g_A = λn/(1−φ) desde (5.4) y comentar", [(242, 274)], 4, 2, r"tasa de crecimiento de largo plazo|\\frac\{\\lambda\}\{1-\\phi\}", (1, .3, .3), 1.0, (1.0, .2, .1)),
 ("sR", "Alza permanente de s_R: Fig. 5.1-5.3, tasa y nivel", [(422, 503), (525, 531)], 4, 4, r"efecto (temporal|permanente|nivel|tasa)|(sube|aumenta|aumento de|alza de) \$?s_r", (.6, .3, 1), 1.0, (.9, .3, .9)),
 ("politica", "«Un subsidio a la I+D sube el crecimiento de largo plazo» (y s_K)", [(382, 420)], 1, 2, r"subsidi|pol.tica", (0, .3, 1), 1.0, (.1, .3, 1.0)),
 ("romer", "Romer original φ=1 y por qué los datos lo rechazan", [(344, 375), (402, 404)], 1, 2, r"\\phi ?= ?1|romer original|acelera", (.2, .3, .5), 1.0, (.3, .7, 1.0)),
 ("spill", "«φ<1 implica que no hay spillovers»", [(377, 380)], 0, 1, r"spillover|derrame", (0, 0, .3), 1.0, (0, .1, 1.0)),
 ("param", "Interpretar φ y λ (hombros, pesca agotada, pisarse los pies)", [(145, 177)], 2, 2, r"fishing|hombros|congesti|duplicaci|pisar|agot", (0, .7, .3), 1.0, (.2, 1.0, .5)),
 ("ext", "Investigador individual vs. agregado: externalidades", [(179, 201)], 1, 1, r"externalidad|congesti", (0, .4, .2), .5, (.1, 1.0, .5)),
 ("cien", "Investigadores constantes: 100 ideas y g_A→0", [(276, 313)], 1, 1, r"constante|cien |100", (.2, .3, .5), 1.0, (.1, .6, 1.0)),
 ("pob", "Población: n en Solow vs. Romer, y si deja de crecer", [(315, 342)], 0, 2, r"poblaci", (.2, .2, 1), 1.0, (.1, .5, 1.0)),
 ("rend", "Rendimientos: CRS en K y L_Y, crecientes con A (no rivalidad, Jobs y Wozniak)", [(97, 108)], 1, 4, r"no rival|rendimientos crecientes|jobs", (0, .3, .2), 1.0, (.1, 1.0, .7)),
 ("ystar", "y*(t), (5.10)-(5.11): s_R dos veces y efecto escala", [(507, 523), (533, 560)], 2, 3, r"efecto escala|1 ?- ?s_r", (.3, .2, .5), 1.0, (.5, .6, .9)),
 ("sect", "Tres sectores: qué hace cada uno y por qué", [(582, 591)], 0, 2, r"tres sectores|sector de", (0, .5, 0), .5, (.2, 1.0, .3)),
 ("cpo", "Bienes finales: problema y CPO (5.12)-(5.13)", [(593, 669)], 2, 2, r"primer orden|cpo|bienes finales", (.5, .1, 0), .5, (1.0, .3, .1)),
 ("mono", "Monopolista: p = r/α, markup", [(671, 716)], 1, 3, r"monopol|markup|patente", (.5, .1, .3), .5, (1.0, .3, .5)),
 ("pix", "Beneficio (5.14) y x = K/A (5.15)", [(718, 740)], 2, 2, r"beneficio|k/a", (.5, 0, 0), .5, (.9, .2, .2)),
 ("rec", "Recuperar (5.16) = (5.1) con simetría", [(742, 754)], 1, 1, r"sim.tric|k/a", (.5, 0, 0), .5, (.8, .2, .2)),
 ("scb", "¿Qué es la SCB en Romer? g_y = g_k = g_A", [(228, 240), (290, 292)], 0, 1, r"senda|sendero|balancead", (.3, 1, 0), .5, (.4, 1.0, .2)),
 ("endo", "Qué agrega Romer a Solow: A endógeno, lucro (Smith)", [(20, 43), (127, 143)], 1, 2, r"end.gen|lucro", (0, .5, .2), 1.0, (.1, 1.0, .4)),
 ("front", "El modelo describe la frontera: no se contrasta entre países", [(74, 80), (323, 334)], 0, 1, r"frontera|pa.ses avanzados|desarrollad", (0, .2, .3), 1.0, (0, .6, .8)),
 ("schump", "Romer (variedades) vs. Schumpeter (calidad)", [(45, 64)], 0, 0, r"schumpeter|aghion", (0, .3, .1), .5, (0, .8, .4)),
 ("pasos", "Análisis en dos pasos y analogía s_R con s_K", [(429, 439), (482, 484)], 0, 1, r"an.log|tasa de ahorro", (0, .3, .4), .5, (0, .6, .7)),
 ("detalle", "Detalles de 5.2.1: integral, nº de firmas, precio normalizado", [(616, 639)], 0, 1, r"integral|normaliz", (0, 0, .2), 0, (0, .4, .6)),
 ("dist", "Distribución del ingreso rK = α²Y (5.2.4, fuera de la lectura)", [], 0, 3, r"distribuci.n del ingreso|\\alpha\^2", (0, 0, 0), 0, (.2, .2, .4)),
]
LINK = {"g_A": ["sR"], "sR": ["g_A"], "ystar": ["sR"], "cpo": ["mono"], "mono": ["pix"], "pix": ["rec"], "rec": ["pix"]}
Q52 = ["sect", "cpo", "mono", "pix", "rec", "detalle"]
ids = [q[0] for q in Q]
J = len(Q)

L = np.array([nonblank(q[2]) for q in Q], float)
E = np.array([q[3] for q in Q], float)
S = np.array([q[4] for q in Q], float)
C = np.array([sum(1 for l in clase.split("\n") if re.search(q[5], l)) for q in Q], float)
ISO = np.array([q[6] for q in Q], float)
B = np.array([q[7] for q in Q], float)
AF = np.array([q[8] for q in Q], float)  # D, A, C
I52 = np.array([i in Q52 for i in ids])


def z(x):
    return (x - x.mean()) / x.std()


X = np.column_stack([z(np.log1p(L)), z(E), z(S), z(np.log1p(C)), B])
# control de lectura: pesan mas los rasgos del texto; laminas y clase pesan menos
MU = np.array([.50, .40, .25, .20, .60])
SD = np.array([.25, .25, .20, .20, .30])
MU_I, SD_I = 1.5, .5
# formatos: (prob, lugares D, A, C)
FORMATOS = [(.55, 1, 1, 3), (.30, 0, 2, 3), (.15, 2, 0, 2)]

rng = np.random.default_rng(SEED)


def un_control(logw, bi, u, rho, rng, p_link):
    """Devuelve preguntas elegidas (con incisos encadenados), lugares 'otro' y total."""
    f = rng.choice(len(FORMATOS), p=[x[0] for x in FORMATOS])
    _, nd, na, nc = FORMATOS[f]
    lugares = [0] * nd + [1] * na + [2] * nc
    cuota = rng.integers(len(lugares)) if rng.random() < rho else -1
    usados, otros = [], 0
    for k, t in enumerate(lugares):
        if k != cuota and rng.random() < u:  # pregunta que nadie anticipo
            otros += 1
            continue
        with np.errstate(divide="ignore"):
            s = logw + bi * ISO[:, t] + np.log(AF[:, t]) + rng.gumbel(size=J)
        s[usados] = -np.inf
        if k == cuota:
            s[~I52] = -np.inf
        i = int(np.argmax(s))
        usados.append(i)
        if t == 0 and ids[i] in LINK and rng.random() < p_link:
            for x in LINK[ids[i]]:
                ix = ids.index(x)
                if ix not in usados:
                    usados.append(ix)
    return usados, otros, len(lugares)


P = np.zeros((N_BETA, J))
slots_tot, slots_otro = 0, 0
for b in range(N_BETA):
    beta = np.maximum(rng.normal(MU, SD), 0)
    logw = X @ beta
    bi, u, rho = max(rng.normal(MU_I, SD_I), 0), rng.beta(2, 8), rng.beta(7, 3)
    for _ in range(N_EXAM):
        usados, otros, tot = un_control(logw, bi, u, rho, rng, .6)
        P[b, usados] += 1
        slots_tot += tot
        slots_otro += otros
P /= N_EXAM
media, lo, hi = P.mean(0), np.quantile(P, .1, axis=0), np.quantile(P, .9, axis=0)
orden = np.argsort(-media)

print(f"Semilla {SEED}; {N_BETA}x{N_EXAM} controles. Lugares no anticipados: {slots_otro/slots_tot:.1%}")
print(f"{'#':>2} {'id':8} {'P':>4} {'p10':>4} {'p90':>4} | {'lin':>3} {'ec':>2} {'lam':>3} {'cla':>4}  pregunta")
for k, i in enumerate(orden, 1):
    print(f"{k:2} {ids[i]:8} {media[i]:4.0%} {lo[i]:4.0%} {hi[i]:4.0%} | {L[i]:3.0f} {E[i]:2.0f} {S[i]:3.0f} {C[i]:4.0f}  {Q[i][1]}")

GR = {"Tasa vs. nivel (sR, politica, pasos, ystar)": ["sR", "politica", "pasos", "ystar"],
      "Ecuación de g_A y qué la mueve (g_A, cien, pob)": ["g_A", "cien", "pob"],
      "φ y λ, y Romer original (param, ext, romer, spill)": ["param", "ext", "romer", "spill"],
      "Microfundamentos 5.2 (sect, cpo, mono, pix, rec, detalle)": Q52,
      "Marco (rend, scb, endo, front, schump)": ["rend", "scb", "endo", "front", "schump"]}
print("\nProbabilidad de que aparezca al menos una pregunta del grupo: estimada aparte")
for g, m in GR.items():
    print(f"  {g}: suma de P = {sum(media[ids.index(x)] for x in m):.2f}")

ESC = {"sin parecido al Control 1": dict(mi=0.0),
       "laminas y clase pesan como el texto": dict(mu=np.array([.5, .4, .5, .4, .6])),
       "sin cuota de 5.2": dict(sinq=True),
       "desarrollo sin incisos": dict(pl=0.0)}
for nombre, e in ESC.items():
    r = np.random.default_rng(SEED)
    Pm = np.zeros(J)
    for b in range(400):
        logw = X @ np.maximum(r.normal(e.get("mu", MU), SD), 0)
        bi = 0.0 if "mi" in e else max(r.normal(MU_I, SD_I), 0)
        rho = 0 if e.get("sinq") else r.beta(7, 3)
        u = r.beta(2, 8)
        for _ in range(100):
            usados, _o, _t = un_control(logw, bi, u, rho, r, e.get("pl", .6))
            Pm[usados] += 1
    Pm /= 40000
    o = np.argsort(-Pm)[:7]
    print(f"\nSensibilidad [{nombre}]: " + ", ".join(f"{ids[i]} {Pm[i]:.0%}" for i in o))
