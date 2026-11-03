from pathlib import Path

p = Path.home() / ".claude/skills/banco-evaluaciones/scripts/motor.py"
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:70])
    s = s.replace(a, b)


# ---- parciales
rep('''def construir_items(ramo, ind, temario):
''', '''REGEX_PARCIAL = re.compile(r"reconstruid[oa] de memoria|faltan? (las )?(secciones|preguntas)", re.I)


def motivo_incompleta(ficha, n, ns_prof):
    """Por que la ficha no sirve como verdad de la prueba (None si sirve). `parcial: false` apaga la heuristica."""
    if ficha.get("parcial") is False:
        return None
    if ficha.get("parcial"):
        return "la ficha esta marcada como parcial"
    d = next((str(x) for x in ficha.get("dudas") or [] if REGEX_PARCIAL.search(str(x))), None)
    if d:
        return f"la ficha dice: {d[:120]}"
    if len(ns_prof) >= 2 and n < min(ns_prof) / 2:
        return f"{n} preguntas, menos de la mitad del minimo del profesor ({min(ns_prof)})"
    return None


def construir_items(ramo, ind, temario):
''')
rep('''    evs, sin_mapa = {}, set()
    for i, m in ind["evaluaciones"].items():
        if m["ramo"] != ramo:
            continue
        ev = B.leer_eval(m)
''', '''    evs, sin_mapa, fichas = {}, set(), {}
    for i, m in ind["evaluaciones"].items():
        if m["ramo"] != ramo:
            continue
        ev = fichas[i] = B.leer_eval(m)
''')
rep('''            "items": items}
    data = {"ramo": ramo, "generado"''', '''            "items": items}
    for i, e in evs.items():
        ns = [len(o["items"]) for j, o in evs.items() if j != i and o.get("profesor") == e.get("profesor")]
        e["parcial"] = motivo_incompleta(fichas[i], len(e["items"]), ns)
    data = {"ramo": ramo, "generado"''')
rep('''    if ids != set(data["evaluaciones"]):  # llegaron o se borraron evaluaciones
''', '''    # llegaron o se borraron evaluaciones, o items.json es anterior al campo parcial
    if ids != set(data["evaluaciones"]) or any("parcial" not in e for e in data["evaluaciones"].values()):
''')
rep('''    for i, ev in items["evaluaciones"].items():
        if ids is not None:
            if i not in ids:
                continue
        elif antes_de is not None:
''', '''    for i, ev in items["evaluaciones"].items():
        if ids is not None:  # repetir un pre-registro: exactamente lo que vio, sin filtrar
            if i not in ids:
                continue
        elif ev.get("parcial"):  # una ficha incompleta no es historia del profesor
            continue
        elif antes_de is not None:
''')
rep('''    evs = sorted(items["evaluaciones"].items(), key=lambda x: clave_orden(x[1]))
    S_prog = [u["id"] for u in temario["unidades"] if not u.get("opcional")]
    modelos =''', '''    evs = sorted(((i, e) for i, e in items["evaluaciones"].items() if not e.get("parcial")),
                 key=lambda x: clave_orden(x[1]))
    S_prog = [u["id"] for u in temario["unidades"] if not u.get("opcional")]
    modelos =''')
rep('''            resueltas = {r["evaluacion_id"]: r for r in d["resueltas"] if r["evaluacion_id"] in items["evaluaciones"]}
''', '''            parciales = {i for i, e in items["evaluaciones"].items() if e.get("parcial")}
            resueltas = {r["evaluacion_id"]: r for r in d["resueltas"]
                         if r["evaluacion_id"] in items["evaluaciones"] and r["evaluacion_id"] not in parciales}
''')
rep('''                if i in resueltas or not (ev.get("anio") and ev.get("semestre")):
''', '''                if i in resueltas or i in parciales or not (ev.get("anio") and ev.get("semestre")):
''')
rep('''    otros = [e for i, e in items["evaluaciones"].items() if i != ev_id]
''', '''    otros = [e for i, e in items["evaluaciones"].items() if i != ev_id and not e.get("parcial")]
''')

