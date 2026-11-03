"""Banco de evaluaciones: archiva y analiza pruebas pasadas y sus pautas, por ramo.

Todo el trabajo pesado (leer PDFs y fotos, extraer preguntas, analizar patrones)
lo hace Gemini desde aqui, fuera del contexto de Claude. Claude solo lee las
salidas compactas de estos comandos.

    python banco.py ingresar [rutas...] [--ramo R --profesor P --tipo T --numero N --anio A --semestre S --rendida]
    python banco.py estado
    python banco.py listar   [--ramo R] [--profesor P]
    python banco.py temas    --ramo R [--profesor P]
    python banco.py buscar   "texto" [--ramo R] [--completo]
    python banco.py ver      <id> [--pregunta N]
    python banco.py analizar --ramo R [--profesor P] [--forzar]
    python banco.py simulacro --ramo R [--profesor P] [--tipo T] [--preguntas 5]
    python banco.py resolver <id> [--pregunta N]
    python banco.py corregir <id> campo=valor ...

Carpeta del banco: BANCO_DIR o ~/OneDrive/BancoEvaluaciones.
"""
import argparse
import base64
import difflib
import hashlib
import json
import mimetypes
import os
import re
import shutil
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BANCO = Path(os.environ.get("BANCO_DIR", Path.home() / "OneDrive" / "BancoEvaluaciones"))
ENTRADA, REVISAR = BANCO / "_Entrada", BANCO / "_Revisar"
INDICE = BANCO / "indice.json"
ENLACES = BANCO / "enlaces.json"  # ramo -> carpeta de otro proyecto que recibe copia de fichas y analisis
SUBIR = "_Subir aqui"
NOTAS_VOZ = Path.home() / "OneDrive" / "NotasDeVoz"
ORQUESTADOR = Path(os.environ.get(
    "ORQUESTADOR_DIR", Path.home() / "OneDrive" / "Documentos" / "Proyecto-ClaudeCode" / "orquestador-multillm"))

IMAGENES = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}
TEXTO = {".txt", ".md", ".tex", ".csv"}
SOPORTADOS = IMAGENES | TEXTO | {".pdf", ".docx"}
MAX_INLINE = 18 * 1024 * 1024  # Gemini acepta ~20 MB por peticion con datos en linea
TIPOS = ["Certamen", "PEP", "Control", "Solemne", "Examen", "Prueba", "Tarea", "Taller", "Quiz", "Ayudantia", "Otro"]
# Nivel gratis: ~20 peticiones/dia POR MODELO, asi que se recorren varios (cada uno es un pozo aparte).
MODELOS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash",
           "gemini-3-flash-preview", "gemini-flash-latest", "gemini-3.1-flash-lite"]


# ---------------------------------------------------------------- utilidades

def normal(s):
    """minusculas, sin tildes ni signos: para comparar nombres."""
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def slug(s):
    return normal(s).replace(" ", "-") or "x"


def limpio(s):
    """Nombre valido para carpeta/archivo de Windows."""
    return re.sub(r'[<>:"/\\|?*]+', "", str(s)).strip(" .") or "Sin nombre"


def sha1(ruta):
    h = hashlib.sha1()
    if ruta.is_dir():
        for p in sorted(ruta.rglob("*")):
            if p.is_file():
                h.update(p.read_bytes())
    else:
        h.update(ruta.read_bytes())
    return h.hexdigest()


def cargar_env():
    env = ORQUESTADOR / ".env"
    if env.exists():
        for linea in env.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*([A-Z_]+)\s*=\s*(.*)", linea)
            if m and m.group(2).strip() and m.group(1) not in os.environ:
                os.environ[m.group(1)] = m.group(2).strip().strip('"').strip("'")


def leer_indice():
    if INDICE.exists():
        return json.loads(INDICE.read_text(encoding="utf-8"))
    return {"version": 1, "evaluaciones": {}, "hashes": {}}


def guardar_indice(ind):
    INDICE.write_text(json.dumps(ind, ensure_ascii=False, indent=1), encoding="utf-8")
    escribir_indice_md(ind)


def ruta_json(meta):
    return BANCO / meta["json"]


def leer_eval(meta):
    return json.loads(ruta_json(meta).read_text(encoding="utf-8"))


def buscar_id(ind, texto):
    """Acepta el id completo o un pedazo unico de el."""
    evs = ind["evaluaciones"]
    if texto in evs:
        return texto
    t = slug(texto)
    hits = [i for i in evs if t in i]
    if len(hits) == 1:
        return hits[0]
    sys.exit(f"'{texto}' calza con {len(hits)} evaluaciones" + (": " + ", ".join(hits[:8]) if hits else ". Usa `listar`."))


# ---------------------------------------------------------------- Gemini

def gemini(partes, json_salida=True, modelo=None, tipo="volumen", intentos=4):
    cargar_env()
    clave = os.environ.get("GEMINI_API_KEY")
    if not clave:
        sys.exit(f"Falta GEMINI_API_KEY en {ORQUESTADOR / '.env'}")
    modelos = list(dict.fromkeys([modelo or os.environ.get("GEMINI_MODEL", MODELOS[0]), *MODELOS]))
    cfg = {"temperature": 0.2}
    if json_salida:
        cfg["responseMimeType"] = "application/json"
    resp = None
    for n, mod in enumerate(modelos, 1):
        for intento in range(1, intentos + 1):
            resp = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent",
                headers={"x-goog-api-key": clave},
                json={"contents": [{"role": "user", "parts": partes}], "generationConfig": cfg},
                timeout=600,
            )
            if resp.status_code == 404:  # modelo retirado: siguiente
                break
            if resp.status_code not in (429, 500, 502, 503, 504):
                resp.raise_for_status()
                data = resp.json()
                registrar_costo(mod, data.get("usageMetadata", {}), tipo)
                cand = data["candidates"][0]
                texto = "".join(p.get("text", "") for p in cand["content"]["parts"] if not p.get("thought"))
                return leer_json(desenvolver(texto)) if json_salida else texto
            if "PerDay" in resp.text:  # cuota diaria del modelo agotada: esperar no sirve
                print(f"    {mod}: cuota diaria agotada")
                break
            if intento < intentos:
                espera = int(re.search(r'"retryDelay": "(\d+)', resp.text).group(1)) + 2 \
                    if '"retryDelay"' in resp.text else 15 * intento
                print(f"    Gemini ocupado ({resp.status_code}); reintento en {espera}s...")
                time.sleep(espera)
        if n < len(modelos):
            print(f"    pruebo con {modelos[n]}...")
    sys.exit("Todos los modelos Gemini agotaron su cuota gratis de hoy (20 peticiones/dia cada uno). "
             "Reintenta manana; lo que quedo en _Entrada se procesa entonces.")


def desenvolver(texto):
    m = re.search(r"```(?:json)?\s*(.*?)```", texto, re.S)
    return m.group(1) if m else texto


