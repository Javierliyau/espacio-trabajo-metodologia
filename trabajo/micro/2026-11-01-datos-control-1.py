# Reemplaza la ficha del Control 1 de Micro por la prueba real, migra el dominio y prepara la prediccion manual.
# Uso: python este.py ficha | dominio | manual-json. Respeta BANCO_DIR (para probar con una copia).
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path.home() / ".claude/skills/banco-evaluaciones/scripts"))
import banco as B
import motor as M

RAMO, ID = "Microeconomía II", "microeconomia-ii/2026-2-control-1-mundaca"
AQUI = Path(__file__).parent
CARPETA = "Microeconomía II/Originales/2026-2 Control 1 - Mundaca [corregido]"
U1 = ["monopolio", "poder de mercado"]
U2 = ["discriminación de precios"]
PIE, CP = "pérdida irrecuperable de eficiencia", "competencia perfecta"

PREGUNTAS = [
    ("Comente 1", 5, 5, U1, "verdadero falso", "media",
     "Un monopolista que enfrenta un aumento en el costo de producción de cada unidad puede mantener su cantidad óptima "
     "sin modificaciones, puesto que su poder de mercado le permite fijar libremente el precio de venta.",
     "Falso. Sube el CMg, y el óptimo $IMg = CMg$ se mueve a menos cantidad y más precio."),
    ("Comente 2", 5, 1, U2, "verdadero falso", "media",
     "En el diseño de una tarifa en dos partes óptima con consumidores idénticos, la empresa fija el precio por unidad "
     "equivalente a su costo medio.",
     "Falso. $p = CMg$ y el cargo fijo $T$ es el excedente del consumidor a ese precio: produce la cantidad eficiente y "
     "se queda con todo el excedente."),
    ("Comente 3", 5, 1, U2, "verdadero falso", "alta",
     "Una empresa monopolista comienza a aplicar discriminación de precios de tercer grado, cobrando un precio menor a un "
     "grupo de consumidores y uno mayor a otro. Si esta estrategia aumenta el excedente total de los consumidores, "
     "entonces constituye una mejora en el sentido de Pareto.",
     "Falso. Pareto exige que nadie empeore, y el grupo al que le sube el precio empeora. Que suba el EC total es una "
     "comparación agregada."),
    ("Comente 4", 5, 5, ["monopolio", PIE], "verdadero falso", "baja",
     "La pérdida irrecuperable de eficiencia generada por un monopolio se debe a que este produce una cantidad inferior a "
     "la socialmente eficiente, dejando de realizar intercambios que habrían generado beneficios para la sociedad.",
     "Verdadero. $Q_m < Q_{CP}$: se dejan de hacer intercambios en que la disposición a pagar supera al costo marginal."),
    ("Desarrollo 1", 10, 3, U2 + [CP], "desarrollo", "alta",
     "Detalle la paradoja del primer grado en la teoría de la discriminación de precios en relación con la competencia "
     "perfecta. Explique el rol del poder de mercado extremo en este contexto y la consecuencia analítica que contradice "
     "la crítica habitual a la ineficiencia de las estructuras monopólicas.",
     "Con discriminación perfecta se vende hasta $P = CMg$ en la última unidad: $Q = Q_{CP}$, $PIE = 0$, mismo ES que en "
     "CP, pero $EC = 0$. El poder de mercado máximo da el resultado eficiente: la ineficiencia viene del precio único "
     "($IMg < P$), no del poder de mercado en sí. Eficiencia no es equidad."),
    ("Desarrollo 2", 10, 7, ["índice de Lerner", "elasticidad precio de la demanda", "poder de mercado"], "desarrollo",
     "media", "Explique la relación entre elasticidad de demanda y poder de mercado del monopolista. (Pista: Lerner)",
     "$IMg = P(1 - 1/|\\varepsilon|)$ y $L = (P - CMg)/P = 1/|\\varepsilon|$. Con $|\\varepsilon| < 1$, $IMg < 0$: no se "
     "opera en el tramo inelástico. Límite: $|\\varepsilon| \\to \\infty \\Rightarrow L \\to 0$ y $P = CMg$."),
    ("Matemático 1", 20, 20, ["monopolio", "equilibrio de monopolio", PIE, CP], "calculo", "media",
     "El único proveedor de servicios de internet de banda ancha en una localidad aislada tiene una función de costes "
     "totales igual a $c(q) = 2{,}5q^2$. La demanda por conexiones a internet en esta localidad está dada por "
     "$q(p) = 60 - \\frac{p}{5}$. a) Obtenga todos los elementos del equilibrio del monopolista. b) Calcule la pérdida "
     "eficiencia que sufre esta economía. En específico señale cómo varía el precio y cantidad de equilibrio y los "
     "excedentes de consumidor, productor y social respecto de la situación de competencia perfecta. c) Grafique ambos "
     "apartados en un mismo gráfico.",
     "Chequeo de cierre: $ES_{CP} - ES_m = PIE$. Resolución comentada en "
     "`datos/material/microeconomia-ii/2026-11-01-feedback-control-1.md`."),
]