# ---- resoluciones con correcciones superpuestas
rep('''def resoluciones(ramo):
    fs = sorted((dir_motor(ramo) / "Resueltas").glob("*.json"))
    return sorted((leer(f) for f in fs), key=lambda r: (r["fecha_real"] or r["resuelta"], r["resuelta"]))
''', '''def resoluciones(ramo):
    """Las resoluciones vigentes: si una tiene correcciones, manda la ultima y `original` guarda lo congelado."""
    out = []
    for f in sorted((dir_motor(ramo) / "Resueltas").glob("*.json")):
        r = leer(f)
        cs = sorted((dir_motor(ramo) / "Correcciones").glob(f"{r['id_registro']}--*.json"))
        if cs:
            c = leer(cs[-1])
            r = dict(c["corregida"], original=c["original"],
                     correccion={"fecha": c["fecha"], "motivo": c["motivo"], "n": len(cs)})
        out.append(r)
    return sorted(out, key=lambda r: (r["fecha_real"] or r["resuelta"], r["resuelta"]))
''')

# ---- dominio
rep('''def actualizar_dominio(ramo, ev_id, ev, meta):
''', '''ESCALA_DOMINIO = "preguntas equivalentes: cada pregunta vale 1 x su fraccion en la unidad, sin importar sus puntos"


def actualizar_dominio(ramo, ev_id, ev, meta):
''')
rep('''    d.setdefault("_fuentes", []).append(ev_id)
    escribir(f, d)
    return "actualizado (logrado/posible por unidad, en preguntas equivalentes)"
''', '''    d.setdefault("_fuentes", []).append(ev_id)
    d["_escala"] = ESCALA_DOMINIO
    escribir(f, d)
    return "actualizado (logrado/posible por unidad, en preguntas equivalentes)"


def anotar_dominio(ramo, temario, args):
    """Practica o ensayo: entra en la misma escala que las pruebas, nunca en puntos brutos."""
    if args.unidad not in temario["por_id"]:
        sys.exit(f"Unidad desconocida: {args.unidad}. Hay: {', '.join(temario['por_id'])}.")
    if args.obtenido is None or not args.puntaje or args.puntaje <= 0 or args.obtenido < 0 or not args.motivo:
        sys.exit("Faltan --obtenido, --puntaje (> 0) o --motivo.")
    if args.preguntas <= 0:
        sys.exit("--preguntas debe ser > 0.")
    f = dir_motor(ramo) / "dominio.json"
    d = leer(f, {})
    x = d.setdefault(args.unidad, {})
    x["logrado"] = round(float(x.get("logrado", 0)) + min(args.obtenido, args.puntaje) / args.puntaje * args.preguntas, 4)
    x["posible"] = round(float(x.get("posible", 0)) + args.preguntas, 4)
    d["_escala"] = ESCALA_DOMINIO
    d.setdefault("_practica", []).append({
        "fecha": f"{datetime.now():%Y-%m-%d}", "unidad": args.unidad, "obtenido": args.obtenido,
        "puntaje": args.puntaje, "preguntas": args.preguntas, "motivo": args.motivo})
    escribir(f, d)
    print(f"ok dominio {args.unidad}: {x['logrado']}/{x['posible']} preguntas equivalentes")
''')