LATEX_BFNRT = (r"(?:b(?:eta|ar|inom|ig[gl]?|ig[gl]?[lr]|oldsymbol|f|ullet|ackslash|egin|ot|mod)"
               r"|f(?:rac|orall|lat|rown)"
               r"|n(?:abla|eq|e|u|ot|ewline|eg|mid|ormalsize|i|otin|subseteq)"
               r"|r(?:ight(?:arrow)?|ho|angle|m|ceil|floor|brace|brack|Rightarrow)"
               r"|t(?:heta|au|imes|ext(?:bf|it|rm)?|an|anh|o|ilde|op|frac|riangle|herefore|extstyle|op))"
               r"(?![A-Za-z])")


def leer_json(texto):
    r"""Gemini a veces deja el LaTeX sin escapar dentro del JSON (\lim, \frac). Si falla, se repara:
    \frac, \theta, \nabla... son comandos LaTeX (palabra completa de LATEX_BFNRT), no escapes; en cambio
    "\nla funcion" sigue siendo salto de linea + texto.
    Se repara siempre (no solo si falla), porque \theta o \beta pasan como JSON valido y quedan corruptos."""
    # "\\" ya escapado se respeta; una barra sola que no inicia un escape JSON real se duplica
    valido = re.compile(r'["/]|u[0-9a-fA-F]{4}|(?!' + LATEX_BFNRT + r')[bfnrt]')
    reparado = re.sub(r"\\\\|\\", lambda m: m.group(0) if len(m.group(0)) == 2
                      or valido.match(texto, m.end()) else "\\\\", texto)
    try:
        return json.loads(reparado)
    except json.JSONDecodeError:
        return json.loads(texto)


def registrar_costo(modelo, uso, tipo):
    """Misma bitacora que el orquestador, para que `resumen_costos` y mejorar.py lo cuenten."""
    try:
        with open(ORQUESTADOR / "costs.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": datetime.now().isoformat(timespec="seconds"), "backend": "gemini", "model": modelo,
                "tipo": tipo, "proyecto": "banco-evaluaciones",
                "prompt_tokens": uso.get("promptTokenCount", 0),
                "completion_tokens": uso.get("candidatesTokenCount", 0), "cost_usd_est": 0.0,
            }) + "\n")
    except OSError:
        pass


def partes_de(ruta):
    """Convierte un archivo (o carpeta de fotos de una misma prueba) en partes para Gemini."""
    archivos = sorted(p for p in ruta.rglob("*") if p.is_file()) if ruta.is_dir() else [ruta]
    partes, total = [], 0
    for p in archivos:
        ext = p.suffix.lower()
        if ext == ".docx":
            import docx
            d = docx.Document(p)
            texto = "\n".join(par.text for par in d.paragraphs)
            for t in d.tables:
                texto += "\n" + "\n".join(" | ".join(c.text for c in fila.cells) for fila in t.rows)
            partes.append({"text": f"--- {p.name} ---\n{texto}"})
        elif ext in TEXTO:
            partes.append({"text": f"--- {p.name} ---\n{p.read_text(encoding='utf-8', errors='replace')}"})
        elif ext == ".pdf" or ext in IMAGENES:
            datos = p.read_bytes()
            if total + len(datos) > MAX_INLINE and ext == ".pdf":
                import pymupdf
                texto = "\n".join(pag.get_text() for pag in pymupdf.open(p))
                partes.append({"text": f"--- {p.name} (texto extraido, PDF muy grande) ---\n{texto}"})
                continue
            total += len(datos)
            mime = "application/pdf" if ext == ".pdf" else (mimetypes.guess_type(p.name)[0] or f"image/{ext[1:]}")
            partes.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(datos).decode()}})
    return partes


# ---------------------------------------------------------------- catalogo

def ramos_conocidos(ind):
    ramos = {m["ramo"] for m in ind["evaluaciones"].values()}
    for base in (NOTAS_VOZ, BANCO):
        if base.exists():
            ramos |= {d.name for d in base.iterdir() if d.is_dir() and not d.name.startswith(("_", "."))}
    return sorted(ramos)


def profesores_de(ind, ramo):
    return sorted({m["profesor"] for m in ind["evaluaciones"].values() if m["ramo"] == ramo and m.get("profesor")})


def temas_de(ind, ramo):
    c = Counter(t for m in ind["evaluaciones"].values() if m["ramo"] == ramo for t in m.get("temas", []))
    return [t for t, _ in c.most_common(80)]


def parecido(nombre, opciones, corte=0.72):
    """Devuelve la opcion existente que calza con nombre (tildes/mayusculas/typos), o None."""
    if not nombre:
        return None
    norm = {normal(o): o for o in opciones}
    n = normal(nombre)
    if n in norm:
        return norm[n]
    for k, o in norm.items():  # "Mundaca" calza con "Cristian Mundaca Caceres"
        if n and (n in k.split() or set(n.split()) <= set(k.split())):
            return o
    hit = difflib.get_close_matches(n, list(norm), n=1, cutoff=corte)
    return norm[hit[0]] if hit else None


def nombre_eval(d):
    periodo = f"{d.get('anio') or 's-f'}-{d.get('semestre') or 'x'}"
    num = f" {d['numero']}" if d.get("numero") not in (None, "") else ""
    return limpio(f"{periodo} {d.get('tipo') or 'Otro'}{num} - {d.get('profesor') or 'sin profesor'}")


def normalizar_tipo(t):
    return parecido(t, TIPOS, 0.6) or (str(t).title() if t else "Otro")


# ---------------------------------------------------------------- ingresar

PROMPT_EXTRAER = """Eres un archivador de evaluaciones universitarias (Chile: certamenes, PEP, controles,
solemnes, examenes, tareas, talleres). Lee el documento adjunto y devuelve SOLO un JSON.

Nombre del archivo: "{archivo}"
Ramos que ya existen (usa exactamente uno de estos nombres si corresponde): {ramos}
Profesores conocidos por ramo: {profes}
Temas ya usados en el ramo (reutilizalos con la misma escritura cuando apliquen, crea nuevos solo si no calza ninguno): {temas}
Datos que el usuario ya fijo (respetalos): {fijos}
{nota}
Esquema:
{{
 "ramo": str|null, "profesor": str|null, "universidad": str|null,
 "tipo": "Certamen|PEP|Control|Solemne|Examen|Prueba|Tarea|Taller|Quiz|Ayudantia|Otro",
 "numero": int|null, "anio": int|null, "semestre": 1|2|null, "fecha": "AAAA-MM-DD"|null,
 "contenido": "enunciado" | "pauta" | "ambos",
 "resumen": "2-3 lineas: que evalua y como (tipo de preguntas, extension, ponderacion)",
 "preguntas": [{{
   "n": "1" | "2a" (numeracion tal como aparece),
   "puntaje": str|null,
   "obtenido": str|null (puntaje que obtuvo el alumno en esa pregunta, SOLO si la prueba viene corregida y lo muestra),
   "temas": ["2 a 4 temas cortos y canonicos, p. ej. 'IS-LM', 'elasticidad precio', 'MCO: sesgo por variable omitida'"],
   "tipo_pregunta": "calculo|desarrollo|alternativas|verdadero-falso|demostracion|grafico|ensayo|caso",
   "dificultad": "baja|media|alta",
   "enunciado": "texto completo en Markdown, formulas en LaTeX $...$; describe graficos o tablas; null si el documento es solo pauta",
   "pauta": "solucion/criterios completos tal como vienen en el documento, en Markdown+LaTeX; null si no hay"
 }}],
 "confianza": 0.0-1.0,
 "dudas": ["partes ilegibles o datos que el usuario deberia confirmar"]
}}
Transcribe fielmente (no resumas los enunciados ni las pautas). Si es una foto torcida o
manuscrita, haz tu mejor lectura y anota en "dudas" lo que no se lee. Si el anio o semestre no
aparecen en el documento, deducelos del nombre del archivo o deja null."""