def ficha():
    ind = B.leer_indice()
    ev = B.leer_eval(ind["evaluaciones"][ID])
    fuentes = [f for f in ev["fuentes"] if "[corregido]" not in f["archivo"]]
    for n in range(1, 6):
        rel = f"{CARPETA}/p{n}.jpg"
        h = hashlib.sha1((B.BANCO / rel).read_bytes()).hexdigest()
        fuentes.append({"archivo": rel, "sha1": h, "contenido": "ambos", "original": f"p{n}.jpg"})
        ind["hashes"][h] = ID
    ev.update(
        parcial=False, rendida=True, revisar=False, fuentes=fuentes, dudas=[],
        resumen="Control corregido, transcrito de las fotos del original (nota 5,2; 42/60). 4 comentes de 5 puntos, 2 "
                "desarrollos de 10 y 1 matemático de 20. Corrector: ayudante Verónica Rojas; profesor Cristian Mundaca. "
                "Pautas propuestas, no oficiales.",
        preguntas=[{"n": n, "puntaje": f"{pu} pts", "obtenido": str(ob), "temas": t, "tipo_pregunta": tp, "dificultad": di,
                    "enunciado": en, "pauta": pa, "pauta_origen": "ia"} for n, pu, ob, t, tp, di, en, pa in PREGUNTAS])
    B.guardar_eval(ind, ev)
    B.guardar_indice(ind)
    temario = M.leer_temario(RAMO)
    h0 = M.hash_temario(RAMO)
    items, sin = M.construir_items(RAMO, ind, temario)
    e = items["evaluaciones"][ID]
    print("parcial:", e["parcial"], "· sin mapa:", sin, "· temario igual:", h0 == M.hash_temario(RAMO))
    print("real:", M.verdad(e))
    for it in e["items"]:
        print(f"  {it['n']:13} {it['puntos']:4} {it['tipo']:11} {it['unidades']}")
    print("parciales del ramo:", {i: x["parcial"] for i, x in items["evaluaciones"].items() if x["parcial"]})


def dominio():
    f = M.dir_motor(RAMO) / "dominio.json"
    d = M.leer(f)
    if d.get("_escala"):
        sys.exit("El dominio ya tiene escala: la migracion no se repite.")
    d["U1"].update(logrado=2.325, posible=6)
    d["U2"].update(logrado=0.7, posible=1)
    d["_escala"] = M.ESCALA_DOMINIO
    d["_migracion"] = {
        "fecha": "2026-11-01",
        "antes": {"U1": "43,5/75 puntos", "U2": "3,5/5 puntos"},
        "U1": "33/40 de matemático (bitácora 2026-10) = 0,825/1; el resto, 10,5/35, repartido en 5 preguntas = 1,5/5.",
        "U2": "3,5/5 como una pregunta = 0,7/1.",
        "supuesto": "No se halló el detalle del resto de U1: se supuso 3 comentes de 5 y 2 desarrollos de 10."}
    M.escribir(f, d)
    print("ok", {u: d[u] for u in ("U1", "U2")})


COMENTES = [("tramo inelástico", .45), ("PIE = toda la pérdida de EC", .40), ("competencia perfecta con más PIE", .35),
            ("margen 1/3", .35), ("produce la mitad", .35), ("3.er grado: prohibir", .35),
            ("competencia monopolística", .35), ("cantidad desde el IMg", .30), ("Hotelling", .30),
            ("3.er grado: más elástico", .25), ("tarifa en dos partes", .20), ("2.º grado", .15)]
DESARROLLOS = [("Lerner", .70), ("no eficiente en el sentido de Pareto", .35), ("monopolio natural", .35),
               ("Hotelling", .25), ("2.º grado", .20), ("eficiencia de la discriminación", .15)]
MATE = [("a: equilibrio de monopolio", .85), ("a: 3.er grado", .15), ("b: PIE frente a CP", .65),
        ("b: 3.er grado", .25), ("b: monopolio social", .10)]
ACIERTOS = ["C11", "D1", "D6", "M1", "M3"]


def manual_json():
    cand = [{"id": f"{pre}{i}", "bloque": b, "texto": t, "p": p}
            for pre, b, xs in (("C", "comentes", COMENTES), ("D", "desarrollos", DESARROLLOS), ("M", "matemático", MATE))
            for i, (t, p) in enumerate(xs, 1)]
    (AQUI / "2026-11-01-manual-control-1.json").write_text(json.dumps({
        "fecha_declarada": "2026-10-21",
        "fuente": "C:/Proyecto Metodologia de estudio/datos/material/microeconomia-ii/2026-10-21-prediccion-control-1-mundaca.tex",
        "nota": "Registrada después de la prueba desde el documento del 21-10; probabilidades copiadas sin cambios.",
        "candidatos": cand}, ensure_ascii=False, indent=1), encoding="utf-8")
    (AQUI / "2026-11-01-manual-control-1-aciertos.json").write_text(json.dumps({
        "aciertos": ACIERTOS, "nota": "Acierto literal por candidato, contra el control corregido."},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", len(cand), "candidatos")


{"ficha": ficha, "dominio": dominio, "manual-json": manual_json}[sys.argv[1]]()