# ---- evaluar: separar el calculo de la escritura
a = s.index('def evaluar(ramo, ind, temario, items, ev_id, silencioso=False):')
b = s.index('def postmortem(ramo, temario, r):')
s = s[:a] + '''def calcular_resolucion(ramo, ind, temario, items, ev_id, reg, fecha_real, nota, hechas, dom):
    """Compara el registro congelado con la prueba tal como esta en la ficha. No escribe nada."""
    ev = items["evaluaciones"][ev_id]
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
    sorpresa = [u for u in S if fila["real"].get(u, 0) > 0 and fila["p"][u] < 0.3] + \\
               [u for u in fila["real"] if u not in S]
    sin_mapa = sorted({t for it in ev["items"] for t in unidades_item(it["temas"], temario)[1]})
    prof_ok = bool(reg["profesor"]) and bool(B.parecido(ev.get("profesor"), [reg["profesor"]], 0.6)) and \\
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
    activas = sorted({k for f in reg["factores_central"].values() for k in f})
    return {"id_registro": reg["id"], "evaluacion_id": ev_id, "evaluacion": reg["evaluacion"],
            "periodo": reg["periodo"], "resuelta": datetime.now().isoformat(timespec="seconds"),
            "fecha_real": fecha_real.isoformat() if fecha_real else None, "nota_fecha": nota,
            "emitida": reg["emitida"], "version_modelo": reg["version_modelo"], "profesor": ev.get("profesor"),
            "S": S, "real": {u: round(v, 4) for u, v in fila["real"].items()}, "p": fila["p"], "sh": fila["sh"],
            "metricas": {"brier": brier, "log": me["log"], "cuad": me["cuad"], "top1": me["top1"], "top2": me["top2"]},
            "bases": {b: {"brier": m["brier_prueba"], "cuad": m["cuad"], "top1": m["top1"]} for b, m in mb.items()},
            "fuera_alcance": fuera, "senales": dirs, "activas": activas, "sorpresas": sorpresa, "sin_mapa": sin_mapa,
            "causas": causas, "deriva": der, "dominio": dom}


def evaluar(ramo, ind, temario, items, ev_id, silencioso=False):
    """Resuelve el pre-registro de una prueba recien ingresada. Devuelve la resolucion o None."""
    ev, meta = items["evaluaciones"][ev_id], ind["evaluaciones"][ev_id]
    if ev.get("parcial"):
        if not silencioso:
            print(f"!  {ev_id}: ficha incompleta, no se resuelve ni suma dominio ({ev['parcial']}). "
                  "Ingresa el original; si la ficha si esta completa: corregir ... parcial=no.")
        return None
    dom = actualizar_dominio(ramo, ev_id, ev, meta)  # antes de los retornos: el puntaje puede llegar despues
    if dom.startswith("actualizado"):
        print(f"ok dominio de {ramo} {dom}: {ev_id}")
    hechas = resoluciones(ramo)
    if any(r["evaluacion_id"] == ev_id for r in hechas):
        print(f"=  {ev_id}: ya estaba resuelta; un ingreso nuevo de la misma prueba no la vuelve a resolver "
              "(si los datos estaban mal: motor corregir).")
        return None
    ingresado = fecha_de(B.leer_eval(meta).get("ingresado"))
    reg, fecha_real, nota = buscar_registro(ramo, ev, ingresado)
    if not reg:
        if not silencioso:
            print(f"-  {ev_id}: {nota}")
        return None
    res = calcular_resolucion(ramo, ind, temario, items, ev_id, reg, fecha_real, nota, hechas, dom)
    f = dir_motor(ramo) / "Resueltas" / f"{reg['id']}.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "x", encoding="utf-8") as fh:  # la resolucion tampoco se sobrescribe
        json.dump(res, fh, ensure_ascii=False, indent=1)
    f.chmod(0o444)
    pm = postmortem(ramo, temario, res)
    print(f"ok resuelta {reg['evaluacion']} con el registro {reg['id']}: Brier {res['metricas']['brier']:.3f} "
          f"(uniforme {res['bases']['uniforme']['brier']:.3f}), cuad {res['metricas']['cuad']:.3f} -> {pm}")
    for x in res["deriva"]:
        print(f"!  deriva: {x}")
    return res


def corregir_resolucion(ramo, ind, temario, items, ev_id, motivo):
    """Rehace una resolucion con la ficha de hoy y el mismo registro congelado. Resueltas/ no se toca: la correccion
    es un archivo nuevo e inmutable en Correcciones/, y guarda los valores originales."""
    ev, meta = items["evaluaciones"][ev_id], ind["evaluaciones"][ev_id]
    if ev.get("parcial"):
        sys.exit(f"{ev_id}: la ficha sigue incompleta ({ev['parcial']}); corregirla con eso no sirve.")
    todas = resoluciones(ramo)
    vig = next((r for r in todas if r["evaluacion_id"] == ev_id), None)
    if not vig:
        sys.exit(f"{ev_id}: no tiene resolucion que corregir (usa motor evaluar).")
    rid = vig["id_registro"]
    orig = leer(dir_motor(ramo) / "Resueltas" / f"{rid}.json")
    fecha_real = fecha_de(ev.get("fecha")) or fecha_de(orig["fecha_real"])
    nota = "" if fecha_real else orig["nota_fecha"]
    dom = actualizar_dominio(ramo, ev_id, ev, meta)
    res = calcular_resolucion(ramo, ind, temario, items, ev_id, leer_registro(ramo, rid), fecha_real, nota,
                              [r for r in todas if r["evaluacion_id"] != ev_id], dom)
    res["resuelta"] = orig["resuelta"]
    ahora = datetime.now()
    c = {"corrige": rid, "evaluacion_id": ev_id, "fecha": ahora.isoformat(timespec="seconds"), "motivo": motivo,
         "corregida": res, "original": {k: orig.get(k) for k in ("resuelta", "fecha_real", "real", "metricas", "bases",
                                                                 "deriva", "dominio")}}
    f = dir_motor(ramo) / "Correcciones" / f"{rid}--{ahora:%Y%m%d-%H%M%S}.json"
    escribir_inmutable(f, c)
    n = len(list(f.parent.glob(f"{rid}--*.json")))
    vigente = dict(res, original=c["original"], correccion={"fecha": c["fecha"], "motivo": motivo, "n": n})
    pm = postmortem(ramo, temario, vigente)
    m, om = res["metricas"], orig["metricas"]
    print(f"ok corregida {res['evaluacion']}: Brier {om['brier']:.3f} -> {m['brier']:.3f}, cuad {om['cuad']:.3f} -> "
          f"{m['cuad']:.3f}. Original intacta en Resueltas/. -> {pm}")
    for x in res["deriva"]:
        print(f"!  deriva: {x}")
    return res


''' + s[b:]