def ingresar(args):
    ind = leer_indice()
    ENTRADA.mkdir(parents=True, exist_ok=True)
    def validos(carpeta):
        return [p for p in sorted(carpeta.iterdir()) if p.is_dir() or p.suffix.lower() in SOPORTADOS]

    if args.rutas:
        items = [(Path(r).resolve(), False, None) for r in args.rutas]  # rutas externas: se copian, no se mueven
    else:
        items = [(p, True, None) for p in validos(ENTRADA)]
        for sub in sorted(BANCO.glob(f"*/{SUBIR}")):  # <Ramo>/_Subir aqui: el ramo ya se sabe
            items += [(p, True, sub.parent.name) for p in validos(sub)]
    if not items:
        print(f"Nada que ingresar. Deja los archivos en {ENTRADA} o en <Ramo>/{SUBIR}")
        return
    base = {k: v for k, v in {
        "ramo": args.ramo, "profesor": args.profesor, "tipo": args.tipo, "numero": args.numero,
        "anio": args.anio, "semestre": args.semestre, "fecha": args.fecha}.items() if v not in (None, "")}
    nuevos = []
    for ruta, mover, ramo_carpeta in items:
        fijos = {"ramo": ramo_carpeta, **base} if ramo_carpeta else base
        if not ruta.exists():
            print(f"x  no existe: {ruta}")
            continue
        h = sha1(ruta)
        if h in ind["hashes"]:
            print(f"=  {ruta.name}: ya estaba (en {ind['hashes'][h]})")
            if mover:  # sacarlo de _Entrada para que no vuelva a aparecer
                REVISAR.mkdir(exist_ok=True)
                shutil.move(str(ruta), str(REVISAR / f"DUPLICADO {ruta.name}"))
            continue
        print(f"-> {ruta.name} ...")
        try:
            nuevos.append(procesar(ind, ruta, mover, h, fijos, args))
        except Exception as e:  # un archivo malo no debe botar la tanda completa
            print(f"x  {ruta.name}: {type(e).__name__}: {e}")
        guardar_indice(ind)
    nuevos = [i for i in nuevos if i]
    if nuevos:  # Fase 5 del motor: si habia una prediccion de esta prueba, se evalua y se aprende de ella
        try:
            import motor
            motor.al_ingresar(nuevos)
        except (SystemExit, Exception) as e:
            print(f"x  motor: {type(e).__name__}: {e} (el ingreso quedo guardado; corre `motor evaluar --ramo R`)")


def procesar(ind, ruta, mover, h, fijos, args):
    ramos = ramos_conocidos(ind)
    ramo_guess = parecido(fijos.get("ramo") or ruta.stem, ramos, 0.5)
    profes = {r: profesores_de(ind, r) for r in ramos if profesores_de(ind, r)}
    prompt = PROMPT_EXTRAER.format(
        archivo=ruta.name, ramos=json.dumps(ramos, ensure_ascii=False),
        profes=json.dumps(profes, ensure_ascii=False),
        temas=json.dumps(temas_de(ind, ramo_guess) if ramo_guess else [], ensure_ascii=False),
        fijos=json.dumps(fijos, ensure_ascii=False),
        nota=f"INSTRUCCIONES DEL USUARIO PARA ESTE DOCUMENTO (prioridad maxima): {args.nota}\n" if getattr(args, "nota", None) else "")
    partes = partes_de(ruta)
    if not partes:
        raise ValueError("no encontre contenido legible")
    d = gemini([{"text": prompt}, *partes], modelo=args.modelo, tipo="volumen")
    d.update(fijos)
    if str(d.get("numero") or "").isdigit():
        d["numero"] = int(d["numero"])

    d["ramo"] = parecido(d.get("ramo"), ramos) or (d.get("ramo") and limpio(d["ramo"]))
    if not d["ramo"]:
        REVISAR.mkdir(exist_ok=True)
        destino = REVISAR / ruta.name
        (shutil.move if mover else copiar)(str(ruta), str(destino))
        print(f"?  no pude deducir el ramo; quedo en _Revisar. Reintenta con --ramo")
        return
    d["profesor"] = parecido(d.get("profesor"), profesores_de(ind, d["ramo"]), 0.8) or d.get("profesor")
    d["tipo"] = normalizar_tipo(d.get("tipo"))
    contenido = d.get("contenido") or "enunciado"

    ev_id, existente = emparejar(ind, d)
    carpeta = BANCO / limpio(d["ramo"])
    (carpeta / "Originales").mkdir(parents=True, exist_ok=True)
    (carpeta / "Fichas").mkdir(exist_ok=True)

    if existente:
        ev = leer_eval(ind["evaluaciones"][ev_id])
        fusionar(ev, d)
        accion = "fusionado con"
    else:
        ev = {k: d.get(k) for k in ("ramo", "profesor", "universidad", "tipo", "numero", "anio", "semestre", "fecha", "resumen")}
        ev.update(preguntas=[], fuentes=[], dudas=[], rendida=False, ingresado=datetime.now().date().isoformat())
        fusionar(ev, d)
        accion = "nuevo"
    ev["rendida"] = ev.get("rendida") or bool(args.rendida)
    ev["revisar"] = (d.get("confianza") or 0) < 0.6 or not d.get("anio")
    nombre = nombre_eval(ev)
    ev["id"] = ev_id or f"{slug(ev['ramo'])}/{slug(nombre)}"

    destino = carpeta / "Originales" / f"{nombre} [{contenido}]{ruta.suffix if ruta.is_file() else ''}"
    k = 2
    while destino.exists():
        destino = destino.with_name(f"{nombre} [{contenido}] ({k}){ruta.suffix if ruta.is_file() else ''}")
        k += 1
    (shutil.move if mover else copiar)(str(ruta), str(destino))
    ev["fuentes"].append({"archivo": destino.relative_to(BANCO).as_posix(), "sha1": h, "contenido": contenido,
                          "original": ruta.name})
    guardar_eval(ind, ev, nombre)
    ind["hashes"][h] = ev["id"]
    n = len(ev["preguntas"])
    marca = "  (revisar: " + "; ".join(ev["dudas"][:2]) + ")" if ev["revisar"] else ""
    print(f"ok {accion}: {ev['id']}  [{contenido}, {n} preguntas]{marca}")
    return ev["id"]


