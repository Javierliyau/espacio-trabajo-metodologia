"""Motor de prediccion de evaluaciones: subcomandos `predecir` y `motor` de banco.py.

Diseno aprobado: C:/Proyecto Metodologia de estudio/datos/motor-predicciones/fase2-diseno.md
- P(unidad): Dirichlet-multinomial jerarquico (programa -> ramo -> mismo profesor) sobre la fraccion de puntos.
- Senales del caso (clase, lo que dijo el profesor, bibliografia, cercania) como factores log-lineales acotados.
- Monte Carlo con plantillas reales de prueba; tres escenarios de parametros (no se estiman: n es chico).
- Prioridad = E[pts] x (1 - dominio); piso de cobertura en el plan, no en la probabilidad.
Todo es determinista con semilla fija y en Python puro (sin numpy).
"""
import hashlib
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

import banco as B

TIPOS_P = ("comente", "analisis", "matematico")
BLOOM = ("B1", "B2", "B3")
BLOOM_TXT = {"B1": "recordar-comprender", "B2": "aplicar", "B3": "analizar-evaluar-crear"}
# hiperparametros versionados (la Fase 5 los recalibra creando versiones nuevas, no editando el codigo):
# versiones/vX.Y.json no se editan nunca; campeon.json dice cual rige
VERSIONES = Path(__file__).with_name("versiones")
CAMPEON_FILE = Path(__file__).with_name("campeon.json")


def cargar_version(v):
    f = VERSIONES / f"v{v}.json"
    if not f.exists():
        sys.exit(f"No existe la version {v} ({f}).")
    return json.loads(f.read_text(encoding="utf-8"))


def estado_campeon():
    return json.loads(CAMPEON_FILE.read_text(encoding="utf-8")) if CAMPEON_FILE.exists() else \
        {"campeon": "1.0", "historial": [], "retadores": [], "platt": None, "ultimo_ciclo": None}


def efectivos(P, ramo=None):
    """Parametros de la version con los ajustes propios del ramo (por_ramo), si los hay."""
    extra = (P.get("por_ramo") or {}).get(ramo) or {}
    return dict(P, **extra) if extra else P


def usar_param(P, ramo=None):
    """Fija los hiperparametros que lee todo el modelo. Devuelve los anteriores (para restaurarlos)."""
    global PARAM, ESCENARIOS, BETA, VIDA_MEDIA, PESO_EXTERNO, REMUESTREOS_ETIQUETA, DIAS_CERCANIA
    previo = globals().get("PARAM")
    P = efectivos(P, ramo)
    PARAM, ESCENARIOS, BETA = P, P["escenarios"], P["beta"]
    VIDA_MEDIA, PESO_EXTERNO = P["vida_media_semestres"], P["peso_otra_universidad"]
    REMUESTREOS_ETIQUETA = P["remuestreos_etiqueta"]   # versiones de pi con los items ambiguos sorteados
    DIAS_CERCANIA = P["dias_cercania"]
    return previo


usar_param(cargar_version(estado_campeon()["campeon"]))
CORRIDAS = PARAM["corridas"]
EQUIV_TIPO = {"verdadero falso": "comente", "desarrollo": "analisis", "calculo": "matematico", "grafico": "analisis"}
ORDEN_TIPO = {"Control": 0, "Quiz": 0, "Tarea": 0, "Taller": 0, "PEP": 1, "Certamen": 1, "Prueba": 1,
              "Solemne": 1, "Examen": 2}


# ---------------------------------------------------------------- archivos

def dir_motor(ramo):
    return B.BANCO / B.limpio(ramo) / "Motor"


def leer(f, defecto=None):
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else defecto


def escribir(f, data):
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def resolver_ramo(nombre):
    ind = B.leer_indice()
    opciones = set(B.ramos_conocidos(ind)) | {p.parent.parent.name for p in B.BANCO.glob("*/Motor/temario.json")}
    r = B.parecido(nombre, opciones, 0.5)
    if not r:
        sys.exit(f"Ramo desconocido: {nombre}. Opciones: {', '.join(sorted(opciones))}")
    return r, ind


def leer_temario(ramo):
    f = dir_motor(ramo) / "temario.json"
    t = leer(f)
    if not t:
        sys.exit(f"Falta {f}. Crealo desde el programa del ramo (formato en SKILL.md, seccion Motor).")
    t["orden"] = [u["id"] for u in t["unidades"]]
    t["por_id"] = {u["id"]: u for u in t["unidades"]}
    return t


def fecha_de(s):
    return datetime.strptime(s, "%Y-%m-%d").date() if s else None


def periodo_de(f):
    return (f.year, 1 if f.month <= 7 else 2)


def semestres_entre(a, b):
    return (b[0] - a[0]) * 2 + (b[1] - a[1])


# ---------------------------------------------------------------- capa de items (seccion 0 del diseno)

def num_puntos(s):
    m = re.search(r"\d+(?:[.,]\d+)?", str(s or ""))
    return float(m.group().replace(",", ".")) if m else None


def tipo_item(p):
    n = B.normal(p.get("n"))
    for pref, t in (("coment", "comente"), ("anali", "analisis"), ("matem", "matematico"), ("desarr", "analisis")):
        if n.startswith(pref):
            return t
    return EQUIV_TIPO.get(B.normal(p.get("tipo_pregunta")), "analisis")


def unidades_item(temas, temario):
    """{unidad: fraccion} por conteo de temas especificos; los transversales (null) no deciden la unidad."""
    mapa = {B.normal(k): v for k, v in temario["temas"].items()}
    c, sin = Counter(), []
    for t in temas or []:
        k = B.normal(t)
        if k not in mapa:
            sin.append(t)
        elif mapa[k]:
            c[mapa[k]] += 1
    if not c:
        c[temario["transversal_por_defecto"]] = 1
    tot = sum(c.values())
    return {u: n / tot for u, n in c.items()}, sin


def orden_supuesto(ev):
    """Sin fecha: Control k -> k, PEP 1 -> 2.5, PEP 2 -> 5.5, Examen al final. Editable en items.json."""
    num = ev.get("numero")
    try:
        num = float(num)
    except (TypeError, ValueError):
        num = 1.0
    t = ORDEN_TIPO.get(B.normalizar_tipo(ev.get("tipo")), 1)
    return {0: num, 1: 3 * num - 0.5, 2: 99.0}[t]


def construir_items(ramo, ind, temario):
    """Lee las fichas del ramo y arma items.json. Conserva lo editado a mano (alcance, orden, fecha, bloom_claude)."""
    f = dir_motor(ramo) / "items.json"
    viejo = leer(f, {"evaluaciones": {}})["evaluaciones"]
    evs, sin_mapa = {}, set()
    for i, m in ind["evaluaciones"].items():
        if m["ramo"] != ramo:
            continue
        ev = B.leer_eval(m)
        ant = viejo.get(i, {})
        ant_items = {it["n"]: it for it in ant.get("items", [])}
        items = []
        for p in ev["preguntas"]:
            us, sin = unidades_item(p.get("temas"), temario)
            sin_mapa |= set(sin)
            a = ant_items.get(str(p.get("n")), {})
            items.append({
                "n": str(p.get("n")), "puntos": num_puntos(p.get("puntaje")), "tipo": tipo_item(p),
                "temas": p.get("temas") or [], "unidades": us, "ambiguo": len(us) > 1,
                "enunciado": re.sub(r"\s+", " ", str(p.get("enunciado") or ""))[:240],
                "bloom_gemini": a.get("bloom_gemini"), "bloom_claude": a.get("bloom_claude")})
        pts = [it["puntos"] for it in items if it["puntos"]]
        for it in items:  # puntaje faltante: promedio de los demas (o 1 si no hay ninguno)
            it["imputado"] = it["puntos"] is None
            if it["imputado"]:
                it["puntos"] = sum(pts) / len(pts) if pts else 1.0
            it["bloom"] = it["bloom_claude"] or it["bloom_gemini"]
        presentes = [u for u in temario["orden"] if any(u in it["unidades"] for it in items)]
        if presentes:
            a0, a1 = temario["orden"].index(presentes[0]), temario["orden"].index(presentes[-1])
            alcance = temario["orden"][a0:a1 + 1]
        else:
            alcance = []
        evs[i] = {
            "profesor": ev.get("profesor"), "tipo": B.normalizar_tipo(ev.get("tipo")), "numero": ev.get("numero"),
            "anio": ev.get("anio"), "semestre": ev.get("semestre"),
            "universidad": ev.get("universidad"),
            "origen": "pauta" if m.get("pauta") == "oficial" else "reconstruido",
            "fecha": ant.get("fecha") or ev.get("fecha"),
            "orden": ant.get("orden", orden_supuesto(ev)), "orden_supuesto": ant.get("orden_supuesto", True),
            "alcance": ant["alcance"] if ant.get("alcance_manual") else alcance,
            "alcance_manual": ant.get("alcance_manual", False),
            "items": items}
    data = {"ramo": ramo, "generado": f"{datetime.now():%Y-%m-%d %H:%M}",
            "nota": ("Editable: fecha, orden (orden_supuesto=false al corregir), alcance (alcance_manual=true), "
                     "bloom_claude. Se conserva al regenerar."),
            "evaluaciones": evs}
    escribir(f, data)
    return data, sorted(sin_mapa)


def leer_items(ramo, ind, temario):
    f = dir_motor(ramo) / "items.json"
    if not f.exists():
        return construir_items(ramo, ind, temario)[0]
    data = leer(f)
    ids = {i for i, m in ind["evaluaciones"].items() if m["ramo"] == ramo}
    if ids != set(data["evaluaciones"]):  # llegaron o se borraron evaluaciones
        data = construir_items(ramo, ind, temario)[0]
    return data


def clave_orden(ev):
    return (ev.get("anio") or 0, ev.get("semestre") or 0, ev.get("fecha") or "", ev.get("orden") or 0)


def kappa(pares):
    """Kappa de Cohen entre dos codificaciones (lista de pares)."""
    pares = [(a, b) for a, b in pares if a and b]
    if not pares:
        return None, 0
    n = len(pares)
    po = sum(a == b for a, b in pares) / n
    ca, cb = Counter(a for a, _ in pares), Counter(b for _, b in pares)
    pe = sum(ca[k] * cb[k] for k in BLOOM) / n ** 2
    return (1.0 if pe == 1 else (po - pe) / (1 - pe)), n


# ---------------------------------------------------------------- Gemini (volumen, fuera del contexto de Claude)

PROMPT_TEMAS = """Asigna cada tema de evaluaciones de {ramo} a UNA unidad del programa, o null si es transversal
(aparece en varias unidades y por si solo no indica la unidad, p. ej. "bienestar social").
Unidades:
{unidades}
Temas: {temas}
Devuelve SOLO JSON: {{"<tema>": "U1" | null, ...}}"""

PROMPT_BLOOM = """Clasifica cada pregunta de {ramo} en un nivel de la taxonomia de Bloom revisada (Anderson y
Krathwohl 2001), colapsada en 3 niveles:
- B1 recordar-comprender: definir, explicar, interpretar, inferir sin calcular ni aplicar un modelo nuevo.
- B2 aplicar: usar un procedimiento o modelo conocido en un caso (calcular un equilibrio, resolver un juego).
- B3 analizar-evaluar-crear: descomponer, comparar escenarios, juzgar una afirmacion con argumentos
  (un "comente" verdadero/falso que exige evaluar la afirmacion es B3), disenar.
Clasifica por lo que la pregunta EXIGE hacer, no por el tema.
Preguntas (id | tipo | enunciado):
{items}
Devuelve SOLO JSON: {{"<id>": "B1" | "B2" | "B3", ...}}"""

PROMPT_CLASE = """Analiza esta transcripcion de una clase de {ramo} (fecha {fecha}). Unidades del programa:
{unidades}
Devuelve SOLO JSON con:
- "tiempo": fraccion aproximada del tiempo de clase dedicada a cada unidad, {{"U1": 0.7, ...}} (suma <= 1;
  lo administrativo o fuera del programa no se asigna).
- "claves": conteo por unidad de claves organizativas o de enfasis del profesor: "esto entra", "lo importante",
  "ojo con esto", "esto es pregunta de prueba", "anoten", repeticiones deliberadas. {{"U1": 3, ...}}
- "dichos": lista de frases del profesor sobre evaluaciones: [{{"texto": "<cita breve literal>",
  "unidades": ["U1"], "tipo": "entra" | "no_entra" | "enfasis", "evaluacion": "<control, PEP 1, etc. o null>"}}]
Transcripcion:
{texto}"""

PROMPT_PISTAS = """Este archivo junta pistas de prueba anotadas por un alumno en clases de {ramo}. Unidades:
{unidades}
Por cada pista, indica la fecha de la clase y la unidad. Devuelve SOLO JSON:
[{{"fecha": "AAAA-MM-DD", "unidad": "U1", "texto": "<pista breve>"}}]
Archivo:
{texto}"""


def lista_unidades(temario):
    return "\n".join(f"- {u['id']} {u['nombre']}: {u['objetivo']}" for u in temario["unidades"])


def cmd_motor(args):
    if args.accion in ("evaluar", "ciclo", "semanal", "tablero", "rollback"):
        return cmd_motor_fase5(args)
    if not args.ramo:
        sys.exit("Falta --ramo.")
    ramo, ind = resolver_ramo(args.ramo)
    temario = leer_temario(ramo)
    if args.accion == "preparar":
        preparar(ramo, ind, temario, args)
    elif args.accion == "senales":
        calcular_senales(ramo, temario, args)
    elif args.accion == "backtest":
        cmd_backtest(ramo, ind, temario, args)