# ---- postmortem
rep('''         "- Se evalúa la predicción tal como quedó congelada; las líneas base usan las mismas pruebas que ella.", "",
         "| Modelo | Brier''', '''         "- Se evalúa la predicción tal como quedó congelada; las líneas base usan las mismas pruebas que ella.", ""]
    if r.get("correccion"):
        o = r["original"]
        L += [f"**Resolución corregida** el {r['correccion']['fecha'][:10]}: {r['correccion']['motivo']} "
              f"Valores originales, que siguen en `Resueltas/`: Brier {o['metricas']['brier']:.3f}, "
              f"cuad {o['metricas']['cuad']:.3f}, reparto real {o['real']}.", ""]
    L += ["| Modelo | Brier''')

# ---- hash_global
rep('''        h.update(",".join(sorted(f.name for f in (t.parent / "Resueltas").glob("*.json"))).encode())
''', '''        for carpeta in ("Resueltas", "Correcciones"):
            h.update(",".join(sorted(f.name for f in (t.parent / carpeta).glob("*.json"))).encode())
''')

# ---- tablero
rep('''        L += ["", veredicto(acum, {bn: [r["bases"][bn]["brier"] for r in rs] for bn in BT_BASES}, rng), ""]
''', '''        L += [""]
        for r in rs:
            if r.get("correccion"):
                o = r["original"]["metricas"]
                L += [f"_{r['evaluacion']} {r['periodo'][0]}-{r['periodo'][1]}: corregida el "
                      f"{r['correccion']['fecha'][:10]} ({r['correccion']['motivo']}). Original: Brier {o['brier']:.3f}, "
                      f"cuad {o['cuad']:.3f}._", ""]
        L += [veredicto(acum, {bn: [r["bases"][bn]["brier"] for r in rs] for bn in BT_BASES}, rng), ""]
''')
rep('''    uc = st.get("ultimo_ciclo") or {}
    if uc.get("walk_forward"):
''', '''    L += seccion_manuales(datos)
    uc = st.get("ultimo_ciclo") or {}
    if uc.get("walk_forward"):
''')