def copiar(origen, destino):
    (shutil.copytree if Path(origen).is_dir() else shutil.copy2)(origen, destino)


def emparejar(ind, d):
    """Una pauta que llega despues se junta con su enunciado (mismo ramo, tipo, numero y periodo)."""
    for i, m in ind["evaluaciones"].items():
        if (m["ramo"] == d["ramo"] and m["tipo"] == d["tipo"] and str(m.get("numero")) == str(d.get("numero"))
                and m.get("anio") == d.get("anio") and m.get("semestre") == d.get("semestre")
                and (not m.get("profesor") or not d.get("profesor")
                     or parecido(d["profesor"], [m["profesor"]], 0.8))):
            return i, True
    return None, False


def fusionar(ev, d):
    for k in ("profesor", "universidad", "fecha", "resumen", "numero", "anio", "semestre"):
        if not ev.get(k) and d.get(k):
            ev[k] = d[k]
    por_n = {normal(p["n"]): p for p in ev["preguntas"]}
    for q in d.get("preguntas") or []:
        q["n"] = str(q.get("n", len(por_n) + 1))
        previa = por_n.get(normal(q["n"]))
        if not previa:
            if q.get("pauta"):
                q["pauta_origen"] = "oficial"
            ev["preguntas"].append(q)
            por_n[normal(q["n"])] = q
            continue
        if q.get("enunciado") and not previa.get("enunciado"):
            previa["enunciado"] = q["enunciado"]
        if q.get("pauta") and (not previa.get("pauta") or previa.get("pauta_origen") == "ia"):
            previa["pauta"], previa["pauta_origen"] = q["pauta"], "oficial"
        for k in ("puntaje", "obtenido", "tipo_pregunta", "dificultad"):
            previa[k] = previa.get(k) or q.get(k)
        previa["temas"] = list(dict.fromkeys((previa.get("temas") or []) + (q.get("temas") or [])))
    ev["dudas"] = list(dict.fromkeys(ev.get("dudas", []) + (d.get("dudas") or [])))


def guardar_eval(ind, ev, nombre=None):
    nombre = nombre or nombre_eval(ev)
    fichas = BANCO / limpio(ev["ramo"]) / "Fichas"
    fichas.mkdir(parents=True, exist_ok=True)
    viejo = ind["evaluaciones"].get(ev["id"])
    js = fichas / f"{nombre}.json"
    if viejo and ruta_json(viejo) != js:  # cambio el nombre (p. ej. llego el profesor en la pauta)
        for ext in (".json", ".md"):
            ruta_json(viejo).with_suffix(ext).unlink(missing_ok=True)
    js.write_text(json.dumps(ev, ensure_ascii=False, indent=1), encoding="utf-8")
    js.with_suffix(".md").write_text(ficha_md(ev), encoding="utf-8")
    pregs = ev["preguntas"]
    ind["evaluaciones"][ev["id"]] = {
        "ramo": ev["ramo"], "profesor": ev.get("profesor"), "tipo": ev["tipo"], "numero": ev.get("numero"),
        "anio": ev.get("anio"), "semestre": ev.get("semestre"), "rendida": ev.get("rendida", False),
        "revisar": ev.get("revisar", False), "n_preguntas": len(pregs),
        "enunciado": any(p.get("enunciado") for p in pregs),
        "pauta": ("oficial" if any(p.get("pauta_origen") == "oficial" for p in pregs)
                  else "ia" if any(p.get("pauta") for p in pregs) else "falta"),
        "temas": list(dict.fromkeys(t for p in pregs for t in p.get("temas") or [])),
        "json": js.relative_to(BANCO).as_posix(),
    }


def ficha_md(ev):
    periodo = f"{ev.get('anio') or 's/f'}-{ev.get('semestre') or '?'}"
    num = f" {ev['numero']}" if ev.get("numero") not in (None, "") else ""
    temas = list(dict.fromkeys(t for p in ev["preguntas"] for t in p.get("temas") or []))
    out = [
        "---", f"id: {ev['id']}", f"ramo: {ev['ramo']}", f"profesor: {ev.get('profesor') or '?'}",
        f"evaluacion: {ev['tipo']}{num} {periodo}", f"temas: {', '.join(temas)}",
        f"fuentes: {', '.join(f['archivo'] for f in ev['fuentes'])}", "---",
        f"# {ev['tipo']}{num} · {ev['ramo']} · {periodo} · {ev.get('profesor') or 'profesor ?'}", "",
    ]
    if ev.get("resumen"):
        out += [f"> {ev['resumen']}", ""]
    if ev.get("dudas"):
        out += ["**Por confirmar:** " + "; ".join(ev["dudas"]), ""]
    for p in ev["preguntas"]:
        cab = [f"P{p['n']}"] + [x for x in (p.get("puntaje"), ", ".join(p.get("temas") or []),
                                            p.get("tipo_pregunta"), p.get("dificultad")) if x]
        out += [f"## {' · '.join(cab)}", "", "**Enunciado**", "", p.get("enunciado") or "_(no disponible)_", ""]
        if p.get("pauta"):
            etiqueta = "Pauta" if p.get("pauta_origen") != "ia" else "Pauta propuesta por IA (no oficial, verificar)"
            out += [f"**{etiqueta}**", "", p["pauta"], ""]
    return "\n".join(out)


def tabla_indice(ind, solo_ramo=None):
    filas = sorted(((i, m) for i, m in ind["evaluaciones"].items() if solo_ramo in (None, m["ramo"])),
                   key=lambda x: (x[1]["ramo"], -(x[1].get("anio") or 0), x[0]))
    out, ramo = [], None
    for i, m in filas:
        if m["ramo"] != ramo:
            ramo = m["ramo"]
            out += ["", f"## {ramo}", "", "| Evaluacion | Profesor | Preg. | Pauta | Temas |", "|---|---|---|---|---|"]
        num = f" {m['numero']}" if m.get("numero") not in (None, "") else ""
        ev = f"{m['tipo']}{num} {m.get('anio') or 's/f'}-{m.get('semestre') or '?'}"
        marca = (" ★" if m.get("rendida") else "") + (" ⚠" if m.get("revisar") else "")
        link = m["json"][:-5] if solo_ramo is None else m["json"][:-5].split("/", 1)[1]
        out.append(f"| [{ev}]({link.replace(' ', '%20')}.md){marca} | {m.get('profesor') or '?'} | "
                   f"{m['n_preguntas']} | {m['pauta']} | {', '.join(m['temas'][:6])} |")
    return out + ["", "★ rendida por ti · ⚠ datos por confirmar"]