def preparar(ramo, ind, temario, args):
    data, sin_mapa = construir_items(ramo, ind, temario)
    if sin_mapa:
        print(f"Temas sin unidad ({len(sin_mapa)}): los mapea Gemini y quedan en temas_por_revisar...")
        r = B.gemini([{"text": PROMPT_TEMAS.format(ramo=ramo, unidades=lista_unidades(temario),
                                                    temas=json.dumps(sin_mapa, ensure_ascii=False))}],
                     modelo=args.modelo, tipo="motor")
        f = dir_motor(ramo) / "temario.json"
        crudo = leer(f)
        for t in sin_mapa:
            u = r.get(t)
            crudo["temas"][t] = u if u in temario["por_id"] else None
            crudo.setdefault("temas_por_revisar", []).append(t)
        escribir(f, crudo)
        temario = leer_temario(ramo)
        data, _ = construir_items(ramo, ind, temario)
    faltan = [(i, it) for i, ev in data["evaluaciones"].items() for it in ev["items"] if not it["bloom_gemini"]]
    if faltan:
        print(f"Rotulando Bloom de {len(faltan)} preguntas con Gemini...")
        txt = "\n".join(f"{i}#{it['n']} | {it['tipo']} | {it['enunciado']}" for i, it in faltan)
        r = B.gemini([{"text": PROMPT_BLOOM.format(ramo=ramo, items=txt)}], modelo=args.modelo, tipo="motor")
        for i, it in faltan:
            b = r.get(f"{i}#{it['n']}")
            it["bloom_gemini"] = b if b in BLOOM else None
            it["bloom"] = it["bloom_claude"] or it["bloom_gemini"]
        escribir(dir_motor(ramo) / "items.json", data)
    todos = [it for ev in data["evaluaciones"].values() for it in ev["items"]]
    k, n = kappa([(it["bloom_gemini"], it["bloom_claude"]) for it in todos])
    print(f"ok {dir_motor(ramo) / 'items.json'}: {len(data['evaluaciones'])} evaluaciones, {len(todos)} preguntas, "
          f"{sum(it['ambiguo'] for it in todos)} ambiguas (varias unidades), "
          f"{sum(it['imputado'] for it in todos)} con puntaje imputado.")
    print(f"Bloom: Gemini {sum(bool(it['bloom_gemini']) for it in todos)}/{len(todos)}, "
          f"Claude {sum(bool(it['bloom_claude']) for it in todos)}/{len(todos)}"
          + (f", kappa = {k:.2f} sobre {n}" if k is not None else " (falta la segunda codificacion ciega)"))
    if temario.get("temas_por_revisar"):
        print(f"Revisar en temario.json: {', '.join(temario['temas_por_revisar'])}")


