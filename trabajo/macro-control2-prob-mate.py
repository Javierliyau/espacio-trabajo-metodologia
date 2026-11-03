"""Control 2 de Macro II si es «matemático» (aviso del 1-11). Modelo de juicio, sin calibrar.

Rasgos medidos en macro-control2-prob.py (lineas, ec/fig, laminas, clase). Nuevo: esta en la
Ayudantia 4 (30-10), que es la unica guia de Droller sobre esta materia.
Lugares = ejercicios matematicos; cada uno puede encadenar incisos, como la ayudantia.
"""
import numpy as np

SEED = 7
N_BETA, N_EXAM = 2000, 300
# id, lineas, ec/fig, laminas, clase, ayudantia, numerico (0/1), enunciado
Q = [
 ("g_A", 21, 4, 2, 8, 1, 0, "Derivar g_A = λn/(1−φ), de (5.4) a (5.7)"),
 ("sR", 63, 4, 4, 5, 0, 0, "Alza de s_R con (5.9): salto, transición y nuevo nivel de A"),
 ("ystar", 32, 2, 3, 23, 0, 0, "Llegar a y*(t) (5.11) desde (5.10) y A = θ s_R L/g_A"),
 ("cpo", 54, 2, 2, 6, 1, 0, "CPO de bienes finales: w (5.12) y p_j (5.13)"),
 ("mono", 30, 1, 3, 10, 1, 0, "Monopolista: CPO, p = r/α y cantidad x"),
 ("xK", 6, 1, 2, 3, 1, 0, "K = ∫x_j dj ⇒ x = K/A (5.15)"),
 ("pi", 12, 1, 2, 3, 0, 0, "Beneficio π = α(1−α)Y/A (5.14)"),
 ("rec", 8, 1, 1, 2, 0, 0, "Recuperar Y = K^α(AL_Y)^(1−α) (5.16)"),
 ("romer", 27, 1, 2, 6, 0, 0, "Romer φ = 1: (5.8), tasa creciente con L_A"),
 ("cien", 31, 1, 1, 20, 0, 0, "L_A constante: Ȧ/A = 100/A → 0"),
 ("sRopt", 6, 1, 1, 2, 0, 0, "s_R que maximiza y*: ½ (ej. 2, derivando (5.11))"),
 ("num51", 10, 1, 1, 2, 0, 1, "Numérico de 5.1: g_A, A en la SCB y salto de s_R"),
 ("num52", 10, 1, 1, 2, 0, 1, "Numérico de 5.2: x, Y, w, p, r, π con datos"),
]
ids = [q[0] for q in Q]
J = len(Q)
L, E, S, C, AY, NUM = (np.array([q[k] for q in Q], float) for k in range(1, 7))
LINK = {"g_A": ["sR"], "sR": ["ystar"], "cpo": ["mono"], "mono": ["xK", "pi"], "xK": ["rec"], "pi": ["rec"], "ystar": ["sRopt"]}


def z(x):
    return (x - x.mean()) / x.std()


X = np.column_stack([z(np.log1p(L)), z(E), z(S), z(np.log1p(C))])
MU = np.array([.35, .4, .25, .2])
SD = np.array([.2, .25, .2, .2])
# numero de ejercicios matematicos: 1 largo, 2, o 3 cortos
FORMATOS = [(.3, 1), (.5, 2), (.2, 3)]


def simula(mu_ay=1.0, p_num=.25, p_link=.6, seed=SEED, nb=N_BETA, ne=N_EXAM):
    rng = np.random.default_rng(seed)
    P = np.zeros((nb, J))
    otros = tot = 0
    bloque = np.zeros(2)
    I51 = np.array([i in ("g_A", "sR", "ystar", "romer", "cien", "sRopt", "num51") for i in ids])
    for b in range(nb):
        logw = X @ np.maximum(rng.normal(MU, SD), 0) + max(rng.normal(mu_ay, .4), 0) * AY if mu_ay else X @ np.maximum(rng.normal(MU, SD), 0)
        u = rng.beta(2, 10)
        numerico = rng.random() < p_num
        for _ in range(ne):
            n = FORMATOS[rng.choice(3, p=[f[0] for f in FORMATOS])][1]
            usados = []
            for _k in range(n):
                tot += 1
                if rng.random() < u:
                    otros += 1
                    continue
                s = logw + (2.5 * NUM if numerico else -9 * NUM) + rng.gumbel(size=J)
                s[usados] = -np.inf
                i = int(np.argmax(s))
                usados.append(i)
                cola = [ids[i]]
                while cola:  # incisos encadenados
                    for x in LINK.get(cola.pop(), []):
                        ix = ids.index(x)
                        if ix not in usados and rng.random() < p_link:
                            usados.append(ix)
                            cola.append(x)
            P[b, usados] += 1
            bloque += [any(I51[usados]), any(~I51[usados] & ~NUM[usados].astype(bool))]
    return P / ne, otros / tot, bloque / (nb * ne)


P, o, bl = simula()
m, lo, hi = P.mean(0), np.quantile(P, .1, 0), np.quantile(P, .9, 0)
print(f"Lugares no anticipados: {o:.0%}. Al menos algo de 5.1: {bl[0]:.0%}; al menos algo de 5.2: {bl[1]:.0%}")
for k, i in enumerate(np.argsort(-m), 1):
    print(f"{k:2} {ids[i]:6} {m[i]:4.0%} {lo[i]:4.0%} {hi[i]:4.0%}  {Q[i][7]}")
for nombre, kw in (("sin la señal de la ayudantía", dict(mu_ay=0)), ("sin incisos encadenados", dict(p_link=0)),
                   ("mitad numérico", dict(p_num=.5)), ("nunca numérico", dict(p_num=0))):
    Pm, _, b2 = simula(nb=400, ne=100, **kw)
    mm = Pm.mean(0)
    print(f"\n[{nombre}] 5.1 {b2[0]:.0%}, 5.2 {b2[1]:.0%}: " + ", ".join(f"{ids[i]} {mm[i]:.0%}" for i in np.argsort(-mm)[:7]))