def escribir_indice_md(ind):
    out = ["# Banco de evaluaciones", "", "_Generado por banco.py; no editar a mano._", ""] + tabla_indice(ind)
    (BANCO / "INDICE.md").write_text("\n".join(out), encoding="utf-8")


# ---------------------------------------------------------------- enlaces con otros proyectos

def leer_enlaces():
    return json.loads(ENLACES.read_text(encoding="utf-8")) if ENLACES.exists() else {}


def escribir_si_cambia(destino, contenido):
    datos = contenido.encode("utf-8") if isinstance(contenido, str) else contenido
    if destino.exists() and destino.read_bytes() == datos:
        return False
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(datos)
    return True


SINCRONIZADOS = ("ANALISIS*.md", "PREDICCION*.md", "Fichas/*.md", "Simulacros/*.md", "Reconstruidas/*.pdf")


def sincronizar(ind=None, silencioso=False):
    """Copia a cada proyecto enlazado solo lo liviano del ramo (fichas .md, analisis, simulacros, indice y
    las pruebas reconstruidas en PDF). Las fotos y escaneos originales se quedan en el banco."""
    ind = ind or leer_indice()
    for ramo, carpeta in leer_enlaces().items():
        origen, destino = BANCO / limpio(ramo), Path(carpeta)
        if not destino.parent.exists():
            print(f"!  enlace roto para {ramo}: {destino}")
            continue
        cambios = 0
        vistos = set()
        for f in [x for g in SINCRONIZADOS for x in origen.glob(g)]:
            rel = f.relative_to(origen)
            vistos.add(rel.as_posix())
            cambios += escribir_si_cambia(destino / rel, f.read_bytes())
        for f in [x for g in SINCRONIZADOS for x in destino.glob(g)]:
            if f.relative_to(destino).as_posix() not in vistos:  # borrado o renombrado en el banco
                f.unlink(); cambios += 1
        cab = [f"# Banco de evaluaciones · {ramo}", "",
               f"_Copia automatica desde `{origen}` (banco.py). No editar aqui: se sobrescribe._",
               "PDFs originales y pautas escaneadas: en `Originales/` del banco. Consultas: skill `banco-evaluaciones`.", ""]
        cambios += escribir_si_cambia(destino / "INDICE.md", "\n".join(cab + tabla_indice(ind, ramo)))
        if cambios and not silencioso:
            print(f"<> {ramo}: {cambios} archivo(s) actualizados en {destino}")


def cmd_enlazar(args):
    ind = leer_indice()
    ramo = parecido(args.ramo, ramos_conocidos(ind), 0.5) or args.ramo
    destino = Path(args.carpeta).resolve()
    if not destino.parent.exists():
        sys.exit(f"No existe la carpeta padre: {destino.parent}")
    enl = leer_enlaces(); enl[ramo] = str(destino)
    ENLACES.write_text(json.dumps(enl, ensure_ascii=False, indent=1), encoding="utf-8")
    (BANCO / limpio(ramo) / SUBIR).mkdir(parents=True, exist_ok=True)
    print(f"ok {ramo} -> {destino}\n   Sube archivos a: {BANCO / limpio(ramo) / SUBIR}")
    sincronizar(ind)


# ---------------------------------------------------------------- consultas (sin LLM)

def filtrar(ind, ramo=None, profesor=None):
    evs = ind["evaluaciones"]
    if ramo:
        r = parecido(ramo, {m["ramo"] for m in evs.values()}, 0.5)
        if not r:
            sys.exit(f"No hay evaluaciones de '{ramo}'. Ramos: {', '.join(sorted({m['ramo'] for m in evs.values()})) or '(ninguno)'}")
        evs = {i: m for i, m in evs.items() if m["ramo"] == r}
    if profesor:
        p = parecido(profesor, {m.get("profesor") for m in evs.values() if m.get("profesor")}, 0.6)
        evs = {i: m for i, m in evs.items() if p and m.get("profesor") == p}
    return evs


def cmd_estado(args):
    ind = leer_indice()
    por_ramo = defaultdict(list)
    for m in ind["evaluaciones"].values():
        por_ramo[m["ramo"]].append(m)
    pendientes = [p.name for p in ENTRADA.iterdir()] if ENTRADA.exists() else []
    revisar = [p.name for p in REVISAR.iterdir()] if REVISAR.exists() else []
    print(f"Banco: {BANCO}")
    for r, ms in sorted(por_ramo.items()):
        profs = Counter(m.get("profesor") or "?" for m in ms)
        print(f"- {r}: {len(ms)} evals, {sum(m['n_preguntas'] for m in ms)} preguntas | "
              f"pauta oficial {sum(m['pauta'] == 'oficial' for m in ms)}, ia {sum(m['pauta'] == 'ia' for m in ms)}, "
              f"sin pauta {sum(m['pauta'] == 'falta' for m in ms)} | profes: "
              + ", ".join(f"{p} ({n})" for p, n in profs.most_common())
              + (" | ANALISIS.md" if (BANCO / limpio(r) / "ANALISIS.md").exists() else ""))
    malos = [i for i, m in ind["evaluaciones"].items() if m.get("revisar")]
    if malos:
        print("Por confirmar: " + ", ".join(malos))
    if pendientes:
        print(f"En _Entrada sin procesar: {len(pendientes)} ({', '.join(pendientes[:5])})")
    if revisar:
        print(f"En _Revisar (sin ramo): {', '.join(revisar[:5])}")
    if not ind["evaluaciones"] and not pendientes:
        print("(vacio) Deja PDFs/fotos/Word en _Entrada y corre `ingresar`.")
    try:
        import motor
        for x in motor.lineas_estado():
            print(x)
    except (SystemExit, Exception) as e:
        print(f"x  motor: {type(e).__name__}: {e}")


def cmd_listar(args):
    evs = filtrar(leer_indice(), args.ramo, args.profesor)
    for i, m in sorted(evs.items(), key=lambda x: (x[1]["ramo"], -(x[1].get("anio") or 0))):
        marca = ("★" if m.get("rendida") else "") + ("⚠" if m.get("revisar") else "")
        print(f"{i}{marca} | {m['n_preguntas']}p | pauta:{m['pauta']} | {', '.join(m['temas'][:5])}")
    if not evs:
        print("(sin resultados)")


def conteo_temas(ind, evs):
    """tema -> [(id, n pregunta, profesor, periodo)] leyendo las fichas (preciso por pregunta)."""
    c = defaultdict(list)
    for i, m in evs.items():
        for p in leer_eval(m)["preguntas"]:
            for t in p.get("temas") or []:
                c[t].append((i, p["n"], m.get("profesor") or "?", f"{m.get('anio') or '?'}-{m.get('semestre') or '?'}"))
    return sorted(c.items(), key=lambda x: (-len({a[0] for a in x[1]}), x[0]))


