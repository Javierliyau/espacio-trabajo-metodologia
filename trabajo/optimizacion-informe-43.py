"""Optimización estocástica del alcance del informe Tema 43 (borrador desechable).

Mochila estocástica: elegir piezas que maximicen la nota esperada con
P(nota < 6,0) acotada, bajo un presupuesto de horas con desborde aleatorio
(falacia de planificación). Luego, robustez: se perturban todos los supuestos
±30 % y se cuenta cuántas veces cada pieza sigue en el óptimo.

TODOS los parámetros son juicios del asistente, no mediciones.
"""
import itertools
import numpy as np

PIEZAS = [  # (nombre, horas, aporte a la nota si sale bien, prob. de éxito propia)
    ("Contabilidad K-L-PTF (4.1)",        10, 0.35, 0.90),
    ("Erizo + H1 por conteo (4.2)",       14, 0.45, 0.95),  # además requiere datos
    ("Sensibilidad fiscal H3 (5.1)",       8, 0.35, 0.85),
    ("Escenarios simples (5.2)",           6, 0.20, 0.95),
    ("H2 descomposición K-L-PTF",         12, 0.30, 0.90),  # requiere erizo + plan A
    ("H1 con regresión",                   4, 0.08, 0.90),  # requiere erizo
    ("Robustez alfa (Anexo D)",            3, 0.05, 0.95),  # requiere K-L-PTF
    ("Anexo puente tesis",                 8, 0.03, 0.90),
    ("Alineación temprana (pauta+Alex)",   4, 0.00, 1.00),  # baja P(desalineación)
    ("Escritura semanal",                  2, 0.00, 1.00),  # baja el desborde
    ("Discusión rival rigurosa (6)",       6, 0.20, 0.90),
    ("Limitaciones (7)",                 1.5, 0.10, 1.00),
]
DEPENDE = {4: [1], 5: [1], 6: [0]}
BASE_NOTA, BASE_HORAS = 5.2, 40          # informe descriptivo bien escrito
P_DATOS, P_PLAN_A = 0.85, 0.40           # pendiente #19
P_DESALINEA = (0.25, 0.07)               # sin / con alineación temprana
CASTIGO_DESALINEA = 0.5
DESBORDE = ((1.30, 0.35), (1.15, 0.20))  # (media, sigma) sin / con escritura semanal
CASTIGO_APURO = 2.0                      # puntos de nota por 100 % de exceso de horas
N, S = len(PIEZAS), 4000


def subconjuntos():
    for bits in itertools.product([0, 1], repeat=N):
        if all(not bits[i] or all(bits[j] for j in deps) for i, deps in DEPENDE.items()):
            yield bits


X = np.array(list(subconjuntos()), dtype=float)          # K × N


def simular(h, g, p, presupuesto, rng):
    datos = rng.random(S) < P_DATOS
    plan_a = rng.random(S) < P_PLAN_A
    exito = rng.random((S, N)) < p
    exito[:, 1] &= datos
    exito[:, 4] &= exito[:, 1] & plan_a
    exito[:, 5] &= exito[:, 1]
    exito[:, 6] &= exito[:, 0]
    aporte = (exito * g) @ X.T                              # S × K

    zc, zi, zb = rng.standard_normal((S, 1)), rng.standard_normal((S, N)), rng.standard_normal(S)
    horas = {}
    for k, (media, sig) in enumerate(DESBORDE):
        mu = np.log(media) - sig**2 / 2
        m = np.exp(mu + sig * (0.7 * zc + 0.71 * zi))
        hh = m * h
        hh[:, 4] *= plan_a          # opción real: H2 solo se trabaja si las actas traen el desglose
        mb = np.exp(mu + sig * (0.7 * zc[:, 0] + 0.71 * zb))
        horas[k] = (hh @ X.T) + (BASE_HORAS * mb)[:, None]
    T = np.where(X[:, 9][None, :] == 1, horas[1], horas[0])
    apuro = CASTIGO_APURO * np.clip((T - presupuesto) / presupuesto, 0, None)

    u = rng.random(S)[:, None]
    desalinea = np.where(X[:, 8][None, :] == 1, u < P_DESALINEA[1], u < P_DESALINEA[0])
    nota = np.clip(BASE_NOTA + aporte - CASTIGO_DESALINEA * desalinea - apuro, 1, 7)
    return nota.mean(0), (nota < 6.0).mean(0)


def optimo(E, R, tope=0.10):
    ok = R <= tope
    return int(np.argmax(np.where(ok, E, -np.inf))) if ok.any() else int(np.argmin(R))


h0 = np.array([x[1] for x in PIEZAS], float)
g0 = np.array([x[2] for x in PIEZAS], float)
p0 = np.array([x[3] for x in PIEZAS], float)
rng = np.random.default_rng(43)

print("== Óptimo con los supuestos centrales (máx. nota esperada con P(<6,0) ≤ 10 %) ==")
for B in (60, 90, 120):
    E, R = simular(h0, g0, p0, B, rng)
    k = optimo(E, R)
    elegidas = [PIEZAS[i][0] for i in range(N) if X[k, i]]
    todo = len(X) - 1
    print(f"\nPresupuesto {B} h -> nota esperada {E[k]:.2f} · P(<6,0) {R[k]:.1%}")
    print(f"   (hacer TODO: {E[todo]:.2f} · P(<6,0) {R[todo]:.1%})")
    for e in elegidas:
        print("   +", e)

print("\n== Robustez: 150 mundos con supuestos perturbados ±30 %, presupuesto 90 h ==")
cuenta = np.zeros(N)
for _ in range(150):
    f = lambda v: v * rng.uniform(0.7, 1.3, N)
    E, R = simular(f(h0), f(g0), np.clip(f(p0), 0, 0.99), 90, rng)
    cuenta += X[optimo(E, R)]
for i in np.argsort(-cuenta):
    print(f"   {cuenta[i]/150:5.0%}  {PIEZAS[i][0]}")