# ---- predicciones manuales
rep('''# ------------------------------------------- ciclo, rollback, tablero
''', '''# ------------------------------------------- prediccion manual (por pregunta candidata; no compite con el motor)

def id_manual(evaluacion, periodo):
    return B.slug(f"{periodo} {evaluacion}")


def registrar_manual(ramo, args):
    """--archivo: {"fecha_declarada", "fuente", "nota", "candidatos": [{"id", "bloque", "texto", "p"}]}."""
    e = leer(Path(args.archivo))
    cs = e["candidatos"]
    if len({c["id"] for c in cs}) != len(cs) or not all(0 <= c["p"] <= 1 for c in cs):
        sys.exit("Candidatos invalidos: los id deben ser unicos y cada p estar entre 0 y 1.")
    ahora, fuente = datetime.now(), Path(e["fuente"]) if e.get("fuente") else None
    hay = bool(fuente and fuente.exists())
    i = id_manual(args.evaluacion, args.periodo)
    retro = fecha_de(e["fecha_declarada"]) < ahora.date()
    escribir_inmutable(dir_motor(ramo) / "Manuales" / f"{i}.json", {
        "id": i, "ramo": ramo, "evaluacion": args.evaluacion, "periodo": args.periodo,
        "registrada": ahora.isoformat(timespec="seconds"), "fecha_declarada": e["fecha_declarada"],
        "retroactiva": retro, "fuente": str(fuente) if fuente else None,
        "sha1_fuente": hashlib.sha1(fuente.read_bytes()).hexdigest() if hay else None,
        "modificada_fuente": f"{datetime.fromtimestamp(fuente.stat().st_mtime):%Y-%m-%dT%H:%M:%S}" if hay else None,
        "nota": e.get("nota", ""), "candidatos": cs})
    print(f"ok prediccion manual {i}: {len(cs)} candidatos"
          + (" (RETROACTIVA: registrada despues de la fecha declarada)" if retro else ""))


def brier_manual(cs, aciertos):
    """Brier de los candidatos y el de una prediccion plana con la tasa real (vara exigente: se conoce despues)."""
    xs = [(c["p"], 1 if c["id"] in aciertos else 0) for c in cs]
    n, k = len(xs), sum(o for _, o in xs)
    return {"n": n, "aciertos": k, "brier": sum((p - o) ** 2 for p, o in xs) / n,
            "plana": sum((k / n - o) ** 2 for _, o in xs) / n}


def resolver_manual(ramo, args):
    """--archivo: {"aciertos": [id, ...], "nota"}."""
    i = id_manual(args.evaluacion, args.periodo)
    f = dir_motor(ramo) / "Manuales" / f"{i}.json"
    if not f.exists():
        sys.exit(f"No hay prediccion manual registrada: {f.name}")
    m, e = leer(f), leer(Path(args.archivo))
    aciertos = set(e["aciertos"])
    ajenos = aciertos - {c["id"] for c in m["candidatos"]}
    if ajenos:
        sys.exit(f"Aciertos que no son candidatos: {sorted(ajenos)}")
    bloques = list(dict.fromkeys(c["bloque"] for c in m["candidatos"]))
    r = {"id": i, "evaluacion": m["evaluacion"], "periodo": m["periodo"], "retroactiva": m["retroactiva"],
         "resuelta": datetime.now().isoformat(timespec="seconds"), "aciertos": sorted(aciertos),
         "nota": e.get("nota", ""), "total": brier_manual(m["candidatos"], aciertos),
         "bloques": {b: brier_manual([c for c in m["candidatos"] if c["bloque"] == b], aciertos) for b in bloques}}
    escribir_inmutable(dir_motor(ramo) / "Manuales" / "Resueltas" / f"{i}.json", r)
    for b, x in list(r["bloques"].items()) + [("total", r["total"])]:
        print(f"{b:14} n={x['n']:2} aciertos={x['aciertos']} brier={x['brier']:.3f} plana={x['plana']:.3f}")


def seccion_manuales(datos):
    filas = []
    for d in datos:
        for f in sorted((dir_motor(d["ramo"]) / "Manuales" / "Resueltas").glob("*.json")):
            r = leer(f)
            filas += [f"| {d['ramo']} | {r['evaluacion']} {r['periodo']}{' (retroactiva)' if r['retroactiva'] else ''} | "
                      f"{b} | {x['n']} | {x['aciertos']} | {x['brier']:.3f} | {x['plana']:.3f} |"
                      for b, x in list(r["bloques"].items()) + [("**total**", r["total"])]]
    if not filas:
        return []
    return ["## Predicciones manuales (por pregunta candidata)", "",
            "No se comparan con el motor: miden otra cosa (pregunta, no unidad). La plana usa la tasa real, que "
            "solo se conoce después.", "", "| Ramo | Prueba | Bloque | n | Aciertos | Brier | Plana |",
            "|---|---|---|---|---|---|---|"] + filas + [""]


# ------------------------------------------- ciclo, rollback, tablero
''')

# escribir_inmutable: junto a la resolucion, antes de usarla en corregir
rep('''def calcular_resolucion(ramo, ind, temario, items, ev_id, reg, fecha_real, nota, hechas, dom):
''', '''def escribir_inmutable(f, data):
    f.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(f, "x", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
    except FileExistsError:
        sys.exit(f"Ya existe y no se sobrescribe: {f}")
    f.chmod(0o444)


def calcular_resolucion(ramo, ind, temario, items, ev_id, reg, fecha_real, nota, hechas, dom):
''')

# ---- comandos
rep('''    if args.accion in ("evaluar", "ciclo", "semanal", "tablero", "rollback"):
        return cmd_motor_fase5(args)
    if not args.ramo:
        sys.exit("Falta --ramo.")
    ramo, ind = resolver_ramo(args.ramo)
    temario = leer_temario(ramo)
    if args.accion == "preparar":''', '''    if args.accion in ("evaluar", "corregir", "ciclo", "semanal", "tablero", "rollback"):
        return cmd_motor_fase5(args)
    if not args.ramo:
        sys.exit("Falta --ramo.")
    ramo, ind = resolver_ramo(args.ramo)
    temario = leer_temario(ramo)
    if args.accion in ("manual", "manual-resolver"):
        if not (args.evaluacion and args.periodo and args.archivo):
            sys.exit("Faltan --evaluacion, --periodo (p. ej. 2026-2) o --archivo.")
        (registrar_manual if args.accion == "manual" else resolver_manual)(ramo, args)
    elif args.accion == "dominio":
        anotar_dominio(ramo, temario, args)
    elif args.accion == "preparar":''')