def fecha_archivo(f, anio):
    m = re.search(r"(\d{1,2})-(\d{1,2})(?:-(\d{2,4}))?", f.stem)
    if not m:
        return None
    a = int(m.group(3)) if m.group(3) else anio
    a = a + 2000 if a < 100 else a
    try:
        return date(a, int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None


def calcular_senales(ramo, temario, args):
    """Una peticion a Gemini por transcripcion nueva (y una por PISTAS_CLASES.md); queda en cache por hash."""
    f = dir_motor(ramo) / "senales.json"
    cache = leer(f, {"clases": {}, "pistas": None})
    carpeta = B.NOTAS_VOZ / ramo / "Transcripciones"
    archivos = sorted(carpeta.glob("*.txt")) + sorted(carpeta.glob("*.md")) if carpeta.exists() else []
    for a in archivos:
        h = B.sha1(a)
        if cache["clases"].get(a.name, {}).get("hash") == h:
            continue
        fe = fecha_archivo(a, datetime.fromtimestamp(a.stat().st_mtime).year)
        print(f"Clase {a.name} ({fe or 'sin fecha'}) -> Gemini...")
        r = B.gemini([{"text": PROMPT_CLASE.format(ramo=ramo, fecha=fe or "?", unidades=lista_unidades(temario),
                                                    texto=a.read_text(encoding="utf-8", errors="replace"))}],
                     modelo=args.modelo, tipo="motor")
        cache["clases"][a.name] = {"hash": h, "fecha": fe.isoformat() if fe else None,
                                   "tiempo": r.get("tiempo") or {}, "claves": r.get("claves") or {},
                                   "dichos": r.get("dichos") or []}
        escribir(f, cache)
    pistas = B.BANCO / B.limpio(ramo) / "PISTAS_CLASES.md"
    if pistas.exists() and (cache.get("pistas") or {}).get("hash") != B.sha1(pistas):
        print("PISTAS_CLASES.md -> Gemini...")
        r = B.gemini([{"text": PROMPT_PISTAS.format(ramo=ramo, unidades=lista_unidades(temario),
                                                     texto=pistas.read_text(encoding="utf-8"))}],
                     modelo=args.modelo, tipo="motor")
        cache["pistas"] = {"hash": B.sha1(pistas), "lista": r if isinstance(r, list) else []}
        escribir(f, cache)
    print(f"ok {f}: {len(cache['clases'])} clases, {len((cache.get('pistas') or {}).get('lista', []))} pistas")


def senales_hasta(ramo, fecha, S):
    """Agrega las senales de clase anteriores (o iguales) a la fecha de la prueba."""
    cache = leer(dir_motor(ramo) / "senales.json", {"clases": {}, "pistas": None})
    tiempo, claves, ultima, dichos, n = defaultdict(float), Counter(), {}, [], 0
    for nombre, c in cache["clases"].items():
        fc = fecha_de(c.get("fecha"))
        if fc and fc > fecha:
            continue
        n += 1
        for u, v in c["tiempo"].items():
            tiempo[u] += float(v or 0)
            if fc and float(v or 0) >= 0.15:
                ultima[u] = max(ultima.get(u, fc), fc)
        for u, v in c["claves"].items():
            claves[u] += int(v or 0)
        dichos += [dict(d, fecha=c.get("fecha")) for d in c["dichos"]]
    for p in (cache.get("pistas") or {}).get("lista", []):
        fp = fecha_de(p.get("fecha"))
        if p.get("unidad") and (not fp or fp <= fecha):
            claves[p["unidad"]] += 1
    fechas = [fecha_de(c.get("fecha")) for c in cache["clases"].values() if c.get("fecha")]
    fechas = [f for f in fechas if f <= fecha]
    return {"n_clases": n, "ultima_clase": max(fechas) if fechas else None, "tiempo": dict(tiempo), "claves": dict(claves), "ultima": ultima, "dichos": dichos}


# ---------------------------------------------------------------- modelo (seccion 2)

def prior_programa(temario, S):
    w = {u: float(temario["por_id"][u].get("peso") or 1) for u in S}
    t = sum(w.values())
    return {u: w[u] / t for u in S}


def puntos_por_unidad(ev, rng=None):
    """Puntos por unidad; con rng, cada item ambiguo se asigna entero a una unidad sorteada por sus fracciones."""
    pts = defaultdict(float)
    for it in ev["items"]:
        if rng and it["ambiguo"]:
            us = list(it["unidades"])
            pts[rng.choices(us, [it["unidades"][u] for u in us])[0]] += it["puntos"]
        else:
            for u, fr in it["unidades"].items():
                pts[u] += it["puntos"] * fr
    return pts


def peso_eval(ev, objetivo, variante, n_medio):
    p = clave_periodo(ev)
    w = 0.5 ** (max(0, semestres_entre(p, objetivo)) / VIDA_MEDIA) if p else 1.0
    if variante == "pregunta":
        w *= len(ev["items"]) / n_medio
    elif variante == "sin_imputados" and any(it["imputado"] for it in ev["items"]):
        w = 0.0
    return w


def clave_periodo(ev):
    return (ev["anio"], ev["semestre"]) if ev.get("anio") and ev.get("semestre") else None


def actualizar(prior, evs, c, S, pi0, objetivo, variante, rng=None, externo=None):
    """Un nivel del modelo jerarquico. Cada prueba aporta un vector g que redistribuye, dentro de S∩alcance,
    la masa que el prior le da a esa interseccion; fuera de ella deja el prior intacto. Peso = decaimiento x
    masa de pi0 en la interseccion (0 si la interseccion tiene una sola unidad: no informa proporciones)."""
    num = {u: c * prior[u] for u in S}
    den = c
    n_medio = (sum(len(e["items"]) for e in evs) / len(evs)) if evs else 1
    usadas = 0.0
    for ev in evs:
        inter = [u for u in S if u in ev["alcance"]]
        pts = puntos_por_unidad(ev, rng)
        tot = sum(pts[u] for u in inter)
        if len(inter) < 2 or tot <= 0:
            continue
        w = peso_eval(ev, objetivo, variante, n_medio) * sum(pi0[u] for u in inter)
        if externo and externo(ev):
            w *= PESO_EXTERNO
        if w <= 0:
            continue
        masa = sum(prior[u] for u in inter)
        for u in S:
            num[u] += w * (pts[u] / tot * masa if u in inter else prior[u])
        den += w
        usadas += w
    return {u: num[u] / den for u in S}, usadas


def acot(x):
    return max(1 / 3, min(3.0, x))


def factores(S, pi0, sen, temario, fecha, entra, fb):
    """{unidad: {senal: multiplicador}} acotados a [1/3, 3]."""
    m = {u: {} for u in S}
    # clase: solo compara unidades ya pasadas entre si. Una unidad aun no pasada no es evidencia en contra
    # (las transcripciones llegan hasta hoy, no hasta la prueba; si no entra, eso lo decide el alcance).
    vistas = [u for u in S if sen["tiempo"].get(u, 0) > 0]
    tot, base = sum(sen["tiempo"][u] for u in vistas), sum(pi0[u] for u in vistas)
    for u in vistas:
        s = math.log((sen["tiempo"][u] / tot) / (pi0[u] / base))
        s = max(-1.5, min(1.5, s)) + 0.25 * min(sen["claves"].get(u, 0), 4)
        m[u]["clase"] = acot(math.exp(BETA["clase"] * fb * s))
    for u in entra:
        if u in m:
            m[u]["dijo"] = acot(math.exp(BETA["dijo"] * fb))
    bib = {u: temario["por_id"][u].get("biblio") for u in S}
    if any(v is True for v in bib.values()) and not all(v is True for v in bib.values()):
        for u in S:
            if bib[u] is True:
                m[u]["biblio"] = acot(math.exp(BETA["biblio"] * fb))
    for u in S:
        ult = sen["ultima"].get(u)
        if ult and 0 <= (fecha - ult).days <= DIAS_CERCANIA:
            m[u]["cercania"] = acot(math.exp(BETA["cercania"] * fb))
    return m


def aplicar_factores(pi, m, S):
    x = {u: pi[u] * math.prod(m[u].values()) for u in S}
    t = sum(x.values())
    return {u: x[u] / t for u in S}


def posterior(ctx, esc, rng=None, variante="prueba"):
    """Devuelve (pi_final, cadena de pasos para el porque, kappa)."""
    S, pi0 = ctx["S"], ctx["pi0"]
    pi1, w1 = actualizar(pi0, ctx["evs_ramo"], esc["c0"], S, pi0, ctx["objetivo"], variante, rng, ctx["externo"])
    pasos = [("programa", pi0), ("ramo", pi1)]
    if ctx["profesor"]:
        pi2, w2 = actualizar(pi1, ctx["evs_prof"], esc["c1"], S, pi0, ctx["objetivo"], variante, rng)
        kap = esc["c1"] + w2
        pasos.append((ctx["profesor"], pi2))
    else:
        pi2, kap = pi1, esc["c0"] + w1
    m = factores(S, pi0, ctx["sen"], ctx["temario"], ctx["fecha"], ctx["entra"], esc["fb"])
    pi = pi2
    if ctx.get("q_pos"):  # v1.1: alcance incierto -> prior de alcance por posicion (no es una senal: sin cota)
        pi = aplicar_factores(pi, {u: {"posicion": ctx["q_pos"][u]} for u in S}, S)
        pasos.append(("posicion", pi))
    for senal in ("clase", "dijo", "biblio", "cercania"):
        if any(senal in m[u] for u in S):
            pi = aplicar_factores(pi, {u: {senal: m[u].get(senal, 1.0)} for u in S}, S)
            pasos.append((senal, pi))
    return pi, pasos, kap


# ---------------------------------------------------------------- Monte Carlo (seccion 4)

def plantillas(ctx):
    """Plantillas reales: [(fraccion de puntos, n unidades, tipo)] por prueba, del profesor y del tipo de
    evaluacion pedidos; si no hay, se relaja (ramo, cualquier tipo). En frio: 4 preguntas iguales."""
    def de(evs, mismo_tipo):
        out = []
        for ev in evs:
            if mismo_tipo and ORDEN_TIPO.get(ev["tipo"], 1) != ctx["clase_eval"]:
                continue
            tot = sum(it["puntos"] for it in ev["items"]) or 1
            out.append([(it["puntos"] / tot, min(2, len(it["unidades"])), it["tipo"]) for it in ev["items"]])
        return out
    for evs, mismo in ((ctx["evs_prof"], True), (ctx["evs_ramo"], True), (ctx["evs_prof"], False),
                       (ctx["evs_ramo"], False)):
        p = de(evs, mismo)
        if p:
            return p
    return [[(0.25, 1, "analisis")] * 4]


def muestra_sin_reemplazo(S, pesos, k, rng):
    us, ws, out = list(S), [w + 1e-12 for w in pesos], []  # la gamma puede dar 0 exacto con forma chica
    for _ in range(k):
        u = rng.choices(range(len(us)), ws)[0]
        out.append(us.pop(u))
        ws.pop(u)
    return out


def simular(pis, kap, plants, S, rng, n):
    entra, pts = Counter(), {u: [] for u in S}
    for _ in range(n):
        pi = rng.choice(pis)
        g = [rng.gammavariate(max(kap * pi[u], 1e-3), 1) for u in S]
        s = sum(g) or 1
        th = [x / s for x in g]
        got = defaultdict(float)
        for frac, k, _t in rng.choice(plants):
            us = muestra_sin_reemplazo(S, th, min(k, len(S)), rng)
            for u in us:
                got[u] += frac / len(us)
        for u in S:
            pts[u].append(got[u] * 100)
            entra[u] += got[u] > 0
    res = {}
    for u in S:
        v = sorted(pts[u])
        pos = [x for x in v if x > 0]
        res[u] = {"p": entra[u] / n, "e": sum(v) / n, "e_cond": sum(pos) / len(pos) if pos else 0.0,
                  "q10": v[int(0.10 * (n - 1))], "q90": v[int(0.90 * (n - 1))]}
    return res


# ---------------------------------------------------------------- tipo y Bloom (seccion 1)

def dist_tipo(ctx, esc):
    def cuenta(evs):
        c = Counter()
        for ev in evs:
            tot = sum(it["puntos"] for it in ev["items"]) or 1
            for it in ev["items"]:
                c[it["tipo"]] += it["puntos"] / tot
        return c, len(evs)
    base = {t: 1 / 3 for t in TIPOS_P}
    cr, nr = cuenta(ctx["evs_ramo"])
    p1 = {t: (esc["c0"] * base[t] + cr[t]) / (esc["c0"] + nr) for t in TIPOS_P}
    if not ctx["profesor"]:
        return p1
    cp, npf = cuenta(ctx["evs_prof"])
    return {t: (esc["c1"] * p1[t] + cp[t]) / (esc["c1"] + npf) for t in TIPOS_P}


def dist_bloom(ctx, u, tipo):
    ub = ctx["temario"]["por_id"][u].get("bloom") or "B2"
    prior = {b: 0.6 if b == ub else 0.2 for b in BLOOM}
    evs = ctx["evs_prof"] or ctx["evs_ramo"]
    c = Counter(it["bloom"] for ev in evs for it in ev["items"] if it["tipo"] == tipo and it.get("bloom"))
    n = sum(c.values())
    return {b: (2 * prior[b] + c[b]) / (2 + n) for b in BLOOM}


# ---------------------------------------------------------------- dominio y plan (seccion 5)

def dominio(ramo, S):
    """Media de una Beta por unidad: prior de la autoevaluacion (1-5 -> 0,1-0,9, peso 2) + logrado/posible."""
    d = leer(dir_motor(ramo) / "dominio.json", {})
    out, hay = {}, False
    for u in S:
        x = d.get(u) or {}
        if not x:
            out[u] = 0.0
            continue
        hay = True
        m0 = 0.1 + 0.2 * (float(x.get("auto", 2)) - 1)
        lo, po = float(x.get("logrado", 0)), float(x.get("posible", 0))
        out[u] = min(0.9, (2 * m0 + lo) / (2 + po))
    return out, hay


# ---------------------------------------------------------------- predecir

def contexto(ramo, ind, temario, items, fecha, profesor, evaluacion, alcance=None, entra=(), no_entra=(),
             antes_de=None, ids=None, incierto=False):
    """Arma todo lo que el modelo necesita. antes_de=(clave_orden) limita las pruebas usadas (backtest); ids las
    fija una por una (repetir un pre-registro); incierto=True marca que el alcance no se conoce (modo programa)."""
    objetivo = periodo_de(fecha)
    sen = None
    evs = []
    for i, ev in items["evaluaciones"].items():
        if ids is not None:
            if i not in ids:
                continue
        elif antes_de is not None:
            if clave_orden(ev) >= antes_de:
                continue
        else:
            # con fecha: solo si es anterior a la prueba; sin fecha: solo si es de un periodo anterior
            # (una prueba de este mismo semestre sin fecha no se usa: anota su fecha en items.json)
            p, fe = clave_periodo(ev), fecha_de(ev.get("fecha"))
            if not ((fe and fe < fecha) or (not fe and p and p < objetivo)):
                continue
        evs.append(dict(ev, id=i))
    prof = B.parecido(profesor, {e["profesor"] for e in items["evaluaciones"].values() if e.get("profesor")}, 0.6) \
        if profesor else None
    prof_nombre = prof or (profesor.title() if profesor else None)
    evs_prof = [e for e in evs if prof and e["profesor"] == prof]
    evs_ramo = [e for e in evs if not (prof and e["profesor"] == prof)]
    # alcance (seccion 2): flag > calendario (desde) > clases vistas hasta la fecha > todo el programa
    origen_S = "indicado"
    if alcance:
        S = [u for u in temario["orden"] if u in alcance]
    else:
        desde = {u["id"]: fecha_de(u.get("desde")) for u in temario["unidades"]}
        sen = senales_hasta(ramo, fecha, temario["orden"])
        if any(desde.values()):
            S = [u for u in temario["orden"] if desde[u] and desde[u] <= fecha]
            origen_S = "calendario"
        elif sen["n_clases"] and sen["ultima_clase"] and (fecha - sen["ultima_clase"]).days <= DIAS_CERCANIA:
            # las clases definen el alcance solo si llegan cerca de la prueba; si faltan semanas de materia
            # por pasar, lo visto hasta hoy subestima el alcance
            tot = sum(sen["tiempo"].values()) or 1
            S = [u for u in temario["orden"] if sen["tiempo"].get(u, 0) / tot >= 0.05]
            origen_S = "provisional: clases vistas hasta la fecha"
        else:
            S = [u["id"] for u in temario["unidades"] if not u.get("opcional")]
            origen_S = "provisional: todo el programa sin opcionales (sin calendario ni clases cerca de la fecha)"
    S = [u for u in temario["orden"] if (u in S or u in entra) and u not in no_entra]
    if not S:
        sys.exit("El alcance quedo vacio: revisa --alcance / --no-entra.")
    sen = sen or senales_hasta(ramo, fecha, S)
    pi0 = prior_programa(temario, S)
    clase_eval = ORDEN_TIPO.get(B.normalizar_tipo(evaluacion.split()[0]) if evaluacion else "PEP", 1)
    uni = B.normal(temario.get("universidad") or "Universidad de Santiago de Chile")
    incierto = incierto or origen_S.startswith("provisional: todo el programa")
    q_pos = alcance_posicion(evs, S, evaluacion) \
        if incierto and evaluacion and (PARAM.get("alcance_posicion") or {}).get("activo") else None
    return {"ramo": ramo, "temario": temario, "fecha": fecha, "objetivo": objetivo, "S": S, "origen_S": origen_S,
            "pi0": pi0, "evs_ramo": evs_ramo, "evs_prof": evs_prof, "profesor": prof_nombre,
            "prof_en_banco": bool(prof), "sen": sen, "entra": list(entra), "clase_eval": clase_eval,
            "incierto": incierto, "q_pos": q_pos,
            "externo": lambda ev: bool(ev.get("universidad")) and B.normal(ev["universidad"]) != uni}


def alcance_posicion(evs, S, evaluacion):
    """v1.1: P(u en el alcance | tipo y numero de la prueba), con las pruebas pasadas del mismo tipo y numero,
    encogida (pseudoconteo a) hacia la cobertura media de las pruebas de su clase. Sin pruebas iguales: None."""
    partes = evaluacion.split()
    tipo, num = B.normalizar_tipo(partes[0]), " ".join(partes[1:])
    iguales = [e for e in evs if num and e["tipo"] == tipo and str(e.get("numero") or "") == num and e["alcance"]]
    if not iguales:
        return None
    clase = ORDEN_TIPO.get(tipo, 1)
    misma = [e for e in evs if ORDEN_TIPO.get(e["tipo"], 1) == clase and e["alcance"]]
    base = sum(len(set(e["alcance"]) & set(S)) / len(S) for e in misma) / len(misma)
    a = PARAM["alcance_posicion"]["a"]
    return {u: (sum(u in e["alcance"] for e in iguales) + a * base) / (len(iguales) + a) for u in S}


def predecir(ctx, semilla=7, corridas=CORRIDAS):
    """Corre los tres escenarios. Devuelve resultados por escenario y lo necesario para el informe."""
    out = {}
    plants = plantillas(ctx)
    for nombre, esc in ESCENARIOS.items():
        rng = random.Random(f"{semilla}-{nombre}")
        pi, pasos, kap = posterior(ctx, esc)
        hay_amb = any(it["ambiguo"] for e in ctx["evs_ramo"] + ctx["evs_prof"] for it in e["items"])
        pis = [posterior(ctx, esc, rng)[0] for _ in range(REMUESTREOS_ETIQUETA)] if hay_amb else [pi]
        out[nombre] = {"pi": pi, "pasos": pasos, "kappa": kap,
                       "sim": simular(pis, kap, plants, ctx["S"], rng, corridas)}
    pl = platt_vigente()
    if pl:  # recalibracion de P(entra) del campeon (Fase 5; solo existe con >= PLATT_DESDE pronosticos resueltos)
        for r in out.values():
            for u in ctx["S"]:
                r["sim"][u]["p"] = recal(r["sim"][u]["p"], pl)
    return out


def banda(p):
    return "alta" if p >= 0.7 else "media" if p >= 0.4 else "baja"


def r5(x):
    return int(5 * round(x * 100 / 5))


def fuerza(ctx):
    if not ctx["evs_ramo"] and not ctx["evs_prof"]:
        return "débil: sin historia"
    if not ctx["evs_prof"]:
        return "débil: sin pruebas de este profesor" if ctx["profesor"] else "media: solo historia del ramo"
    if len(ctx["evs_prof"]) < 3:
        return "media: menos de 3 pruebas del profesor"
    if all(e["origen"] == "reconstruido" for e in ctx["evs_prof"]):
        return "media: las pruebas del profesor son enunciados reconstruidos, sin pauta"
    return "fuerte"


def porque(pasos, u):
    nombres = {"programa": "programa", "ramo": "+ramo", "posicion": "×alcance por posición", "clase": "×clase", "dijo": "×dijo el profe",
               "biblio": "×bibliografía", "cercania": "×cercanía"}
    trozos = []
    for i, (n, pi) in enumerate(pasos):
        etiqueta = nombres.get(n, f"+{n}")
        trozos.append(f"{etiqueta} {pi[u] * 100:.0f} %")
    return " → ".join(trozos)


def informe(ctx, res, evaluacion, provisional, args):
    S, tem = ctx["S"], ctx["temario"]
    c = res["central"]
    frio = not ctx["evs_ramo"] and not ctx["evs_prof"]
    dom, hay_dom = dominio(ctx["ramo"], S)
    prio = {u: c["sim"][u]["e"] * (1 - dom[u]) for u in S}
    tp = dist_tipo(ctx, ESCENARIOS["central"])
    orden = sorted(S, key=lambda u: -prio[u])
    rango = {u: (min(r["sim"][u]["q10"] for r in res.values()), max(r["sim"][u]["q90"] for r in res.values()))
             for u in S}
    p_rng = {u: (min(r["sim"][u]["p"] for r in res.values()), max(r["sim"][u]["p"] for r in res.values()))
             for u in S}
    rank = {n: sorted(S, key=lambda u: -r["sim"][u]["e"]) for n, r in res.items()}
    sensible = {u for u in S if max(rk.index(u) for rk in rank.values()) - min(rk.index(u) for rk in rank.values()) >= 2}
    L = [f"---", f"generado: {datetime.now():%Y-%m-%d %H:%M}", f"ramo: {ctx['ramo']}", f"evaluacion: {evaluacion}",
         f"fecha: {ctx['fecha']}{' (provisional)' if provisional else ''}", f"profesor: {ctx['profesor'] or '-'}",
         f"semilla: {args.semilla}", "---",
         f"# Predicción · {evaluacion} · {ctx['ramo']}", "",
         f"- **Fecha:** {ctx['fecha']}{' — provisional: vuelve a correr `predecir` cuando se confirme' if provisional else ''}",
         f"- **Alcance ({ctx['origen_S']}):** " + ", ".join(f"{u} {tem['por_id'][u]['nombre']}" for u in S),
         f"- **Fuerza:** {fuerza(ctx)}",
         f"- **Datos usados:** {len(ctx['evs_prof'])} pruebas de {ctx['profesor'] or '(sin profesor)'}, "
         f"{len(ctx['evs_ramo'])} del ramo (otros profesores), {ctx['sen']['n_clases']} clases transcritas"
         + (f", dijo que entra: {', '.join(ctx['entra'])}" if ctx["entra"] else ""),
         "- El Monte Carlo solo propaga la incertidumbre del modelo supuesto; no agrega evidencia. "
         "Los porcentajes van redondeados al 5 % y los rangos juntan los tres escenarios (conservador, central, audaz).",
         ""]
    if len(S) == 1:
        L.insert(-1, f"- ⚠ El alcance tiene una sola unidad: la probabilidad es trivial. Si la prueba cubre más "
                     "(clases aún no transcritas o calendario), corre de nuevo con `--alcance` o `--entra`.")
    if ctx["profesor"] and not ctx["prof_en_banco"]:
        L.insert(-1, f"- ⚠ {ctx['profesor']} no tiene pruebas en el banco: el nivel «profesor» queda vacío.")
    L += ["## Por unidad (orden de prioridad de estudio)", ""]
    if frio:
        L += ["Ramo en frío: solo orden y banda, sin números (el diseño prohíbe intervalos heredados de otro ramo).", "",
              "| # | Unidad | Banda | Por qué |", "|---|---|---|---|"]
        for k, u in enumerate(orden, 1):
            L.append(f"| {k} | {u} {tem['por_id'][u]['nombre']} | {banda(c['sim'][u]['p'])} | {porque(c['pasos'], u)} |")
    else:
        L += ["| # | Unidad | P(entra) | Puntos esperados (% de la prueba) | Si entra | Rango 80 % | Dominio | Por qué |",
              "|---|---|---|---|---|---|---|---|"]
        for k, u in enumerate(orden, 1):
            s = c["sim"][u]
            pr = f"{r5(s['p'])} % ({banda(s['p'])}; {r5(p_rng[u][0])}-{r5(p_rng[u][1])})"
            flag = " ⚠ sensible al escenario" if u in sensible else ""
            L.append(f"| {k} | {u} {tem['por_id'][u]['nombre']}{flag} | {pr} | {s['e']:.0f} | {s['e_cond']:.0f} | "
                     f"{rango[u][0]:.0f}-{rango[u][1]:.0f} | {dom[u]:.1f} | {porque(c['pasos'], u)} |")
    L += ["", "## Tipo y nivel de Bloom más probables", "",
          "Tipo de pregunta (fracción de puntos): " + ", ".join(f"{t} {tp[t] * 100:.0f} %" for t in TIPOS_P), ""]
    for u in orden[:5]:
        combos = sorted(((tp[t] * pb, t, b) for t in TIPOS_P for b, pb in dist_bloom(ctx, u, t).items()), reverse=True)[:3]
        L.append(f"- **{u}:** " + "; ".join(f"{t} · {b} {BLOOM_TXT[b]} ({p * 100:.0f} %)" for p, t, b in combos))
    L += ["", "_Supuesto: tipo y Bloom independientes de la unidad salvo por el verbo del objetivo._", ""]
    # plan con piso de cobertura
    tot = sum(prio.values()) or 1
    piso = 0.5 / len(S)
    L += ["## Plan: reparto del tiempo de estudio (piso de cobertura)", "",
          f"Cada unidad recibe al menos {piso * 100:.0f} % del tiempo y una sesión de recuperación; el resto va "
          "según la prioridad = puntos esperados × (1 − dominio). Nada queda en cero: el motor ordena, no autoriza "
          "saltarse unidades.", ""]
    if not hay_dom:
        L += ["⚠ No hay `Motor/dominio.json`: dominio = 0 en todo; la prioridad es igual a los puntos esperados.", ""]
    for u in orden:
        L.append(f"- {u} {tem['por_id'][u]['nombre']}: {(piso + 0.5 * prio[u] / tot) * 100:.0f} % del tiempo")
    dias = (ctx["fecha"] - date.today()).days
    if dias > 0:
        L += ["", f"Faltan {dias} días: espaciar los repasos cada {max(1, round(0.2 * dias))}-{max(1, round(0.4 * dias))} "
              "días (20-40 % de la distancia), intercalando unidades y tipos, siempre con práctica de recuperación."]
    # reaparicion de items
    evs = ctx["evs_prof"] or ctx["evs_ramo"]
    L += ["", "## Preguntas pasadas para practicar (no entran a la probabilidad)", ""]
    for u in orden[:3]:
        its = [(e["id"], it) for e in evs for it in e["items"] if max(it["unidades"], key=it["unidades"].get) == u]
        for i, it in its[:3]:
            L.append(f"- {u} · `{i}` {it['n']} ({it['tipo']}): {it['enunciado'][:140]}")
    # dichos del profesor detectados en clase
    dichos = [d for d in ctx["sen"]["dichos"] if d.get("tipo") in ("entra", "no_entra")]
    if dichos:
        L += ["", "## Lo que el profesor dijo en clase sobre evaluaciones (revisar si aplica a esta)", ""]
        for d in dichos[:8]:
            L.append(f"- {d.get('fecha')}: «{d.get('texto')}» → {d.get('tipo')} {', '.join(d.get('unidades') or [])}"
                     f" ({d.get('evaluacion') or 'evaluación no especificada'}). Si aplica, usa --entra / --no-entra.")
    L += ["", "## Escenarios", "",
          "| Escenario | c₀ | c₁ | β × | Top 3 por puntos esperados |", "|---|---|---|---|---|"]
    for n, esc in ESCENARIOS.items():
        L.append(f"| {n} | {esc['c0']} | {esc['c1']} | {esc['fb']} | " + ", ".join(rank[n][:3]) + " |")
    L += ["", "_Los β de las señales de clase no están validados: no hay transcripciones de semestres pasados. "
          "Se evalúan prueba a prueba, en forma prospectiva._"]
    return "\n".join(L) + "\n"


def hash_datos(ramo):
    h = hashlib.sha1()
    for n in ("temario.json", "items.json", "senales.json", "dominio.json"):
        f = dir_motor(ramo) / n
        h.update(n.encode() + (f.read_bytes() if f.exists() else b"-"))
    return h.hexdigest()


def hash_temario(ramo):
    """Hash de la estructura del programa (unidades, pesos, objetivos); mapear un tema nuevo no lo cambia."""
    f = dir_motor(ramo) / "temario.json"
    if not f.exists():
        return None
    us = [(u["id"], u["nombre"], u.get("peso"), u.get("objetivo"), u.get("opcional")) for u in leer(f)["unidades"]]
    return hashlib.sha1(json.dumps(us, ensure_ascii=False).encode()).hexdigest()


def sen_json(sen):
    iso = lambda d: d.isoformat() if d else None
    return {"n_clases": sen["n_clases"], "ultima_clase": iso(sen["ultima_clase"]), "tiempo": sen["tiempo"],
            "claves": sen["claves"], "ultima": {u: iso(d) for u, d in sen["ultima"].items()}, "dichos": sen["dichos"]}


def sen_de_json(s):
    return dict(s, ultima_clase=fecha_de(s["ultima_clase"]), ultima={u: fecha_de(d) for u, d in s["ultima"].items()})


def registrar(ctx, res, args):
    """Pre-registro (Fase 5): cada corrida queda congelada en <Ramo>/Predicciones/<id>.json, solo lectura.
    Se guardan todas; la que se evalua es la ultima emitida antes de la fecha de la prueba."""
    ahora = datetime.now()
    partes = args.evaluacion.split()
    S, central = ctx["S"], ESCENARIOS["central"]
    m = factores(S, ctx["pi0"], ctx["sen"], ctx["temario"], ctx["fecha"], ctx["entra"], central["fb"])
    rid = f"{ahora:%Y%m%d-%H%M%S}-{B.slug(args.evaluacion)}"
    data = {
        "id": rid, "emitida": ahora.isoformat(timespec="seconds"), "ramo": ctx["ramo"],
        "evaluacion": args.evaluacion, "tipo": B.normalizar_tipo(partes[0]),
        "numero": " ".join(partes[1:]) or None, "periodo": list(ctx["objetivo"]),
        "fecha_prueba": ctx["fecha"].isoformat(), "fecha_provisional": bool(args.provisional),
        "profesor": ctx["profesor"], "version_modelo": PARAM["version"], "parametros": PARAM,
        "hash_datos": hash_datos(ctx["ramo"]), "semilla": args.semilla, "corridas": args.corridas or CORRIDAS,
        "alcance": S, "origen_alcance": ctx["origen_S"], "entra": ctx["entra"],
        "no_entra": [x.strip().upper() for x in (args.no_entra or "").split(",") if x.strip()],
        "pruebas_usadas": {"profesor": [e["id"] for e in ctx["evs_prof"]], "ramo": [e["id"] for e in ctx["evs_ramo"]]},
        "n_clases": ctx["sen"]["n_clases"], "fuerza": fuerza(ctx),
        "sen": sen_json(ctx["sen"]), "q_pos": ctx["q_pos"], "incierto": ctx["incierto"],
        "hash_temario": hash_temario(ctx["ramo"]), "platt": platt_vigente(),
        "por_escenario": {n: {u: {k: round(v, 4) for k, v in r["sim"][u].items()} for u in S} for n, r in res.items()},
        "pi_central": {u: round(res["central"]["pi"][u], 4) for u in S},
        "descomposicion_central": [[n, {u: round(pi[u], 4) for u in S}] for n, pi in res["central"]["pasos"]],
        "factores_central": {u: {k: round(v, 4) for k, v in m[u].items()} for u in S}}
    f = B.BANCO / B.limpio(ctx["ramo"]) / "Predicciones" / f"{rid}.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "x", encoding="utf-8") as fh:  # "x": nunca sobrescribe
        json.dump(data, fh, ensure_ascii=False, indent=1)
    f.chmod(0o444)
    return f


def cmd_predecir(args):
    ramo, ind = resolver_ramo(args.ramo)
    usar_param(PARAM, ramo)
    temario = leer_temario(ramo)
    items = leer_items(ramo, ind, temario) if any(m["ramo"] == ramo for m in ind["evaluaciones"].values()) \
        else {"evaluaciones": {}}
    lista = lambda s: [x.strip().upper() for x in s.split(",") if x.strip()] if s else []
    fecha = fecha_de(args.fecha)
    ctx = contexto(ramo, ind, temario, items, fecha, args.profesor, args.evaluacion,
                   lista(args.alcance), lista(args.entra), lista(args.no_entra))
    res = predecir(ctx, args.semilla, args.corridas or CORRIDAS)
    destino = B.BANCO / B.limpio(ramo) / f"PREDICCION - {B.limpio(args.evaluacion)}.md"
    destino.write_text(informe(ctx, res, args.evaluacion, args.provisional, args), encoding="utf-8")
    reg = registrar(ctx, res, args)
    c = res["central"]["sim"]
    print(f"ok {destino}")
    print(f"registro {reg.name} (modelo v{PARAM['version']})")
    print(f"Alcance ({ctx['origen_S']}): {', '.join(ctx['S'])} | fuerza: {fuerza(ctx)}")
    for u in sorted(ctx["S"], key=lambda u: -c[u]["e"]):
        print(f"  {u} P(entra) {r5(c[u]['p'])} %  E[pts] {c[u]['e']:.0f}  si entra {c[u]['e_cond']:.0f}")


# ---------------------------------------------------------------- backtest (Fase 4, seccion 6 del diseno)
# Reglas fijadas antes de correrlo (no se tocan despues de ver los resultados):
# - Cada prueba se predice solo con las anteriores (clave_orden) y sin ninguna senal de clase ni dicho.
# - Dos modos de alcance: "programa" (lo que haria el motor sin calendario ni clases: programa sin opcionales)
#   y "conocido" (el alcance real de la prueba; aisla el reparto de puntos; P(entra) no se evalua ahi porque el
#   alcance sale de los mismos items).
# - Especificacion principal: escenario central, variante "prueba". Las demas son sensibilidad.
# - Verdad: puntos por unidad de la prueba (items ambiguos repartidos por fraccion); entra = puntos > 0.

BT_VARIANTES = ("prueba", "pregunta", "sin_imputados")
BT_BASES = ("frecuente", "ultima_prueba", "uniforme", "programa")
BT_PRINC = "motor/central/prueba"
BT_BINS = 5          # calibracion en quintos: con ~55 pronosticos, los deciles quedan casi vacios
BT_BOOT = 2000
BT_N = (1, 2)        # cobertura top-N


def sen_vacia():
    return {"n_clases": 0, "ultima_clase": None, "tiempo": {}, "claves": {}, "ultima": {}, "dichos": []}


def verdad(ev):
    pts = puntos_por_unidad(ev)
    tot = sum(pts.values()) or 1
    return {u: v / tot for u, v in pts.items() if v > 0}


def base_frecuencia(evs, S):
    """'Lo mas frecuente' (sin programa): P(entra) = (veces que entro + 0,5) / (n + 1); reparto = media de las
    fracciones de puntos dentro de S, con una prueba uniforme de pseudoconteo. Sin pruebas: 0,5 y uniforme."""
    n = len(evs)
    if not n:
        return {u: 0.5 for u in S}, {u: 1 / len(S) for u in S}
    vs = [verdad(ev) for ev in evs]
    acc = defaultdict(float)
    for v in vs:
        t = sum(v.get(u, 0) for u in S)
        for u in S:
            acc[u] += v.get(u, 0) / t if t else 0
    p = {u: (sum(1 for v in vs if v.get(u, 0) > 0) + 0.5) / (n + 1) for u in S}
    sh = {u: (acc[u] + 1 / len(S)) / (n + 1) for u in S}
    t = sum(sh.values())
    return p, {u: sh[u] / t for u in S}


def bt_motor(ctx, esc, variante, rng, corridas):
    pi, _, kap = posterior(ctx, esc, variante=variante)
    hay_amb = any(it["ambiguo"] for e in ctx["evs_ramo"] + ctx["evs_prof"] for it in e["items"])
    pis = [posterior(ctx, esc, rng, variante)[0] for _ in range(REMUESTREOS_ETIQUETA)] if hay_amb else [pi]
    sim = simular(pis, kap, plantillas(ctx), ctx["S"], rng, corridas)
    return {u: sim[u]["p"] for u in ctx["S"]}, {u: sim[u]["e"] / 100 for u in ctx["S"]}


def bt_fijo(ctx, pi, rng, corridas):
    """Linea base con reparto fijo: P(entra) sale de las mismas plantillas, sin incertidumbre en theta."""
    sim = simular([pi], 1e6, plantillas(ctx), ctx["S"], rng, corridas)
    return {u: sim[u]["p"] for u in ctx["S"]}, dict(pi)


def entro(f, u):
    return 1 if f["real"].get(u, 0) > 0 else 0


def cuad(f):
    """Error cuadratico del reparto de puntos de una prueba (incluye los puntos reales fuera de S)."""
    return sum((f["sh"][u] - f["real"].get(u, 0)) ** 2 for u in f["S"]) + \
        sum(v ** 2 for u, v in f["real"].items() if u not in f["S"])


def brier_prueba(f):
    return sum((f["p"][u] - entro(f, u)) ** 2 for u in f["S"]) / len(f["S"])


def intervalos(fs):
    g = defaultdict(list)
    for p, y in fs:
        g[min(BT_BINS - 1, int(p * BT_BINS))].append((p, y))
    return g


def murphy(fs):
    """Brier = fiabilidad - resolucion + incertidumbre, por intervalos; el resto (varianza dentro de cada
    intervalo) se informa aparte para que la suma cierre."""
    n = len(fs)
    bs = sum((p - y) ** 2 for p, y in fs) / n
    obar = sum(y for _, y in fs) / n
    rel = res = 0.0
    for g in intervalos(fs).values():
        pm, om = sum(p for p, _ in g) / len(g), sum(y for _, y in g) / len(g)
        rel += len(g) * (pm - om) ** 2 / n
        res += len(g) * (om - obar) ** 2 / n
    unc = obar * (1 - obar)
    return {"brier": bs, "fiab": rel, "resol": res, "incert": unc, "resto": bs - (rel - res + unc), "n": n}


def calibracion(fs, rng):
    """Por intervalo: pronostico medio, frecuencia observada y barras de consistencia 5-95 % (Brocker y Smith
    2007): el rango que se veria si los pronosticos estuvieran calibrados."""
    out = []
    for k, g in sorted(intervalos(fs).items()):
        sims = sorted(sum(rng.random() < p for p, _ in g) / len(g) for _ in range(1000))
        out.append({"intervalo": f"{k / BT_BINS:.1f}-{(k + 1) / BT_BINS:.1f}", "n": len(g),
                    "pron": sum(p for p, _ in g) / len(g), "obs": sum(y for _, y in g) / len(g),
                    "lo": sims[50], "hi": sims[949]})
    return out


def cobertura(f, n):
    """Fraccion de los puntos reales en las n unidades con mas puntos esperados. Con empates en el corte, valor
    esperado de desempatar al azar (si no, el orden del temario favorece a U1)."""
    sh, real = f["sh"], f["real"]
    orden = sorted(f["S"], key=lambda u: -sh[u])
    if n >= len(orden):
        return sum(real.get(u, 0) for u in orden)
    corte = sh[orden[n - 1]]
    arriba = [u for u in orden if sh[u] > corte + 1e-9]
    empate = [u for u in orden if abs(sh[u] - corte) <= 1e-9]
    return sum(real.get(u, 0) for u in arriba) + \
        (n - len(arriba)) / len(empate) * sum(real.get(u, 0) for u in empate)


def metricas(filas):
    """filas: una por prueba, con S, real (reparto real), p (P(entra)) y sh (reparto predicho)."""
    fs, ll = [], []
    for f in filas:
        for u in f["S"]:
            y, q = entro(f, u), min(0.99, max(0.01, f["p"][u]))
            fs.append((f["p"][u], y))
            ll.append(-math.log(q if y else 1 - q))
    m = lambda xs: sum(xs) / len(xs) if xs else None
    cov = {n: [cobertura(f, n) for f in filas] for n in BT_N}
    return {"fs": fs, "brier": m([(p - y) ** 2 for p, y in fs]), "log": m(ll), "cuad": m([cuad(f) for f in filas]),
            **{f"top{n}": m(cov[n]) for n in BT_N}}


def boot_dif(a, b, rng):
    """IC 90 % de media(a) - media(b), pareado, remuestreando pruebas."""
    n = len(a)
    if n < 2:
        return None
    ds = []
    for _ in range(BT_BOOT):
        idx = [rng.randrange(n) for _ in range(n)]
        ds.append(sum(a[i] - b[i] for i in idx) / n)
    ds.sort()
    return ds[int(0.05 * BT_BOOT)], ds[int(0.95 * BT_BOOT) - 1]


def backtest(ramo, ind, temario, items, semilla, corridas):
    evs = sorted(items["evaluaciones"].items(), key=lambda x: clave_orden(x[1]))
    S_prog = [u["id"] for u in temario["unidades"] if not u.get("opcional")]
    modelos = [f"motor/{e}/{v}" for e in ESCENARIOS for v in BT_VARIANTES] + list(BT_BASES)
    filas = {modo: {m: [] for m in modelos} for modo in ("programa", "conocido")}
    meta = []
    for i, ev in evs:
        fecha = date(ev["anio"], 5 if ev["semestre"] == 1 else 10, 1)
        evaluacion = f"{ev['tipo']} {ev.get('numero') or ''}".strip()
        for modo in ("programa", "conocido"):
            S = S_prog if modo == "programa" else [u for u in temario["orden"] if u in ev["alcance"]]
            if len(S) < 2:
                continue
            ctx = contexto(ramo, ind, temario, items, fecha, ev["profesor"], evaluacion, alcance=S,
                           antes_de=clave_orden(ev))
            ctx["sen"] = sen_vacia()  # en el corte no existia ninguna senal de clase
            previas = sorted(ctx["evs_ramo"] + ctx["evs_prof"], key=clave_orden)
            if modo == "programa":
                meta.append({"id": i, "profesor": ev["profesor"], "periodo": f"{ev['anio']}-{ev['semestre']}",
                             "n_previas": len(previas), "n_prof": len(ctx["evs_prof"]), "alcance_real": ev["alcance"]})
            base = {"S": S, "real": verdad(ev), "id": i, "profesor": ev["profesor"]}
            for e, esc in ESCENARIOS.items():
                for v in BT_VARIANTES:
                    p, sh = bt_motor(ctx, esc, v, random.Random(f"{semilla}-{i}-{modo}-{e}-{v}"), corridas)
                    filas[modo][f"motor/{e}/{v}"].append(dict(base, p=p, sh=sh))
            p, sh = base_frecuencia(previas, S)
            filas[modo]["frecuente"].append(dict(base, p=p, sh=sh))
            # ultima prueba: la mas reciente; con empate de orden, la del mismo profesor
            ult = [e for e in previas if clave_orden(e) == clave_orden(previas[-1])] if previas else []
            ult = [e for e in ult if e["profesor"] == ev["profesor"]] or ult
            p, sh = base_frecuencia(ult[-1:], S)
            filas[modo]["ultima_prueba"].append(dict(base, p=p, sh=sh))
            rng = random.Random(f"{semilla}-{i}-{modo}-base")
            p, sh = bt_fijo(ctx, {u: 1 / len(S) for u in S}, rng, corridas)
            filas[modo]["uniforme"].append(dict(base, p=p, sh=sh))
            p, sh = bt_fijo(ctx, ctx["pi0"], rng, corridas)
            filas[modo]["programa"].append(dict(base, p=p, sh=sh))
    return filas, meta, modelos


def informe_backtest(ramo, filas, meta, modelos, semilla, corridas):
    rng = random.Random(f"{semilla}-informe")
    pct = lambda x: "—" if x is None else f"{100 * x:.0f} %"
    num = lambda x: "—" if x is None else f"{x:.3f}"
    ic = lambda x: f" [{x[0]:+.3f}, {x[1]:+.3f}]" if x else ""
    L = [f"# Backtest del motor — {ramo}", "",
         f"Generado {datetime.now():%Y-%m-%d %H:%M} · modelo v{PARAM['version']} · semilla {semilla} · "
         f"{corridas} corridas por pronóstico · {BT_BOOT} remuestreos", "",
         "Reglas fijadas antes de correr: cada prueba se predice solo con las anteriores y sin señales de clase. "
         f"La especificación principal es `{BT_PRINC}`; las demás son sensibilidad. "
         "Modo **programa**: alcance = programa sin opcionales (lo que haría el motor sin calendario ni clases); "
         "evalúa P(entra) y el reparto. Modo **conocido**: alcance = el real de la prueba; evalúa solo el reparto "
         "de puntos (P(entra) no, porque el alcance sale de los mismos ítems). "
         "La línea base «lo último visto en clase» **no es evaluable**: no hay clases de semestres pasados. "
         "En su lugar va «última prueba» (recencia), que no es lo mismo.", "",
         "Métricas: Brier y log-loss de P(entra) por unidad (menor es mejor); «cuad» = error cuadrático del "
         "reparto de puntos por prueba (menor es mejor); top-N = fracción de los puntos reales que caen en las N "
         "unidades con más puntos esperados (mayor es mejor).", "",
         "## Pruebas (en el orden del backtest)", "",
         "| Prueba | Profesor | Periodo | Previas (del profesor) | Alcance real |", "|---|---|---|---|---|"]
    for m in meta:
        L.append(f"| {m['id'].split('/')[-1]} | {m['profesor']} | {m['periodo']} | {m['n_previas']} ({m['n_prof']}) | "
                 f"{', '.join(m['alcance_real'])} |")
    resumen = {}
    for prof in sorted({m["profesor"] for m in meta}):
        L += ["", f"## {prof}", ""]
        if prof == "Mundaca":
            L += ["Enunciados reconstruidos y n = 4: esto es diagnóstico; la validación real de Mundaca es "
                  "prospectiva (pre-registros desde el Control 1 del 2026-2).", ""]
        for modo in ("programa", "conocido"):
            fl = {m: [f for f in filas[modo][m] if f["profesor"] == prof] for m in modelos}
            n = len(fl[BT_PRINC])
            if not n:
                L += [f"### Modo {modo}", "", "Sin pruebas con alcance de 2 o más unidades.", ""]
                continue
            ms = {m: metricas(fl[m]) for m in modelos}
            resumen[(prof, modo)] = ms
            L += [f"### Modo {modo} (n = {n} pruebas)", ""]
            if modo == "programa":
                L += ["| Modelo | Brier | Log-loss | Cuad | Top-1 | Top-2 |", "|---|---|---|---|---|---|"]
            else:
                L += ["| Modelo | Cuad | Top-1 | Top-2 |", "|---|---|---|---|"]
            for m in modelos:
                x, nombre = ms[m], (f"**{m}**" if m == BT_PRINC else m)
                cols = [num(x["brier"]), num(x["log"])] if modo == "programa" else []
                cols += [num(x["cuad"]), pct(x["top1"]), pct(x["top2"])]
                L.append(f"| {nombre} | " + " | ".join(cols) + " |")
            L += ["", f"Diferencia `{BT_PRINC}` − línea base (negativo = gana el motor; IC 90 % pareado, "
                  "remuestreando pruebas):", ""]
            for b in BT_BASES:
                partes = []
                if modo == "programa":
                    a, c = [brier_prueba(f) for f in fl[BT_PRINC]], [brier_prueba(f) for f in fl[b]]
                    partes.append(f"Brier {(sum(a) - sum(c)) / n:+.3f}{ic(boot_dif(a, c, rng))}")
                a, c = [cuad(f) for f in fl[BT_PRINC]], [cuad(f) for f in fl[b]]
                partes.append(f"cuad {(sum(a) - sum(c)) / n:+.3f}{ic(boot_dif(a, c, rng))}")
                L.append(f"- vs {b}: " + "; ".join(partes))
            if modo == "programa":
                mu = murphy(ms[BT_PRINC]["fs"])
                L += ["", f"Murphy (`{BT_PRINC}`, {BT_BINS} intervalos): Brier {mu['brier']:.3f} = fiabilidad "
                      f"{mu['fiab']:.3f} − resolución {mu['resol']:.3f} + incertidumbre {mu['incert']:.3f} "
                      f"(resto dentro de intervalos {mu['resto']:+.3f}; {mu['n']} pronósticos).", "",
                      "| Intervalo | n | Pronóstico medio | Observado | Consistencia 5-95 % |", "|---|---|---|---|---|"]
                for c in calibracion(ms[BT_PRINC]["fs"], rng):
                    fuera = "" if c["lo"] <= c["obs"] <= c["hi"] else " (fuera)"
                    L.append(f"| {c['intervalo']} | {c['n']} | {pct(c['pron'])} | {pct(c['obs'])}{fuera} | "
                             f"{pct(c['lo'])}-{pct(c['hi'])} |")
            L.append("")
    L += ["## Detalle por prueba (modo programa, especificación principal)", "",
          "| Prueba | Unidad | P(entra) motor | P frecuente | Reparto motor | Reparto real |", "|---|---|---|---|---|---|"]
    for f, g in zip(filas["programa"][BT_PRINC], filas["programa"]["frecuente"]):
        for u in f["S"]:
            L.append(f"| {f['id'].split('/')[-1]} | {u} | {pct(f['p'][u])} | {pct(g['p'][u])} | {pct(f['sh'][u])} | "
                     f"{pct(f['real'].get(u, 0))} |")
    return "\n".join(L) + "\n", resumen


def cmd_backtest(ramo, ind, temario, args):
    items = leer_items(ramo, ind, temario)
    semilla, corridas = args.semilla, args.corridas or 2000
    filas, meta, modelos = backtest(ramo, ind, temario, items, semilla, corridas)
    texto, resumen = informe_backtest(ramo, filas, meta, modelos, semilla, corridas)
    d = dir_motor(ramo) / "Backtest"
    d.mkdir(parents=True, exist_ok=True)
    nombre = f"{datetime.now():%Y%m%d-%H%M%S}-v{PARAM['version']}"
    (d / f"{nombre}.md").write_text(texto, encoding="utf-8")
    datos = {"version_modelo": PARAM["version"], "hash_datos": hash_datos(ramo), "semilla": semilla,
             "corridas": corridas, "pruebas": meta,
             "filas": {modo: {m: [{k: f[k] for k in ("id", "profesor", "S", "real", "p", "sh")} for f in fs]
                              for m, fs in porm.items()} for modo, porm in filas.items()}}
    (d / f"{nombre}.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ok {d / (nombre + '.md')}")
    for (prof, modo), ms in resumen.items():
        fmt = lambda x: (f"B {x['brier']:.3f} " if modo == "programa" else "") + f"c {x['cuad']:.3f} t1 {100 * x['top1']:.0f}%"
        print(f"{prof:8} {modo:9} motor {fmt(ms[BT_PRINC])} | " +
              " | ".join(f"{b} {fmt(ms[b])}" for b in BT_BASES))


# ---------------------------------------------------------------- aprendizaje continuo (Fase 5)
# Diseno aprobado: datos/motor-predicciones/fase5-diseno.md. Reglas fijadas antes de ver resultados:
# - Se evalua la ultima prediccion emitida en o antes de la fecha real de la prueba y de su ingreso.
#   Emparejamiento: ramo + tipo + numero + periodo; sin numero, solo si hay una sola candidata.
# - Compuerta: el retador reemplaza al campeon solo si (a) el Brier medio por prueba baja con el IC 90 %
#   pareado (boot_dif) entero bajo 0, (b) el cuad no empeora (estimacion puntual) y (c) n >= GATE_N pruebas.
# - Filas del walk-forward: modo programa con alcance incierto (Brier), modo conocido (cuad); una prediccion
#   prospectiva resuelta reemplaza a las filas historicas de su misma prueba y se repite con sus senales.
# - Ajuste MAP en rejilla GRID alrededor del campeon, prior log-normal de sd SD_PRIOR en log por multiplicador.
#   Verosimilitud: log-score de P(entra) (filas con Brier) + entropia cruzada del reparto (filas con cuad).
#   c0 y c1 (un multiplicador para todos los escenarios) y vida media siempre; fb desde N_FB prospectivas con
#   senales; cada beta desde N_BETA resoluciones con esa senal; parametros por ramo desde N_RAMO.
# - Platt regularizado hacia identidad desde PLATT_DESDE pronosticos prospectivos, rodante dentro del
#   walk-forward; isotonica no (necesita del orden de 1000; Niculescu-Mizil y Caruana 2005).
# - Deriva (profesor nuevo, temario cambiado, formato fuera de rango, Brier de las ultimas 3 > uniforme dos veces
#   seguidas): no cambia nada sola; avisa y crea un retador con la vida media a la mitad para ese ramo.
GATE_N, GRID, SD_PRIOR = 5, (1.0, 0.5, 2.0), 0.5
N_FB, N_BETA, N_RAMO, PLATT_DESDE = 3, 8, 10, 50
WF_CORRIDAS = 1000
SENALES = ("clase", "dijo", "biblio", "cercania")


def logit(p):
    p = min(1 - 1e-4, max(1e-4, p))
    return math.log(p / (1 - p))


def recal(p, pl):
    return 1 / (1 + math.exp(-(pl["a"] * logit(p) + pl["b"])))


def platt_vigente():
    st = estado_campeon()
    pl = st.get("platt")
    return pl if pl and pl.get("version") == st["campeon"] else None


def ajustar_platt(fs, lam=1.0):
    """Platt (1999) con penalizacion L2 (lam) hacia la identidad a = 1, b = 0. Newton en dos parametros."""
    a, b = 1.0, 0.0
    for _ in range(50):
        ga, gb, haa, hab, hbb = lam * (a - 1), lam * b, lam, 0.0, lam
        for p, y in fs:
            x = logit(p)
            q = 1 / (1 + math.exp(-(a * x + b)))
            w = q * (1 - q)
            ga, gb = ga + (q - y) * x, gb + (q - y)
            haa, hab, hbb = haa + w * x * x, hab + w * x, hbb + w
        det = haa * hbb - hab * hab
        da, db = (hbb * ga - hab * gb) / det, (haa * gb - hab * ga) / det
        a, b = a - da, b - db
        if abs(da) + abs(db) < 1e-8:
            break
    return {"a": round(a, 4), "b": round(b, 4), "n": len(fs)}


# ------------------------------------------- registros y resoluciones

def dir_ramo(ramo):
    return B.BANCO / B.limpio(ramo)


def registros(ramo):
    out = []
    for f in sorted((dir_ramo(ramo) / "Predicciones").glob("*.json")):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            print(f"x  registro ilegible: {f.name}")
    return out


def resoluciones(ramo):
    fs = sorted((dir_motor(ramo) / "Resueltas").glob("*.json"))
    return sorted((leer(f) for f in fs), key=lambda r: (r["fecha_real"] or r["resuelta"], r["resuelta"]))


def mismo_num(a, b):
    return B.normal(str(a)) == B.normal(str(b))


def clave_prueba(r):
    return (r["tipo"], B.normal(str(r.get("numero") or "")), tuple(r["periodo"]))


def candidatas(regs, ev):
    """Registros de la misma prueba: tipo y periodo iguales; numero igual, o falta en algun lado.
    None = ambiguo (sin numero y varias pruebas distintas posibles)."""
    per = [ev.get("anio"), ev.get("semestre")]
    c = [r for r in regs if r["tipo"] == ev["tipo"] and r["periodo"] == per]
    exactas = [r for r in c if r.get("numero") and ev.get("numero") and mismo_num(r["numero"], ev["numero"])]
    if exactas:
        return exactas
    sueltas = [r for r in c if not r.get("numero") or not ev.get("numero")]
    if len({B.normal(r["evaluacion"]) for r in sueltas}) > 1:
        return None
    return sueltas


def buscar_registro(ramo, ev, ingresado):
    """(registro, fecha_real, nota) o (None, None, motivo)."""
    c = candidatas(registros(ramo), ev)
    if c is None:
        return None, None, "varias predicciones posibles (falta el numero): no se evalua"
    fecha_real = fecha_de(ev.get("fecha"))
    cota = min(x for x in (fecha_real, ingresado) if x) if (fecha_real or ingresado) else date.today()
    nota = "" if fecha_real else f"Sin fecha real de la prueba: se usa el dia del ingreso ({cota}) como cota."
    validas = [r for r in c if datetime.fromisoformat(r["emitida"]).date() <= cota]
    if not validas:
        return None, None, ("no hay prediccion emitida antes de la prueba" if c else "no hay prediccion registrada")
    return max(validas, key=lambda r: r["emitida"]), fecha_real, nota


def leer_registro(ramo, rid):
    return leer(dir_ramo(ramo) / "Predicciones" / f"{rid}.json")


# ------------------------------------------- evaluar y postmortem

def lineas_base(ctx, previas, S, profesor, semilla_txt, corridas):
    """Las cuatro lineas base de la Fase 4, con las mismas reglas que backtest()."""
    out = {"frecuente": base_frecuencia(previas, S)}
    ult = [e for e in previas if clave_orden(e) == clave_orden(previas[-1])] if previas else []
    ult = [e for e in ult if e["profesor"] == profesor] or ult
    out["ultima_prueba"] = base_frecuencia(ult[-1:], S)
    rng = random.Random(semilla_txt)
    out["uniforme"] = bt_fijo(ctx, {u: 1 / len(S) for u in S}, rng, corridas)
    out["programa"] = bt_fijo(ctx, ctx["pi0"], rng, corridas)
    return out


def ctx_registro(ramo, ind, temario, items, reg):
    """Contexto con exactamente lo que vio el pre-registro: sus pruebas, su alcance y sus senales."""
    ids = set(reg["pruebas_usadas"]["profesor"]) | set(reg["pruebas_usadas"]["ramo"])
    ctx = contexto(ramo, ind, temario, items, fecha_de(reg["fecha_prueba"]), reg["profesor"], reg["evaluacion"],
                   alcance=reg["alcance"], entra=reg.get("entra") or (), ids=ids, incierto=reg.get("incierto", False))
    ctx["sen"] = sen_de_json(reg["sen"]) if reg.get("sen") else sen_vacia()
    return ctx


def direccion(reg, real_S):
    """Acierto direccional por senal: la senal movio la unidad hacia su reparto real (k de m unidades)."""
    out, pasos = {}, reg["descomposicion_central"]
    for (_, antes), (n, despues) in zip(pasos, pasos[1:]):
        if n not in SENALES + ("posicion",):
            continue
        k = m = 0
        for u, pa in antes.items():
            mov = despues[u] - pa
            if abs(mov) < 1e-6:
                continue
            m += 1
            k += abs(real_S.get(u, 0) - pa) > 1e-9 and (mov > 0) == (real_S.get(u, 0) - pa > 0)
        if m:
            out[n] = [k, m]
    return out


def deriva(ramo, ev_id, ev, reg, items, res_ramo, brier, brier_unif):
    """Disparadores de contexto y de error (seccion 5.4)."""
    d = []
    otros = [e for i, e in items["evaluaciones"].items() if i != ev_id]
    if ev.get("profesor") and ev["profesor"] not in {e.get("profesor") for e in otros}:
        d.append(f"profesor nuevo en el ramo ({ev['profesor']})")
    if reg.get("hash_temario") and reg["hash_temario"] != hash_temario(ramo):
        d.append("el temario cambio desde la prediccion (unidades, pesos u objetivos)")
    ns = [len(e["items"]) for e in otros if e.get("profesor") == ev.get("profesor")]
    if len(ns) >= 2 and not min(ns) <= len(ev["items"]) <= max(ns):
        d.append(f"formato: {len(ev['items'])} preguntas, fuera del rango del profesor ({min(ns)}-{max(ns)})")
    serie = [(r["metricas"]["brier"], r["bases"]["uniforme"]["brier"]) for r in res_ramo] + [(brier, brier_unif)]
    malo = lambda s: len(s) >= 3 and sum(a for a, _ in s[-3:]) > sum(b for _, b in s[-3:])
    if malo(serie) and malo(serie[:-1]):
        d.append("error: el Brier de las ultimas 3 resoluciones supera al de la linea base uniforme dos veces seguidas")
    return d


def actualizar_dominio(ramo, ev_id, ev, meta):
    """Suma logrado/posible por unidad si la prueba es tuya y trae el puntaje obtenido por pregunta."""
    if not meta.get("rendida"):
        return "sin cambios (la prueba no esta marcada como rendida)"
    ficha = B.leer_eval(meta)
    obt = {str(p.get("n")): num_puntos(p.get("obtenido")) for p in ficha["preguntas"]}
    if not any(v is not None for v in obt.values()):
        return "sin cambios (la ficha no trae el puntaje obtenido por pregunta)"
    f = dir_motor(ramo) / "dominio.json"
    d = leer(f, {})
    if ev_id in d.get("_fuentes", []):
        return "ya estaba sumada"
    for it in ev["items"]:
        o = obt.get(it["n"])
        if o is None:
            continue
        for u, fr in it["unidades"].items():  # en "preguntas equivalentes": cada pregunta vale 1 x su fraccion
            x = d.setdefault(u, {})
            x["logrado"] = round(float(x.get("logrado", 0)) + min(o, it["puntos"]) / it["puntos"] * fr, 4)
            x["posible"] = round(float(x.get("posible", 0)) + fr, 4)
    d.setdefault("_fuentes", []).append(ev_id)
    escribir(f, d)
    return "actualizado (logrado/posible por unidad, en preguntas equivalentes)"


def evaluar(ramo, ind, temario, items, ev_id, silencioso=False):
    """Resuelve el pre-registro de una prueba recien ingresada. Devuelve la resolucion o None."""
    ev, meta = items["evaluaciones"][ev_id], ind["evaluaciones"][ev_id]
    hechas = resoluciones(ramo)
    if any(r["evaluacion_id"] == ev_id for r in hechas):
        print(f"=  {ev_id}: ya estaba resuelta; un ingreso nuevo de la misma prueba no la vuelve a resolver.")
        return None
    ingresado = fecha_de(B.leer_eval(meta).get("ingresado"))
    reg, fecha_real, nota = buscar_registro(ramo, ev, ingresado)
    if not reg:
        if not silencioso:
            print(f"-  {ev_id}: {nota}")
        return None
    S = reg["alcance"]
    c = reg["por_escenario"]["central"]
    fila = {"S": S, "real": verdad(ev), "p": {u: c[u]["p"] for u in S}, "sh": {u: c[u]["e"] / 100 for u in S}}
    ctx = ctx_registro(ramo, ind, temario, items, reg)
    previas = sorted(ctx["evs_ramo"] + ctx["evs_prof"], key=clave_orden)
    bases = lineas_base(ctx, previas, S, ev["profesor"], f"{reg['semilla']}-{reg['id']}-base", WF_CORRIDAS)
    me = metricas([fila])
    mb = {b: dict(metricas([dict(fila, p=p, sh=sh)]), brier_prueba=brier_prueba(dict(fila, p=p)))
          for b, (p, sh) in bases.items()}
    fuera = sum(v for u, v in fila["real"].items() if u not in S)
    tS = sum(v for u, v in fila["real"].items() if u in S) or 1
    real_S = {u: fila["real"].get(u, 0) / tS for u in S}
    dirs = direccion(reg, real_S)
    sorpresa = [u for u in S if fila["real"].get(u, 0) > 0 and fila["p"][u] < 0.3] + \
               [u for u in fila["real"] if u not in S]
    sin_mapa = sorted({t for it in ev["items"] for t in unidades_item(it["temas"], temario)[1]})
    prof_ok = bool(reg["profesor"]) and bool(B.parecido(ev.get("profesor"), [reg["profesor"]], 0.6)) and \
        bool(reg["pruebas_usadas"]["profesor"])
    causas = []
    if fuera > 0.10:
        causas.append(f"alcance: {fuera * 100:.0f} % de los puntos cayo fuera del alcance predicho")
    if not prof_ok:
        causas.append("profesor: el de la prueba no es el del registro, o no tenia pruebas en el banco")
    if sin_mapa:
        causas.append(f"tema nuevo / taxonomia: {len(sin_mapa)} temas sin unidad ({', '.join(sin_mapa[:4])})")
    if not reg["n_clases"] and reg["fuerza"].startswith("débil"):
        causas.append("senal ausente: sin clases transcritas y con historia debil")
    for s, (k, m) in dirs.items():
        if k / m < 0.5:
            causas.append(f"senal enganosa: {s} acerto la direccion en {k} de {m} unidades")
    brier, b_unif = brier_prueba(fila), mb["uniforme"]["brier_prueba"]
    der = deriva(ramo, ev_id, ev, reg, items, hechas, brier, b_unif)
    dom = actualizar_dominio(ramo, ev_id, ev, meta)
    activas = sorted({k for f in reg["factores_central"].values() for k in f})
    res = {"id_registro": reg["id"], "evaluacion_id": ev_id, "evaluacion": reg["evaluacion"],
           "periodo": reg["periodo"], "resuelta": datetime.now().isoformat(timespec="seconds"),
           "fecha_real": fecha_real.isoformat() if fecha_real else None, "nota_fecha": nota,
           "emitida": reg["emitida"], "version_modelo": reg["version_modelo"], "profesor": ev.get("profesor"),
           "S": S, "real": {u: round(v, 4) for u, v in fila["real"].items()}, "p": fila["p"], "sh": fila["sh"],
           "metricas": {"brier": brier, "log": me["log"], "cuad": me["cuad"], "top1": me["top1"], "top2": me["top2"]},
           "bases": {b: {"brier": m["brier_prueba"], "cuad": m["cuad"], "top1": m["top1"]} for b, m in mb.items()},
           "fuera_alcance": fuera, "senales": dirs, "activas": activas, "sorpresas": sorpresa, "sin_mapa": sin_mapa,
           "causas": causas, "deriva": der, "dominio": dom}
    f = dir_motor(ramo) / "Resueltas" / f"{reg['id']}.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "x", encoding="utf-8") as fh:  # la resolucion tampoco se sobrescribe
        json.dump(res, fh, ensure_ascii=False, indent=1)
    f.chmod(0o444)
    pm = postmortem(ramo, temario, res)
    print(f"ok resuelta {reg['evaluacion']} con el registro {reg['id']}: Brier {brier:.3f} (uniforme {b_unif:.3f})"
          f", cuad {me['cuad']:.3f} -> {pm}")
    for x in der:
        print(f"!  deriva: {x}")
    return res


def postmortem(ramo, temario, r):
    pct = lambda x: f"{100 * x:.0f} %"
    nom = lambda u: f"{u} {temario['por_id'][u]['nombre']}" if u in temario["por_id"] else u
    L = [f"# Postmortem · {r['evaluacion']} {r['periodo'][0]}-{r['periodo'][1]} · {ramo}", "",
         f"- **Registro evaluado:** `{r['id_registro']}` (emitido {r['emitida']}, modelo v{r['version_modelo']}). "
         f"Fecha real de la prueba: {r['fecha_real'] or '—'}. {r['nota_fecha']}".rstrip(),
         f"- **Alcance predicho:** {', '.join(r['S'])}. Puntos reales fuera de él: {pct(r['fuera_alcance'])}.",
         "- Se evalúa la predicción tal como quedó congelada; las líneas base usan las mismas pruebas que ella.", "",
         "| Modelo | Brier (P entra) | Cuad (reparto) | Top-1 |", "|---|---|---|---|",
         f"| **motor** | {r['metricas']['brier']:.3f} | {r['metricas']['cuad']:.3f} | {pct(r['metricas']['top1'])} |"]
    for b, m in r["bases"].items():
        L.append(f"| {b} | {m['brier']:.3f} | {m['cuad']:.3f} | {pct(m['top1'])} |")
    L += ["", "_Una sola prueba no dice si el motor sirve: eso lo dice el tablero con n ≥ 5._", "",
          "## Por unidad", "", "| Unidad | P(entra) | Reparto predicho | Reparto real |", "|---|---|---|---|"]
    for u in r["S"]:
        L.append(f"| {nom(u)} | {pct(r['p'][u])} | {pct(r['sh'][u])} | {pct(r['real'].get(u, 0))} |")
    for u in r["real"]:
        if u not in r["S"]:
            L.append(f"| {nom(u)} (fuera del alcance) | — | — | {pct(r['real'][u])} |")
    L += ["", "## Señales (acierto direccional: la señal movió la unidad hacia su reparto real)", ""]
    L += [f"- {s}: {k} de {m} unidades" for s, (k, m) in r["senales"].items()] or ["- Ninguna señal movió el reparto."]
    L += ["", "## Sorpresas", "",
          "- Unidades con puntos y P(entra) < 30 % o fuera del alcance: " + (", ".join(r["sorpresas"]) or "ninguna"),
          "- Temas sin unidad del programa: " + (", ".join(r["sin_mapa"]) or "ninguno"), "",
          "## Causas probables (reglas fijas, sin LLM)", ""]
    L += [f"- {c}" for c in r["causas"]] or ["- Ninguna regla se activó."]
    L += ["", "## Deriva", ""] + ([f"- ⚠ {d}" for d in r["deriva"]] or ["- Sin disparadores."])
    if r["deriva"]:
        L.append("- El próximo `motor ciclo` prueba un retador con la vida media a la mitad para este ramo.")
    L += ["", "## Dominio", "", f"- {r['dominio']}"]
    d = dir_ramo(ramo) / "Postmortem"
    d.mkdir(parents=True, exist_ok=True)
    f = d / f"{B.limpio(r['evaluacion'])} {r['periodo'][0]}-{r['periodo'][1]}.md"
    f.write_text("\n".join(L) + "\n", encoding="utf-8")
    return f


# ------------------------------------------- walk-forward de una version cualquiera

def cargar_datos():
    """Todos los ramos con Motor/temario.json y pruebas en el banco, listos para el walk-forward."""
    ind = B.leer_indice()
    out = []
    for t in sorted(B.BANCO.glob("*/Motor/temario.json")):
        ramo = B.parecido(t.parent.parent.name, set(B.ramos_conocidos(ind)), 0.5) or t.parent.parent.name
        if not any(m["ramo"] == ramo for m in ind["evaluaciones"].values()):
            continue
        temario = leer_temario(ramo)
        out.append({"ramo": ramo, "ind": ind, "temario": temario, "items": leer_items(ramo, ind, temario),
                    "resueltas": resoluciones(ramo)})
    return out


def fila_wf(ramo, modo, i, ev, S, p, sh, prosp=False, activas=(), orden=None):
    f = {"ramo": ramo, "id": i, "modo": modo, "S": S, "real": verdad(ev), "p": p, "sh": sh, "prosp": prosp,
         "activas": list(activas), "orden": orden or clave_orden(ev)}
    f["brier"] = brier_prueba(f) if modo in ("programa", "prosp") else None
    f["cuad"] = cuad(f) if modo in ("conocido", "prosp") else None
    return f


def walk_forward(P, datos, solo_prosp=False, semilla=7, corridas=WF_CORRIDAS):
    """Filas de la version P: historicas sin senales + prospectivas repetidas con sus senales guardadas.
    Mismas semillas para cualquier version (numeros aleatorios comunes: la comparacion es pareada)."""
    filas = []
    for d in datos:
        ramo, ind, temario, items = d["ramo"], d["ind"], d["temario"], d["items"]
        previo = usar_param(P, ramo)
        try:
            central = ESCENARIOS["central"]
            resueltas = {r["evaluacion_id"]: r for r in d["resueltas"] if r["evaluacion_id"] in items["evaluaciones"]}
            for i, r in resueltas.items():
                reg = leer_registro(ramo, r["id_registro"])
                ctx = ctx_registro(ramo, ind, temario, items, reg)
                p, sh = bt_motor(ctx, central, "prueba", random.Random(f"{semilla}-{i}-prosp"), corridas)
                filas.append(fila_wf(ramo, "prosp", i, items["evaluaciones"][i], reg["alcance"], p, sh, True,
                                     r["activas"], (r["fecha_real"] or r["resuelta"],)))
            if solo_prosp:
                continue
            S_prog = [u["id"] for u in temario["unidades"] if not u.get("opcional")]
            for i, ev in sorted(items["evaluaciones"].items(), key=lambda x: clave_orden(x[1])):
                if i in resueltas or not (ev.get("anio") and ev.get("semestre")):
                    continue
                fecha = date(ev["anio"], 5 if ev["semestre"] == 1 else 10, 1)
                evaluacion = f"{ev['tipo']} {ev.get('numero') or ''}".strip()
                for modo in ("programa", "conocido"):
                    S = S_prog if modo == "programa" else [u for u in temario["orden"] if u in ev["alcance"]]
                    if len(S) < 2:
                        continue
                    ctx = contexto(ramo, ind, temario, items, fecha, ev["profesor"], evaluacion, alcance=S,
                                   antes_de=clave_orden(ev), incierto=(modo == "programa"))
                    ctx["sen"] = sen_vacia()
                    p, sh = bt_motor(ctx, central, "prueba", random.Random(f"{semilla}-{i}-{modo}"), corridas)
                    filas.append(fila_wf(ramo, modo, i, ev, S, p, sh))
        finally:
            usar_param(previo)
    return filas


def platt_rodante(filas):
    """Recalibra cada fila prospectiva con Platt ajustado solo en las prospectivas anteriores (>= PLATT_DESDE)."""
    out, vistos = [], []
    for f in sorted(filas, key=lambda f: (not f["prosp"], f["orden"])):
        if f["prosp"]:
            g = dict(f)
            if len(vistos) >= PLATT_DESDE:
                pl = ajustar_platt(vistos)
                g["p"] = {u: recal(f["p"][u], pl) for u in f["S"]}
                g["brier"] = brier_prueba(g)
            vistos += [(f["p"][u], entro(f, u)) for u in f["S"]]
            out.append(g)
        else:
            out.append(f)
    return out


def resumen_filas(filas):
    m = lambda xs: sum(xs) / len(xs) if xs else None
    b, c = [f["brier"] for f in filas if f["brier"] is not None], [f["cuad"] for f in filas if f["cuad"] is not None]
    return {"n_brier": len(b), "brier": m(b), "n_cuad": len(c), "cuad": m(c),
            "n_prosp": sum(f["prosp"] for f in filas)}


def compuerta(filas_c, filas_r, semilla=7):
    clave = lambda f: (f["ramo"], f["id"], f["modo"])
    r = {clave(f): f for f in filas_r}
    pares_b = [(r[clave(f)]["brier"], f["brier"]) for f in filas_c if f["brier"] is not None and clave(f) in r]
    pares_c = [(r[clave(f)]["cuad"], f["cuad"]) for f in filas_c if f["cuad"] is not None and clave(f) in r]
    n = len(pares_b)
    a, b = [x for x, _ in pares_b], [y for _, y in pares_b]
    ic = boot_dif(a, b, random.Random(f"{semilla}-compuerta"))
    dif = (sum(a) - sum(b)) / n if n else None
    cr = sum(x for x, _ in pares_c) / len(pares_c) if pares_c else None
    cc = sum(y for _, y in pares_c) / len(pares_c) if pares_c else None
    motivos = []
    if n < GATE_N:
        motivos.append(f"n = {n} < {GATE_N}")
    if not ic or ic[1] >= 0:
        motivos.append("el IC 90 % del Brier no queda entero bajo 0")
    if cr is not None and cr > cc + 1e-12:
        motivos.append("el cuad empeora")
    return {"n": n, "dif_brier": dif, "ic90": list(ic) if ic else None, "cuad_campeon": cc, "cuad_retador": cr,
            "n_cuad": len(pares_c), "pasa": not motivos, "motivos": motivos}


# ------------------------------------------- ajuste MAP y versiones

def variar(P, mc=1.0, mv=1.0, mfb=1.0, mbeta=None):
    Q = json.loads(json.dumps(P))
    for esc in Q["escenarios"].values():
        esc["c0"], esc["c1"], esc["fb"] = round(esc["c0"] * mc, 3), round(esc["c1"] * mc, 3), round(esc["fb"] * mfb, 3)
    Q["vida_media_semestres"] = round(Q["vida_media_semestres"] * mv, 3)
    for s, m in (mbeta or {}).items():
        Q["beta"][s] = round(Q["beta"][s] * m, 3)
    return Q


def log_vero(filas):
    ll = 0.0
    for f in filas:
        if f["brier"] is not None:
            for u in f["S"]:
                q = min(0.99, max(0.01, f["p"][u]))
                ll += math.log(q if entro(f, u) else 1 - q)
        if f["cuad"] is not None:
            ll += sum(r * math.log(max(1e-3, f["sh"][u])) for u, r in f["real"].items() if u in f["S"])
    return ll


def log_post(filas, ms):
    return log_vero(filas) - sum(math.log(m) ** 2 for m in ms) / (2 * SD_PRIOR ** 2)


def rejilla(datos, filas_base, hacer, n_mult, solo_prosp=False):
    """Mejor punto de la rejilla; empieza por el campeon (x1) y solo cambia si mejora estrictamente."""
    import itertools
    mejor = None
    for ms in itertools.product(GRID, repeat=n_mult):
        filas = filas_base if all(m == 1.0 for m in ms) else walk_forward(hacer(*ms), datos, solo_prosp)
        v = log_post(filas, ms)
        if mejor is None or v > mejor[0] + 1e-9:
            mejor = (v, ms, filas)
    return mejor[1], mejor[2]


def ajustar(P, datos, filas_c):
    """Retador MAP (seccion 5.4). Devuelve (parametros, descripcion) o (None, motivo) si sale igual al campeon."""
    (mc, mv), filas = rejilla(datos, filas_c, lambda a, b: variar(P, a, b), 2)
    desc = [f"c0,c1 ×{mc:g}", f"vida media ×{mv:g}"]
    prosp = [f for f in filas if f["prosp"]]
    mfb, mbeta = 1.0, {}
    base = variar(P, mc, mv)
    if sum(1 for f in prosp if f["activas"]) >= N_FB:
        (mfb,), _ = rejilla(datos, prosp, lambda a: variar(base, mfb=a), 1, True)
        desc.append(f"fb ×{mfb:g}")
    for s in SENALES:
        if sum(1 for f in prosp if s in f["activas"]) >= N_BETA:
            Q = variar(base, mfb=mfb, mbeta=mbeta)
            (m,), _ = rejilla(datos, walk_forward(Q, datos, True), lambda a: variar(Q, mbeta={s: a}), 1, True)
            if m != 1.0:
                mbeta[s] = m
                desc.append(f"β {s} ×{m:g}")
    Q = variar(P, mc, mv, mfb, mbeta)
    for d in datos:  # parametros propios de un ramo: solo con >= N_RAMO resoluciones; el prior los encoge
        if len(d["resueltas"]) >= N_RAMO:
            propio = lambda a, b: {k: variar(Q, a, b)[k] for k in ("escenarios", "vida_media_semestres")}
            con = lambda a, b: dict(Q, por_ramo=dict(Q.get("por_ramo") or {}, **{d["ramo"]: propio(a, b)}))
            (a, b), _ = rejilla([d], walk_forward(Q, [d]), con, 2)
            if (a, b) != (1.0, 1.0):
                Q = con(a, b)
                desc.append(f"{d['ramo']}: c ×{a:g}, vida ×{b:g}")
    if mismos(Q, P):
        return None, "el MAP queda en el campeon (ningun punto de la rejilla mejora la posterior)"
    return Q, "MAP en rejilla: " + ", ".join(desc)


CLAVES_MODELO = ("escenarios", "beta", "vida_media_semestres", "peso_otra_universidad", "dias_cercania",
                 "remuestreos_etiqueta", "alcance_posicion", "por_ramo")


def mismos(P, Q):
    return all(P.get(k) == Q.get(k) for k in CLAVES_MODELO)


def guardar_version(Q, padre, origen):
    """Reutiliza una version identica si ya existe; si no, crea la siguiente menor (1.2, 1.3...)."""
    for f in sorted(VERSIONES.glob("v*.json")):
        V = json.loads(f.read_text(encoding="utf-8"))
        if mismos(V, Q):
            return V["version"], False
    mayor = padre.split(".")[0]
    menores = [int(f.stem.split(".")[1]) for f in VERSIONES.glob(f"v{mayor}.*.json")]
    v = f"{mayor}.{max(menores) + 1}"
    Q = dict(Q, version=v, fecha=f"{date.today()}", padre=padre, origen=origen)
    f = VERSIONES / f"v{v}.json"
    with open(f, "x", encoding="utf-8") as fh:
        json.dump(Q, fh, ensure_ascii=False, indent=1)
    f.chmod(0o444)
    return v, True


# ------------------------------------------- ciclo, rollback, tablero

def hash_global():
    h = hashlib.sha1()
    for t in sorted(B.BANCO.glob("*/Motor/temario.json")):
        h.update(t.parent.parent.name.encode())
        for n in ("temario.json", "items.json", "senales.json"):
            f = t.parent / n
            h.update(f.read_bytes() if f.exists() else b"-")
        h.update(",".join(sorted(f.name for f in (t.parent / "Resueltas").glob("*.json"))).encode())
    h.update(json.dumps(estado_campeon().get("campeon")).encode())
    return h.hexdigest()


def guardar_estado(st):
    CAMPEON_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def anotar_retador(st, por_probar, v, origen, hoy):
    if v == st["campeon"] or any(r["version"] == v for r in por_probar):
        return
    ent = next((r for r in st["retadores"] if r["version"] == v), None)
    if not ent:
        ent = {"version": v, "creado": hoy, "origen": origen, "estado": "pendiente", "resultados": []}
        st["retadores"].append(ent)
    por_probar.append(ent)


def ciclo(motivo="manual"):
    """Campeon contra retadores (pendientes, estructurales, MAP y de deriva); aplica la compuerta."""
    st = estado_campeon()
    datos = cargar_datos()
    if not datos:
        print("No hay ramos con Motor/temario.json y pruebas en el banco.")
        return
    campeon = st["campeon"]
    Pc = cargar_version(campeon)
    hoy = f"{datetime.now():%Y-%m-%d %H:%M}"
    print(f"Walk-forward del campeon v{campeon}...")
    filas_c = walk_forward(Pc, datos)
    # pendientes y estructurales (estos se reevaluan en cada ciclo mientras no ganen: la evidencia crece)
    por_probar = [r for r in st["retadores"] if r["version"] != campeon and
                  (r["estado"] == "pendiente" or r["origen"].startswith("estructural"))]
    print("Ajuste MAP en rejilla...")
    Q, desc = ajustar(Pc, datos, filas_c)
    if Q:
        v, nueva = guardar_version(Q, campeon, desc)
        print(f"Retador MAP: v{v} ({desc}){'' if nueva else ' (ya existia)'}")
        anotar_retador(st, por_probar, v, desc, hoy)
    else:
        print(f"Sin retador MAP: {desc}")
    atendida = st.setdefault("deriva_atendida", [])
    for d in datos:
        nuevas = [r for r in d["resueltas"] if r["deriva"] and r["id_registro"] not in atendida]
        if not nuevas:
            continue
        propio = dict((Pc.get("por_ramo") or {}).get(d["ramo"]) or {},
                      vida_media_semestres=efectivos(Pc, d["ramo"])["vida_media_semestres"] / 2)
        Qd = dict(Pc, por_ramo=dict(Pc.get("por_ramo") or {}, **{d["ramo"]: propio}))
        org = f"deriva en {d['ramo']} ({nuevas[-1]['deriva'][0]}): vida media a la mitad"
        v, _ = guardar_version(Qd, campeon, org)
        anotar_retador(st, por_probar, v, org, hoy)
        atendida += [r["id_registro"] for r in nuevas]
    ganadores = []
    for ent in por_probar:
        print(f"Walk-forward del retador v{ent['version']}...")
        fr = walk_forward(cargar_version(ent["version"]), datos)
        g = compuerta(filas_c, fr)
        ent["resultados"].append(dict(g, fecha=hoy, contra=campeon))
        ent["estado"] = "archivado"
        ic = f"[{g['ic90'][0]:+.4f}, {g['ic90'][1]:+.4f}]" if g["ic90"] else "—"
        print(f"  v{ent['version']}: ΔBrier {g['dif_brier']:+.4f} IC90 {ic}, cuad {g['cuad_retador']:.4f} vs "
              f"{g['cuad_campeon']:.4f}, n = {g['n']} -> "
              + ("PASA" if g["pasa"] else "no pasa: " + "; ".join(g["motivos"])))
        if g["pasa"]:
            ganadores.append((g["dif_brier"], ent, fr))
    if ganadores:
        _, ent, fr = min(ganadores, key=lambda x: x[0])
        ent["estado"] = "campeon"
        st["historial"].append({"fecha": hoy, "de": campeon, "a": ent["version"],
                                "motivo": f"paso la compuerta ({motivo})"})
        st["campeon"], filas_c, campeon = ent["version"], fr, ent["version"]
        print(f"Nuevo campeon: v{campeon}")
    # Platt: solo con >= PLATT_DESDE pronosticos prospectivos y si pasa la misma compuerta en las prospectivas
    prosp = [f for f in filas_c if f["prosp"]]
    n_fs = sum(len(f["S"]) for f in prosp)
    st["platt"] = None
    if n_fs >= PLATT_DESDE:
        g = compuerta(prosp, [f for f in platt_rodante(filas_c) if f["prosp"]])
        if g["pasa"]:
            st["platt"] = dict(ajustar_platt([(f["p"][u], entro(f, u)) for f in prosp for u in f["S"]]),
                               version=campeon, fecha=hoy)
        print(f"Platt ({n_fs} pronosticos prospectivos): {'adoptado' if st['platt'] else 'no pasa la compuerta'}")
    st["ultimo_ciclo"] = {"fecha": hoy, "motivo": motivo, "hash": None, "campeon": campeon,
                          "walk_forward": resumen_filas(filas_c)}
    guardar_estado(st)
    st["ultimo_ciclo"]["hash"] = hash_global()  # despues de guardar: el hash incluye al campeon vigente
    guardar_estado(st)
    print(f"ok {tablero(datos)}")


def rollback(version, motivo):
    cargar_version(version)
    st = estado_campeon()
    st["historial"].append({"fecha": f"{datetime.now():%Y-%m-%d %H:%M}", "de": st["campeon"], "a": version,
                            "motivo": f"rollback manual: {motivo or 'sin motivo indicado'}"})
    st["campeon"] = version
    if (st.get("platt") or {}).get("version") != version:
        st["platt"] = None
    guardar_estado(st)
    print(f"ok campeon = v{version} (no se borro nada). Corre `motor ciclo` para rehacer el tablero.")


def vencidas(ramo):
    """Pruebas con prediccion cuya fecha ya paso y que no tienen resolucion (la ultima emitida de cada una)."""
    regs = registros(ramo)
    hechas = {r["id_registro"] for r in resoluciones(ramo)}
    resueltas = {clave_prueba(r) for r in regs if r["id"] in hechas}
    ultimas = {}
    for r in regs:
        k = clave_prueba(r)
        if k not in ultimas or r["emitida"] > ultimas[k]["emitida"]:
            ultimas[k] = r
    return [r for k, r in ultimas.items() if k not in resueltas and fecha_de(r["fecha_prueba"]) < date.today()]


def lineas_estado():
    out = []
    for t in sorted(B.BANCO.glob("*/Predicciones")):
        for r in vencidas(t.parent.name):
            out.append(f"Prediccion vencida sin resolver: {r['ramo']} · {r['evaluacion']} ({r['fecha_prueba']}). "
                       "Ingresa la prueba (con --fecha si no la trae) y se evalua sola.")
    st = estado_campeon()
    if st.get("ultimo_ciclo"):
        out.append(f"Motor: campeon v{st['campeon']}, ultimo ciclo {st['ultimo_ciclo']['fecha']} "
                   f"({B.BANCO / 'DESEMPENO_MOTOR.md'})")
    return out


def boot_media(xs, rng):
    if len(xs) < 2:
        return None
    ms = sorted(sum(rng.choice(xs) for _ in xs) / len(xs) for _ in range(BT_BOOT))
    return ms[int(0.05 * BT_BOOT)], ms[int(0.95 * BT_BOOT) - 1]


def veredicto(motor, bases, rng):
    n = len(motor)
    if n < GATE_N:
        return f"**Veredicto: sin evidencia todavía** (n = {n} < {GATE_N} resoluciones prospectivas)."
    mejor = min(bases, key=lambda b: sum(bases[b]) / n)
    x = boot_dif(motor, bases[mejor], rng)
    dif = (sum(motor) - sum(bases[mejor])) / n
    if x[1] < 0:
        txt = f"el motor le gana a «{mejor}», la mejor línea base"
    elif x[0] > 0:
        txt = f"el motor pierde contra «{mejor}»"
    else:
        txt = f"el motor no le gana a «{mejor}» (el IC incluye 0)"
    return f"**Veredicto:** {txt}: ΔBrier {dif:+.3f} [{x[0]:+.3f}, {x[1]:+.3f}], n = {n}."


def tablero(datos=None):
    datos = datos if datos is not None else cargar_datos()
    st = estado_campeon()
    rng = random.Random("tablero")
    ic = lambda x: f"[{x[0]:.3f}, {x[1]:.3f}]" if x else "—"
    icd = lambda x: f"[{x[0]:+.4f}, {x[1]:+.4f}]" if x else "—"
    barra = lambda x: "█" * round(x * 40)
    pl = st.get("platt")
    L = ["# Desempeño del motor de predicción", "",
         f"Actualizado {datetime.now():%Y-%m-%d %H:%M} · campeón **v{st['campeon']}** · Platt: "
         + (f"a = {pl['a']:.2f}, b = {pl['b']:.2f} (n = {pl['n']})" if pl else
            f"no (hace falta ≥ {PLATT_DESDE} pronósticos prospectivos y pasar la compuerta)"),
         "", "Toda cifra va con su n y su IC 90 %. Brier: menor es mejor (0,25 = decir 50 % siempre). Reglas: "
         "`datos/motor-predicciones/fase5-diseno.md` (proyecto de metodología).", ""]
    todas_fs, global_m, global_b = [], [], defaultdict(list)
    for d in datos:
        rs = d["resueltas"]
        L += [f"## {d['ramo']} — predicciones prospectivas resueltas (n = {len(rs)})", ""]
        venc = vencidas(d["ramo"])
        if venc:
            L += ["Vencidas sin resolver: " + ", ".join(f"{r['evaluacion']} ({r['fecha_prueba']})" for r in venc), ""]
        if not rs:
            L += ["Todavía ninguna. **Veredicto: sin evidencia todavía.**", ""]
            continue
        L += ["| Prueba | Fecha | Motor | Frecuente | Última | Uniforme | Programa | Cuad motor | Media acumulada [IC 90 %] |",
              "|---|---|---|---|---|---|---|---|---|"]
        acum = []
        for r in rs:
            acum.append(r["metricas"]["brier"])
            mu, b = sum(acum) / len(acum), r["bases"]
            L.append(f"| {r['evaluacion']} {r['periodo'][0]}-{r['periodo'][1]} | {r['fecha_real'] or '—'} | "
                     f"{r['metricas']['brier']:.3f} | {b['frecuente']['brier']:.3f} | {b['ultima_prueba']['brier']:.3f} | "
                     f"{b['uniforme']['brier']:.3f} | {b['programa']['brier']:.3f} | {r['metricas']['cuad']:.3f} | "
                     f"{mu:.3f} {ic(boot_media(acum, rng))} `{barra(mu)}` |")
            todas_fs += [(r["p"][u], 1 if r["real"].get(u, 0) > 0 else 0) for u in r["S"]]
        global_m += acum
        for bn in BT_BASES:
            global_b[bn] += [r["bases"][bn]["brier"] for r in rs]
        L += ["", veredicto(acum, {bn: [r["bases"][bn]["brier"] for r in rs] for bn in BT_BASES}, rng), ""]
    if len(datos) > 1 and global_m:
        L += ["## Todos los ramos", "", veredicto(global_m, global_b, rng), ""]
    if todas_fs:
        L += ["## Calibración de P(entra) (pronósticos prospectivos)", "",
              "| Intervalo | n | Pronóstico medio | Observado | Consistencia 5-95 % |", "|---|---|---|---|---|"]
        for c in calibracion(todas_fs, rng):
            fuera = "" if c["lo"] <= c["obs"] <= c["hi"] else " (fuera)"
            L.append(f"| {c['intervalo']} | {c['n']} | {c['pron'] * 100:.0f} % | {c['obs'] * 100:.0f} %{fuera} | "
                     f"{c['lo'] * 100:.0f}-{c['hi'] * 100:.0f} % |")
        L.append("")
    uc = st.get("ultimo_ciclo") or {}
    if uc.get("walk_forward"):
        w = uc["walk_forward"]
        L += ["## Walk-forward del campeón (historia sin señales + prospectivas repetidas)", "",
              f"Último ciclo {uc['fecha']} ({uc['motivo']}): Brier medio {w['brier']:.3f} en {w['n_brier']} pruebas, "
              f"cuad medio {w['cuad']:.3f} en {w['n_cuad']}; {w['n_prosp']} prospectivas. Es diagnóstico: la "
              "historia ya se usó para diseñar el motor.", ""]
    L += ["## Versiones", "", "| Fecha | De | A | Motivo |", "|---|---|---|---|"]
    L += [f"| {h['fecha']} | {h['de'] or '—'} | {h['a']} | {h['motivo']} |" for h in st["historial"]]
    L += ["", "| Retador | Estado | Origen | Último resultado contra el campeón |", "|---|---|---|---|"]
    for r in st["retadores"]:
        g = r["resultados"][-1] if r["resultados"] else None
        txt = (f"ΔBrier {g['dif_brier']:+.4f} IC90 {icd(g['ic90'])}, cuad {g['cuad_retador']:.4f} vs "
               f"{g['cuad_campeon']:.4f}, n = {g['n']} ({g['fecha']}, contra v{g['contra']}): "
               + ("pasa" if g["pasa"] else "no pasa — " + "; ".join(g["motivos"]))) if g else "sin evaluar"
        L.append(f"| v{r['version']} | {r['estado']} | {r['origen']} | {txt} |")
    f = B.BANCO / "DESEMPENO_MOTOR.md"
    f.write_text("\n".join(L) + "\n", encoding="utf-8")
    return f


def semanal():
    """Tarea de Windows (domingo 20:00): ciclo solo si cambiaron los datos; si no, solo el tablero."""
    print(f"[{datetime.now():%Y-%m-%d %H:%M}] motor semanal")
    for x in lineas_estado():
        print(x)
    if (estado_campeon().get("ultimo_ciclo") or {}).get("hash") != hash_global():
        ciclo("semanal: cambiaron los datos")
    else:
        print(f"Sin cambios desde el ultimo ciclo. ok {tablero()}")


def al_ingresar(ids):
    """Gancho de `ingresar`: regenera items, resuelve los pre-registros y corre el ciclo si hubo resoluciones."""
    ind = B.leer_indice()
    hubo = False
    for ramo in sorted({ind["evaluaciones"][i]["ramo"] for i in ids if i in ind["evaluaciones"]}):
        if not (dir_motor(ramo) / "temario.json").exists():
            continue
        temario = leer_temario(ramo)
        items, _ = construir_items(ramo, ind, temario)
        for i in ids:
            if i in items["evaluaciones"]:
                hubo |= evaluar(ramo, ind, temario, items, i) is not None
    if hubo:
        ciclo("ingreso de una prueba con prediccion")


def cmd_motor_fase5(args):
    if args.accion == "ciclo":
        ciclo(args.motivo or "manual")
    elif args.accion == "semanal":
        semanal()
    elif args.accion == "tablero":
        print(f"ok {tablero()}")
    elif args.accion == "rollback":
        if not args.version:
            sys.exit("Falta --version (p. ej. --version 1.0).")
        rollback(args.version.lstrip("v"), args.motivo)
    elif args.accion == "evaluar":
        if not args.ramo:
            sys.exit("Falta --ramo.")
        ramo, ind = resolver_ramo(args.ramo)
        temario = leer_temario(ramo)
        items, _ = construir_items(ramo, ind, temario)
        ids = list(items["evaluaciones"])
        if args.evaluacion:
            partes = args.evaluacion.split()
            t, num = B.normalizar_tipo(partes[0]), " ".join(partes[1:])
            ids = [i for i in ids if items["evaluaciones"][i]["tipo"] == t and
                   (not num or mismo_num(items["evaluaciones"][i].get("numero"), num))]
            if not ids:
                sys.exit(f"No hay una prueba «{args.evaluacion}» de {ramo} en el banco: ingresala primero.")
        if not any([evaluar(ramo, ind, temario, items, i, silencioso=not args.evaluacion) for i in ids]):
            print("Nada nuevo que resolver.")
        else:
            ciclo(f"evaluar {ramo}")