def cmd_temas(args):
    ind = leer_indice()
    evs = filtrar(ind, args.ramo, args.profesor)
    total = len(evs)
    print(f"{total} evaluaciones. tema | aparece en | preguntas | profesores | periodos")
    for t, usos in conteo_temas(ind, evs):
        ids = {u[0] for u in usos}
        print(f"{t} | {len(ids)}/{total} | {len(usos)} | {', '.join(sorted({u[2] for u in usos}))} | "
              f"{', '.join(sorted({u[3] for u in usos}))}")


def cmd_buscar(args):
    ind = leer_indice()
    evs = filtrar(ind, args.ramo, args.profesor)
    palabras = normal(args.texto).split()
    hits = 0
    for i, m in evs.items():
        for p in leer_eval(m)["preguntas"]:
            blob = normal(" ".join([*(p.get("temas") or []), p.get("enunciado") or "", p.get("pauta") or ""]))
            if all(w in blob for w in palabras):
                hits += 1
                if args.completo:
                    print(f"=== {i} P{p['n']} ===\n{p.get('enunciado') or ''}\n--- pauta ---\n{p.get('pauta') or '(sin pauta)'}\n")
                else:
                    extracto = re.sub(r"\s+", " ", p.get("enunciado") or "")[:160]
                    print(f"{i} P{p['n']} [{', '.join(p.get('temas') or [])}] {extracto}")
    print(f"({hits} preguntas)")


def cmd_ver(args):
    ind = leer_indice()
    i = buscar_id(ind, args.id)
    m = ind["evaluaciones"][i]
    if not args.pregunta:
        print(ruta_json(m).with_suffix(".md").read_text(encoding="utf-8"))
        return
    ev = leer_eval(m)
    for p in ev["preguntas"]:
        if normal(p["n"]) == normal(args.pregunta):
            print(f"## {i} P{p['n']} · {', '.join(p.get('temas') or [])}\n\n{p.get('enunciado') or ''}\n\n"
                  f"**Pauta ({p.get('pauta_origen') or 'falta'})**\n\n{p.get('pauta') or '(sin pauta)'}")
            return
    sys.exit(f"No hay P{args.pregunta}. Preguntas: {', '.join(p['n'] for p in ev['preguntas'])}")


# ---------------------------------------------------------------- analisis (Gemini)

def material(ind, evs, con_pauta=True):
    bloques = []
    for i, m in sorted(evs.items(), key=lambda x: (x[1].get("anio") or 0, x[1].get("semestre") or 0)):
        ev = leer_eval(m)
        b = [f"### {i} | {ev['tipo']} {ev.get('numero') or ''} | {ev.get('anio')}-{ev.get('semestre')} | "
             f"prof. {ev.get('profesor') or '?'}" + (" | RENDIDA POR EL ALUMNO" if ev.get("rendida") else "")]
        for p in ev["preguntas"]:
            b.append(f"P{p['n']} ({p.get('puntaje') or '?'} | {', '.join(p.get('temas') or [])} | "
                     f"{p.get('tipo_pregunta')} | {p.get('dificultad')}): {p.get('enunciado') or ''}")
            if con_pauta and p.get("pauta"):
                b.append(f"  PAUTA ({p.get('pauta_origen')}): {p['pauta']}")
        bloques.append("\n".join(b))
    return "\n\n".join(bloques)


PROMPT_ANALISIS = """Eres un tutor universitario que prepara a un alumno para su proxima evaluacion de {ramo}{prof}.
Abajo estan TODAS las evaluaciones pasadas archivadas (enunciados y pautas) y un conteo exacto de temas
ya calculado. Escribe en Markdown, en espanol, conciso y accionable:

## Que se evalua siempre
Tabla: tema | frecuencia (usa el conteo dado, no lo inventes) | como lo preguntan | ultima vez.
## Estilo del profesor
Por profesor: tipo de pregunta preferido, extension, nivel de formalidad matematica, trampas habituales,
que exige la pauta para dar puntaje completo (lo que descuenta).
## Preguntas que se repiten
Ejercicios casi identicos entre anios (cita ids y P#), y como varian.
## Prioridades de estudio
Lista ordenada (probabilidad de aparecer x puntaje), con los ejercicios del banco que conviene hacer para cada una.
## Errores tipicos segun las pautas
{extra}
Cita siempre la evaluacion como `id P#` para que el alumno pueda abrirla. No inventes datos que no esten abajo.

CONTEO DE TEMAS (evaluaciones donde aparece / total):
{conteo}

EVALUACIONES:
{material}"""


def cmd_analizar(args):
    ind = leer_indice()
    evs = filtrar(ind, args.ramo, args.profesor)
    if not evs:
        sys.exit("Sin evaluaciones para analizar.")
    ramo = next(iter(evs.values()))["ramo"]
    prof = next(iter(evs.values())).get("profesor") if args.profesor else None
    destino = BANCO / limpio(ramo) / (f"ANALISIS - {limpio(prof)}.md" if prof else "ANALISIS.md")
    firma = hashlib.sha1(json.dumps(sorted((i, ruta_json(m).stat().st_mtime) for i, m in evs.items())).encode()).hexdigest()[:12]
    if destino.exists() and not args.forzar and f"firma: {firma}" in destino.read_text(encoding="utf-8")[:300]:
        print(f"Sin cambios desde el ultimo analisis: {destino}")
        return
    conteo = "\n".join(f"- {t}: {len({u[0] for u in usos})}/{len(evs)}" for t, usos in conteo_temas(ind, evs))
    rendidas = [i for i, m in evs.items() if m.get("rendida")]
    extra = ("## Como te fue a ti\nEn las evaluaciones RENDIDAS POR EL ALUMNO, contrasta con la pauta y di que reforzar."
             if rendidas else "")
    print(f"Analizando {len(evs)} evaluaciones de {ramo} con Gemini...")
    texto = gemini([{"text": PROMPT_ANALISIS.format(
        ramo=ramo, prof=f" con {prof}" if prof else "", conteo=conteo, extra=extra,
        material=material(ind, evs))}], json_salida=False, modelo=args.modelo, tipo="analisis")
    cab = (f"---\nfirma: {firma}\nevaluaciones: {len(evs)}\ngenerado: {datetime.now():%Y-%m-%d %H:%M}\n---\n"
           f"# Analisis de evaluaciones · {ramo}{' · ' + prof if prof else ''}\n\n")
    destino.write_text(cab + texto, encoding="utf-8")
    print(f"ok {destino}  ({len(texto.splitlines())} lineas)")


PROMPT_SIMULACRO = """Crea un simulacro de {tipo} de {ramo}{prof} con {n} preguntas, en el mismo estilo, extension,
dificultad y distribucion de temas que las evaluaciones reales de abajo (prioriza los temas mas frecuentes;
no copies preguntas textuales, cambia datos y contexto). Formato Markdown + LaTeX:
# Simulacro ...
(instrucciones y puntajes como en las reales)
## P1 ... ## P{n}
Luego una seccion final `# Pauta` con la solucion completa y criterios de puntaje de cada pregunta,
al estilo de las pautas reales.

EVALUACIONES REALES:
{material}"""