rep('''def cmd_motor_fase5(args):
    if args.accion == "ciclo":''', '''def ids_evaluacion(ramo, items, texto):
    partes = texto.split()
    t, num = B.normalizar_tipo(partes[0]), " ".join(partes[1:])
    ids = [i for i, e in items["evaluaciones"].items() if e["tipo"] == t and (not num or mismo_num(e.get("numero"), num))]
    if not ids:
        sys.exit(f"No hay una prueba «{texto}» de {ramo} en el banco: ingresala primero.")
    return ids


def cmd_motor_fase5(args):
    if args.accion == "ciclo":''')
rep('''        if args.evaluacion:
            partes = args.evaluacion.split()
            t, num = B.normalizar_tipo(partes[0]), " ".join(partes[1:])
            ids = [i for i in ids if items["evaluaciones"][i]["tipo"] == t and
                   (not num or mismo_num(items["evaluaciones"][i].get("numero"), num))]
            if not ids:
                sys.exit(f"No hay una prueba «{args.evaluacion}» de {ramo} en el banco: ingresala primero.")
        if not any(''', '''        if args.evaluacion:
            ids = ids_evaluacion(ramo, items, args.evaluacion)
        if not any(''')
rep('''            ciclo(f"evaluar {ramo}")
''', '''            ciclo(f"evaluar {ramo}")
    elif args.accion == "corregir":
        if not (args.ramo and args.evaluacion and args.motivo):
            sys.exit("Faltan --ramo, --evaluacion o --motivo.")
        ramo, ind = resolver_ramo(args.ramo)
        temario = leer_temario(ramo)
        items, _ = construir_items(ramo, ind, temario)
        resueltas = {r["evaluacion_id"] for r in resoluciones(ramo)}
        ids = [i for i in ids_evaluacion(ramo, items, args.evaluacion) if i in resueltas]
        if len(ids) != 1:
            sys.exit(f"Se esperaba una sola prueba resuelta con ese nombre y hay {len(ids)}: {ids}")
        corregir_resolucion(ramo, ind, temario, items, ids[0], args.motivo)
        ciclo(f"correccion de {ramo}: {args.evaluacion}")
''')
p.write_text(s, encoding="utf-8")

# ---- banco.py
p = Path.home() / ".claude/skills/banco-evaluaciones/scripts/banco.py"
s = p.read_text(encoding="utf-8")
rep('''"fecha", "rendida", "universidad"):''', '''"fecha", "rendida", "parcial", "universidad"):''')
rep('''        v = v.lower() in ("1", "si", "true", "sí") if k == "rendida" else v
''', '''        v = v.lower() in ("1", "si", "true", "sí") if k in ("rendida", "parcial") else v
''')
rep(''' "contenido": "enunciado" | "pauta" | "ambos",
''', ''' "contenido": "enunciado" | "pauta" | "ambos",
 "parcial": true|false (true si el documento no trae la prueba entera: reconstruida de memoria, faltan secciones o preguntas),
''')
rep('''    p.add_argument("accion", choices=("preparar", "senales", "backtest", "evaluar", "ciclo", "semanal", "tablero",
                                      "rollback"))
    p.add_argument("--ramo"); p.add_argument("--evaluacion", help="evaluar: p. ej. 'PEP 1'")
''', '''    p.add_argument("accion", choices=("preparar", "senales", "backtest", "evaluar", "corregir", "dominio", "manual",
                                      "manual-resolver", "ciclo", "semanal", "tablero", "rollback"))
    p.add_argument("--ramo"); p.add_argument("--evaluacion", help="evaluar, corregir, manual: p. ej. 'PEP 1'")
    p.add_argument("--periodo", help="manual: p. ej. 2026-2"); p.add_argument("--archivo", help="manual: JSON")
    p.add_argument("--unidad", help="dominio: p. ej. U2"); p.add_argument("--obtenido", type=float)
    p.add_argument("--puntaje", type=float); p.add_argument("--preguntas", type=float, default=1.0,
                                                            help="dominio: cuantas preguntas equivale (1 por defecto)")
''')
p.write_text(s, encoding="utf-8")
print("parche ok")