def cmd_simulacro(args):
    ind = leer_indice()
    evs = filtrar(ind, args.ramo, args.profesor)
    if args.tipo:
        t = normalizar_tipo(args.tipo)
        evs = {i: m for i, m in evs.items() if m["tipo"] == t} or evs
    if not evs:
        sys.exit("Sin evaluaciones de referencia.")
    ramo = next(iter(evs.values()))["ramo"]
    prof = next(iter(evs.values())).get("profesor") if args.profesor else None
    print(f"Generando simulacro con {len(evs)} evaluaciones de referencia...")
    texto = gemini([{"text": PROMPT_SIMULACRO.format(
        tipo=args.tipo or "evaluacion", ramo=ramo, prof=f" (profesor {prof})" if prof else "",
        n=args.preguntas, material=material(ind, evs))}], json_salida=False, modelo=args.modelo, tipo="simulacro")
    carpeta = BANCO / limpio(ramo) / "Simulacros"
    carpeta.mkdir(parents=True, exist_ok=True)
    destino = carpeta / f"Simulacro {datetime.now():%Y-%m-%d %H%M}{' - ' + limpio(prof) if prof else ''}.md"
    destino.write_text(texto, encoding="utf-8")
    print(f"ok {destino}")


PROMPT_RESOLVER = """Resuelve estas preguntas de {ramo} como lo haria una pauta oficial: desarrollo completo,
resultado final destacado y criterios de puntaje. Markdown + LaTeX. Devuelve SOLO un JSON
{{"P<n>": "solucion", ...}} con una entrada por pregunta.
{contexto}
PREGUNTAS:
{preguntas}"""


def cmd_resolver(args):
    ind = leer_indice()
    i = buscar_id(ind, args.id)
    m = ind["evaluaciones"][i]
    ev = leer_eval(m)
    objetivo = [p for p in ev["preguntas"] if p.get("enunciado") and not p.get("pauta")
                and (not args.pregunta or normal(p["n"]) == normal(args.pregunta))]
    if not objetivo:
        print("Todas esas preguntas ya tienen pauta.")
        return
    # Las pautas oficiales del mismo ramo sirven de ejemplo de estilo y notacion
    otras = {j: x for j, x in filtrar(ind, ev["ramo"]).items() if x["pauta"] == "oficial" and j != i}
    contexto = ("EJEMPLOS DE PAUTAS OFICIALES DEL RAMO (imita notacion y criterios):\n" + material(ind, dict(list(otras.items())[:4]))
                if otras else "")
    sol = gemini([{"text": PROMPT_RESOLVER.format(
        ramo=ev["ramo"], contexto=contexto,
        preguntas="\n\n".join(f"P{p['n']}: {p['enunciado']}" for p in objetivo))}], modelo=args.modelo, tipo="complejo")
    for p in objetivo:
        s = sol.get(f"P{p['n']}") or sol.get(p["n"])
        if s:
            p["pauta"], p["pauta_origen"] = s, "ia"
    guardar_eval(ind, ev)
    guardar_indice(ind)
    print(f"ok pauta IA en {sum(1 for p in objetivo if p.get('pauta'))} preguntas de {i}. "
          f"Marcada como no oficial; verifica las dificiles.")


def cmd_corregir(args):
    ind = leer_indice()
    i = buscar_id(ind, args.id)
    ev = leer_eval(ind["evaluaciones"][i])
    viejo = dict(ind["evaluaciones"][i])
    for par in args.cambios:
        k, _, v = par.partition("=")
        if k not in ("ramo", "profesor", "tipo", "numero", "anio", "semestre", "fecha", "rendida", "universidad"):
            sys.exit(f"Campo no editable: {k}")
        v = int(v) if k in ("anio", "semestre") and v.isdigit() else v
        v = v.lower() in ("1", "si", "true", "sí") if k == "rendida" else v
        v = normalizar_tipo(v) if k == "tipo" else v
        ev[k] = v
    ev["revisar"] = False
    del ind["evaluaciones"][i]
    nuevo_id = f"{slug(ev['ramo'])}/{slug(nombre_eval(ev))}"
    if ev["ramo"] != viejo["ramo"]:  # mover originales al ramo nuevo
        dest = BANCO / limpio(ev["ramo"]) / "Originales"
        dest.mkdir(parents=True, exist_ok=True)
        for f in ev["fuentes"]:
            nueva = dest / Path(f["archivo"]).name
            shutil.move(str(BANCO / f["archivo"]), str(nueva))
            f["archivo"] = nueva.relative_to(BANCO).as_posix()
    for ext in (".json", ".md"):
        (BANCO / viejo["json"]).with_suffix(ext).unlink(missing_ok=True)
    ev["id"] = nuevo_id
    guardar_eval(ind, ev)
    ind["hashes"] = {h: (nuevo_id if v == i else v) for h, v in ind["hashes"].items()}
    guardar_indice(ind)
    print(f"ok {i} -> {nuevo_id}")


# ---------------------------------------------------------------- CLI

# ---------------------------------------------------------------- pruebas reconstruidas en PDF

HTML_PDF = """<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}],throwOnError:false}})"></script>
<style>@page{{size:letter;margin:2cm 2.2cm}} body{{font:11.5pt/1.5 Georgia,'Times New Roman',serif;color:#111}}
h1{{font-size:16pt;margin:0}} .sub{{color:#444;margin:.3em 0 1.4em;border-bottom:2px solid #111;padding-bottom:.5em}}
h2{{font-size:13pt;margin:1.5em 0 .4em;text-transform:uppercase;letter-spacing:.04em}}
.preg{{margin:.8em 0 1.1em}} .n{{font-weight:bold}} .pts{{color:#555;font-style:italic}}
.preg p{{margin:.3em 0}} table{{border-collapse:collapse;margin:.5em 0}} td,th{{border:1px solid #888;padding:3px 8px}}
.nota{{font-size:8.5pt;color:#777;margin-top:2.5em;border-top:1px solid #ccc;padding-top:.4em}}</style>
</head><body>{cuerpo}</body></html>"""


def md_con_formulas(texto):
    """Markdown -> HTML sin que el Markdown rompa el LaTeX ($x_1$ no debe volverse cursiva)."""
    import html
    import markdown
    formulas = []

    def guardar(m):
        formulas.append(m.group(0))
        return f"@@F{len(formulas) - 1}@@"
    protegido = re.sub(r"\$\$.+?\$\$|\$[^$\n]+?\$", guardar, texto or "", flags=re.S)
    out = markdown.markdown(protegido, extensions=["tables"])
    return re.sub(r"@@F(\d+)@@", lambda m: html.escape(formulas[int(m.group(1))]), out)


def navegador():
    for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
        if Path(p).exists():
            return p
    sys.exit("No encontre Edge ni Chrome para imprimir el PDF.")


def cmd_pdf(args):
    """Rearma cada evaluacion solo con sus enunciados (sin pauta ni desarrollo) y la imprime a PDF."""
    import subprocess
    import tempfile
    ind = leer_indice()
    ids = [buscar_id(ind, args.id)] if args.id else list(filtrar(ind, args.ramo, args.profesor))
    for i in ids:
        meta = ind["evaluaciones"][i]
        ev = leer_eval(meta)
        num = f" {ev['numero']}" if ev.get("numero") not in (None, "") else ""
        titulo = f"{ev['tipo']}{num} · {ev['ramo']}"
        periodo = f"{ev.get('anio') or 's/f'}-{ev.get('semestre') or '?'}"
        cuerpo = [f"<h1>{titulo}</h1>",
                  f"<div class='sub'>Profesor {ev.get('profesor') or '?'} · Semestre {periodo}</div>"]
        seccion = None
        for p in ev["preguntas"]:
            n = str(p.get("n") or "")
            m = re.match(r"([A-Za-zÁÉÍÓÚáéíóúñÑ]+)\s*(.*)", n)  # "Comente 2" -> seccion Comente
            if m and m.group(1).lower() != seccion:
                seccion = m.group(1).lower()
                cuerpo.append(f"<h2>{m.group(1)}</h2>")
            etiqueta = n if m else f"{n}."
            pts = f" <span class='pts'>({p['puntaje']})</span>" if p.get("puntaje") else ""
            cuerpo.append(f"<div class='preg'><span class='n'>{etiqueta}</span>{pts}"
                          f"{md_con_formulas(p.get('enunciado') or '_(enunciado no disponible)_')}</div>")
        cuerpo.append(f"<div class='nota'>Reconstruida desde fotos por banco.py ({datetime.now():%Y-%m-%d}). "
                      "Transcripcion automatica: verificar contra el original si algo no calza.</div>")
        destino = BANCO / limpio(ev["ramo"]) / "Reconstruidas" / f"{Path(meta['json']).stem}.pdf"
        destino.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            html_f = Path(tmp) / "prueba.html"
            html_f.write_text(HTML_PDF.format(titulo=titulo, cuerpo="\n".join(cuerpo)), encoding="utf-8")
            subprocess.run([navegador(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            "--virtual-time-budget=20000", f"--user-data-dir={tmp}",
                            f"--print-to-pdf={destino}", html_f.as_uri()],
                           capture_output=True, timeout=120)
        print(f"ok {destino}" if destino.exists() else f"x  no se genero el PDF de {i}")


def main():
    ap = argparse.ArgumentParser(description="Banco de evaluaciones")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def filtros(p, ramo_obligatorio=False):
        p.add_argument("--ramo", required=ramo_obligatorio)
        p.add_argument("--profesor")

    p = sub.add_parser("ingresar")
    p.add_argument("rutas", nargs="*")
    filtros(p)
    for k in ("tipo", "numero", "anio", "semestre"):
        p.add_argument(f"--{k}", type=int if k in ("anio", "semestre") else str)
    p.add_argument("--fecha", help="AAAA-MM-DD en que se rindio (si el documento no la trae)")
    p.add_argument("--rendida", action="store_true", help="la rendiste tu (su analisis la destaca)")
    p.add_argument("--nota", help="instruccion extra para Gemini, p. ej. 'ignora el desarrollo a lapiz'")
    p.add_argument("--modelo")
    p.set_defaults(f=ingresar)

    sub.add_parser("estado").set_defaults(f=cmd_estado)
    p = sub.add_parser("listar"); filtros(p); p.set_defaults(f=cmd_listar)
    p = sub.add_parser("temas"); filtros(p); p.set_defaults(f=cmd_temas)
    p = sub.add_parser("buscar"); p.add_argument("texto"); filtros(p)
    p.add_argument("--completo", action="store_true"); p.set_defaults(f=cmd_buscar)
    p = sub.add_parser("ver"); p.add_argument("id"); p.add_argument("--pregunta"); p.set_defaults(f=cmd_ver)
    p = sub.add_parser("analizar"); filtros(p, True); p.add_argument("--forzar", action="store_true")
    p.add_argument("--modelo"); p.set_defaults(f=cmd_analizar)
    p = sub.add_parser("simulacro"); filtros(p, True); p.add_argument("--tipo")
    p.add_argument("--preguntas", type=int, default=5); p.add_argument("--modelo"); p.set_defaults(f=cmd_simulacro)
    p = sub.add_parser("resolver"); p.add_argument("id"); p.add_argument("--pregunta")
    p.add_argument("--modelo"); p.set_defaults(f=cmd_resolver)
    p = sub.add_parser("corregir"); p.add_argument("id"); p.add_argument("cambios", nargs="+")
    p.set_defaults(f=cmd_corregir)
    p = sub.add_parser("enlazar"); p.add_argument("--ramo", required=True); p.add_argument("carpeta")
    p.set_defaults(f=cmd_enlazar)
    sub.add_parser("sincronizar").set_defaults(f=lambda a: sincronizar())
    p = sub.add_parser("pdf"); p.add_argument("id", nargs="?"); filtros(p); p.set_defaults(f=cmd_pdf)

    # motor de prediccion (motor.py; diseno en el proyecto de metodologia, datos/motor-predicciones/)
    p = sub.add_parser("predecir", help="P(unidad entra), puntos esperados y plan de estudio")
    p.add_argument("--ramo", required=True); p.add_argument("--evaluacion", required=True)
    p.add_argument("--fecha", required=True, help="AAAA-MM-DD"); p.add_argument("--profesor")
    p.add_argument("--alcance", help="unidades que entran, p. ej. U1,U2 (manda sobre el calendario)")
    p.add_argument("--entra", help="unidades que el profesor dijo que entran"); p.add_argument("--no-entra")
    p.add_argument("--provisional", action="store_true", help="la fecha no es oficial")
    p.add_argument("--semilla", type=int, default=7); p.add_argument("--corridas", type=int)
    p.set_defaults(f=lambda a: __import__("motor").cmd_predecir(a))
    p = sub.add_parser("motor", help="insumos, backtest y aprendizaje continuo del motor")
    p.add_argument("accion", choices=("preparar", "senales", "backtest", "evaluar", "ciclo", "semanal", "tablero",
                                      "rollback"))
    p.add_argument("--ramo"); p.add_argument("--evaluacion", help="evaluar: p. ej. 'PEP 1'")
    p.add_argument("--version", help="rollback: p. ej. 1.0"); p.add_argument("--motivo")
    p.add_argument("--modelo"); p.add_argument("--semilla", type=int, default=7)
    p.add_argument("--corridas", type=int, help="backtest: corridas por pronostico (2000 por defecto)")
    p.set_defaults(f=lambda a: __import__("motor").cmd_motor(a))

    args = ap.parse_args()
    BANCO.mkdir(parents=True, exist_ok=True)
    args.f(args)
    if args.cmd in ("ingresar", "analizar", "simulacro", "resolver", "corregir", "pdf", "predecir"):
        sincronizar()  # los proyectos enlazados quedan al dia sin pedirlo


if __name__ == "__main__":
    main()
