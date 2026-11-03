---
name: banco-evaluaciones
description: Banco de evaluaciones pasadas del usuario (certámenes, PEP, controles, solemnes, exámenes, tareas, talleres) y sus pautas, organizado por ramo y profesor. Archiva PDFs, fotos o Word de pruebas y pautas, y los analiza (temas que más se repiten, estilo de cada profesor, preguntas recurrentes, prioridades de estudio, simulacros, pautas propuestas). Úsala siempre que el usuario suba o mencione una prueba o pauta pasada, pregunte qué entra en una evaluación, cómo pregunta un profesor, qué estudiar para un certamen, quiera practicar con pruebas anteriores o un simulacro, aunque no diga "banco".
---

# Banco de evaluaciones

El banco vive en `~/OneDrive/BancoEvaluaciones` (una carpeta por ramo, igual que `OneDrive/NotasDeVoz`).
Todo el trabajo pesado lo hace `scripts/banco.py`: lee los PDFs y fotos y analiza con Gemini (gratis), **fuera
de tu contexto**. Tú solo lees salidas compactas. Esa es la regla principal de la habilidad para ahorrar tokens.

```
PY="C:/Users/javie/AppData/Local/Python/pythoncore-3.14-64/python.exe"
B="C:/Users/javie/.claude/skills/banco-evaluaciones/scripts/banco.py"
"$PY" "$B" <comando>
```

## Reglas para ahorrar tokens

1. **Nunca abras con Read un PDF, foto o Word de una evaluación.** Pásalo por `ingresar`. Una prueba de 6 páginas
   leída por ti cuesta decenas de miles de tokens; con Gemini cuesta 0.
2. Responde con el comando más acotado que sirva: `estado` < `listar` < `temas` < `buscar` < `ver --pregunta N`
   < `ver` (la ficha entera). Solo lee una ficha completa si de verdad se necesita.
3. Para "qué entra / cómo pregunta el profe / qué estudio", corre `analizar`: deja `<Ramo>/ANALISIS.md` y se
   guarda en caché (no vuelve a llamar a Gemini si no llegaron evaluaciones nuevas). Lee ese archivo por secciones
   (`CTX seccion <archivo> "Prioridades de estudio"`) en vez de rehacer el análisis tú.
4. Los simulacros y las pautas propuestas también los genera el script; tú solo das la ruta del archivo.
5. Razonamiento difícil sobre una pregunta puntual (verificar un desarrollo matemático, explicar un error): pásale
   a `preguntar_codex` solo el texto de esa pregunta (sale de `ver <id> --pregunta N`), no la ficha completa.

## Comandos

| Comando | Qué hace |
|---|---|
| `ingresar [rutas…] [--ramo --profesor --tipo --numero --anio --semestre --rendida]` | Sin rutas procesa `_Entrada/` y **mueve** los archivos al banco. Con rutas los **copia** (no toca los originales del usuario). Los flags fijan datos que el documento no trae. |
| `estado` | Resumen por ramo: cuántas evaluaciones, pautas oficiales/IA/faltantes, profesores, pendientes. |
| `listar [--ramo] [--profesor]` | Una línea por evaluación con su id. |
| `temas --ramo R [--profesor P]` | Frecuencia exacta de cada tema (en cuántas evaluaciones sale, profesores, periodos). Sin LLM. |
| `buscar "texto" [--ramo] [--completo]` | Preguntas que contienen el texto o tema (sin tildes ni mayúsculas). |
| `ver <id> [--pregunta N]` | Ficha completa o una pregunta con su pauta. El id puede ser un pedazo único (`calculo/2025-1-certamen-1`). |
| `analizar --ramo R [--profesor P] [--forzar]` | Escribe `ANALISIS.md` (o `ANALISIS - <Profesor>.md`). |
| `simulacro --ramo R [--profesor P] [--tipo T] [--preguntas 5]` | Prueba de práctica al estilo real, con pauta, en `<Ramo>/Simulacros/`. |
| `resolver <id> [--pregunta N]` | Propone una pauta con IA para preguntas sin pauta (queda marcada como "no oficial"). |
| `corregir <id> campo=valor …` | Corrige ramo, profesor, tipo, numero, anio, semestre, fecha o rendida (mueve los archivos si cambia el ramo). |
| `enlazar --ramo R <carpeta>` | Conecta un ramo con la carpeta de otro proyecto y crea `<Ramo>/_Subir aqui/`. Tras cada `ingresar`, `analizar`, `simulacro`, `resolver` o `corregir`, se copia solo lo liviano (INDICE.md, fichas .md, ANALISIS, simulacros), sin los PDFs. |
| `sincronizar` | Fuerza esa copia a todos los proyectos enlazados (`enlaces.json`). |
| `pdf [id] [--ramo R] [--profesor P]` | Reconstruye la prueba como PDF limpio con solo los enunciados, agrupados en Comente/Análisis/Matemático y con KaTeX, usando Edge headless. Queda en `<Ramo>/Reconstruidas/` y se sincroniza. |
| `predecir --ramo R --evaluacion "Control 1" --fecha AAAA-MM-DD [--profesor P] [--alcance U1,U2] [--entra U3] [--no-entra U4] [--provisional]` | Para cada unidad del alcance da P(entra), puntos esperados (% de la prueba), rango, el porqué, tipo×Bloom probable y el reparto del tiempo de estudio. Escribe `<Ramo>/PREDICCION - <evaluación>.md` y lo sincroniza. Sin LLM: es un modelo bayesiano más Monte Carlo y tarda ~1 s. Ver «Motor de predicción». |
| `motor preparar --ramo R` / `motor senales --ramo R` | Prepara los insumos de `predecir` (ver «Motor de predicción»). |
| `motor backtest --ramo R` | Valida el motor sin mirar el futuro, contra cuatro líneas base (ver «Motor de predicción»). |
| `motor evaluar --ramo R [--evaluacion "PEP 1"]` / `motor ciclo` / `motor tablero` / `motor semanal` / `motor rollback --version 1.0 [--motivo "..."]` | Aprendizaje continuo (ver «Aprendizaje continuo»). `evaluar` corre solo al `ingresar`; casi nunca hace falta a mano. |
| `ingresar … --fecha AAAA-MM-DD` | Fecha en que se rindió, si el documento no la trae (la usa el motor para saber qué predicción evaluar). |
| `ingresar … --nota "texto"` | Pasa a Gemini una instrucción prioritaria para ese lote. Ej.: ignorar lo escrito a lápiz y transcribir solo el enunciado impreso. Para una prueba de varias fotos: una subcarpeta por prueba en `_Subir aqui/`, con las fotos nombradas en orden. |

## Flujo al recibir evaluaciones

1. Si el usuario da rutas o adjunta archivos: `ingresar <rutas>` con los flags que ya sepas por la conversación
   (p. ej. "es el certamen 2 de Macro con Mundaca del 2024" → `--ramo "Macroeconomía II" --profesor Mundaca --tipo Certamen --numero 2 --anio 2024`).
   Marca `--rendida` si es una prueba que el usuario rindió: el análisis la contrasta con la pauta.
   Varias fotos de una misma prueba van en una subcarpeta (se procesan juntas como una sola evaluación).
2. Si están en Google Drive, descárgalas a `_Entrada/` con el conector de Drive y corre `ingresar`.
3. Informa en pocas líneas lo que imprimió el script. Si una evaluación sale con ⚠ (por confirmar), pregunta solo
   el dato dudoso y corrígelo con `corregir`.
4. Una pauta que llega después se une sola a su enunciado (mismo ramo, tipo, número y periodo). Si no se unió,
   probablemente falta el año o el número: `corregir` la pauta con esos datos.

El usuario también puede hacerlo sin ti: deja archivos en `_Entrada/` o en `<Ramo>/_Subir aqui/` (así el ramo ya
queda fijado) y hace doble clic en `Ingresar.bat`.

Enlaces activos: Microeconomía II → `C:\Proyecto Metodologia de estudio\datos\material\microeconomia-ii\banco-evaluaciones`.
Dentro de ese proyecto, lee la copia enlazada (`INDICE.md`, `ANALISIS.md`) en vez de correr comandos.

## Cómo se organiza

```
BancoEvaluaciones/
  _Entrada/  _Revisar/  Ingresar.bat  indice.json (catálogo)  INDICE.md (tabla legible)
  <Ramo>/Originales/  2024-2 Certamen 2 - Mundaca [pauta].pdf
        /Fichas/      2024-2 Certamen 2 - Mundaca.md (+ .json)
        /ANALISIS.md  /Simulacros/  /PREDICCION - <evaluación>.md
        /Motor/       temario.json  items.json  senales.json  dominio.json
        /Predicciones/ <AAAAmmdd-HHMMSS>-<evaluación>.json (pre-registro inmutable)
        /Motor/Resueltas/ <id del registro>.json (resolución inmutable)   /Postmortem/ <evaluación> <periodo>.md
  DESEMPENO_MOTOR.md (tablero del motor)   motor-semanal.log
```

- Los nombres de ramo se toman de las carpetas de `NotasDeVoz` y del banco, para que "macro 2", "Macroeconomia II"
  y "Macroeconomía II" terminen en la misma carpeta. Los profesores se unifican por apellido.
- Los temas de cada pregunta se reutilizan entre evaluaciones del mismo ramo. Por eso `temas` sirve para contar.
- Los apuntes de clase del mismo ramo están en `OneDrive/NotasDeVoz/<Ramo>/Apuntes/`. Para un plan de estudio,
  cruza las prioridades de `ANALISIS.md` con `grep -il "<tema>"` sobre esos apuntes, sin leerlos completos.
- `<Ramo>/PISTAS_CLASES.md` en el banco lo llena la habilidad `goodnotes`. Junta lo que el usuario anotó en clase
  como "pregunta prueba" o énfasis del profesor. Es corto: léelo antes de `analizar` o de armar un simulacro, y
  dale a esos temas más peso que a los que solo aparecen en pruebas antiguas.

## Motor de predicción

El diseño, con sus fuentes y supuestos, está en `C:\Proyecto Metodologia de estudio\datos\motor-predicciones\fase2-diseno.md`.
Código: `scripts/motor.py`. Insumos por ramo, en `<Ramo>/Motor/`:

- `temario.json` (**a mano**, desde el programa del ramo). Lleva
  `unidades: [{id, nombre, objetivo, bloom B1|B2|B3, peso, opcional, desde AAAA-MM-DD|null, biblio true|null}]`,
  `temas: {"<tema del banco>": "U1"|null}` (null = transversal) y `transversal_por_defecto`.
  Los `desde` son el calendario: cuando haya fechas oficiales, llénalos y el alcance sale solo.
- `items.json`: lo genera `motor preparar`, que cuesta 1 petición de Gemini para el Bloom y 1 más si hay temas nuevos.
  Se puede editar `fecha`, `orden` (con `orden_supuesto: false`), `alcance` (con `alcance_manual: true`) y
  `bloom_claude`, y se conservan al regenerar. Una prueba de este mismo semestre sin `fecha` no se usa: anótale la fecha.
- `senales.json`: lo genera `motor senales`, con 1 petición por transcripción nueva de
  `NotasDeVoz/<Ramo>/Transcripciones/` y 1 por `PISTAS_CLASES.md`. Queda en caché por hash. Córrelo cuando haya clases nuevas.
- `dominio.json` (opcional): `{"U1": {"auto": 1-5, "logrado": pts, "posible": pts}}`. Sin él, dominio = 0. `evaluar` suma
  `logrado`/`posible` solo si la prueba es `rendida` y la ficha trae `obtenido` por pregunta (`_fuentes` evita sumarla dos veces).

El alcance sale, en este orden, de `--alcance`, de los `desde` ≤ fecha, de las unidades vistas en clases transcritas
hasta la fecha, y si no hay nada de eso, del programa completo sin las unidades opcionales. Lo que el profesor dijo que
entra o no entra solo se aplica con `--entra` / `--no-entra`; las frases detectadas en las clases se muestran para
que tú decidas.

Los hiperparámetros (escenarios, β de las señales, decaimiento y corridas) viven en `scripts/versiones/vX.Y.json`
(solo lectura; nunca se editan) y `scripts/campeon.json` dice cuál rige, con el historial y los retadores. Cada corrida de
`predecir` deja un pre-registro inmutable, de solo lectura, en `<Ramo>/Predicciones/<AAAAmmdd-HHMMSS>-<evaluación>.json`,
con la versión del modelo, el hash de los datos, las pruebas usadas, las probabilidades por escenario, la
descomposición por nivel y los factores de cada señal. Se guardan todas las corridas, y la que vale es la última
emitida antes de la prueba. Nunca los borres ni los edites.

Al informar, da la ruta y las 3-4 líneas que imprime el script; no leas el .md completo. Si el alcance queda en una
sola unidad, pregunta si la prueba cubre más.

**Backtest** (`motor backtest --ramo R [--corridas 2000] [--semilla 7]`, ~10 s): predice cada prueba del banco solo con
las anteriores y sin señales de clase, en dos modos. En el modo *programa* el alcance es todo el programa; en el modo
*conocido* es el alcance real y se mide solo el reparto. Lo compara con cuatro líneas base: frecuente, última prueba,
uniforme y programa. Reporta Brier (con la descomposición de Murphy), log-loss, error del reparto, top-N y calibración
con barras de consistencia, separado por profesor. Escribe `<Ramo>/Motor/Backtest/<fecha>-v<versión>.md` y `.json`.
Informa solo las líneas que imprime el script. Resultado y lectura de Micro II:
`datos/motor-predicciones/fase4-backtest.md` (proyecto de metodología).

### Aprendizaje continuo (Fase 5)

Diseño y reglas fijadas de antemano: `datos/motor-predicciones/fase5-diseno.md`; cierre: `fase5-cierre.md`. Todo es
script, sin LLM.

- **Al ingresar** una prueba de un ramo con `Motor/`, se regeneran los items y, si había una predicción de esa prueba
  (misma tipo, número y periodo; la última emitida antes de la fecha real o del ingreso), se resuelve: escribe
  `Motor/Resueltas/<id>.json` y `<Ramo>/Postmortem/…md` (motor contra las cuatro líneas base, error de alcance, acierto
  direccional por señal, causas por reglas fijas, deriva y dominio). Luego corre `motor ciclo`. Si el motor falla, el
  ingreso queda guardado y se imprime el error.
- **`motor ciclo`** (~5 s): walk-forward del campeón; retador MAP en rejilla (×½, ×1, ×2, prior log-normal); retadores
  estructurales (v1.1 «alcance por posición») y de deriva (vida media a la mitad). Un retador reemplaza al campeón solo si
  baja el Brier medio con el IC 90 % pareado entero bajo 0, no empeora el cuad y n ≥ 5. Platt solo con ≥ 50 pronósticos
  prospectivos. Escribe `DESEMPENO_MOTOR.md`.
- **Tarea de Windows** «BancoEvaluaciones - motor semanal» (domingo 20:00, `scripts/motor-semanal.bat`): corre el ciclo
  solo si cambiaron los datos y anota en `motor-semanal.log`. `estado` lista las predicciones vencidas sin resolver.
- `motor rollback --version X` deja X como campeón y lo anota; no borra nada. Nunca edites `versiones/`, `Resueltas/`
  ni `Predicciones/`.
- Al informar: las líneas que imprime el script y el veredicto del tablero. Con n < 5 resoluciones el veredicto es
  «sin evidencia todavía»: no lo maquilles.

## Límites de Gemini

Nivel gratis: unas 20 peticiones al día **por modelo**. El script recorre varios modelos Flash, así que da para
unas 100 al día. Cada evaluación ingresada gasta 1 petición, y `analizar`, `simulacro` y `resolver` gastan 1 cada uno.
Si imprime "Todos los modelos Gemini agotaron su cuota", avísale al usuario: lo que quedó en `_Entrada`
se procesa al día siguiente. No leas tú los PDFs para reemplazar a Gemini, salvo que el usuario lo pida sabiendo
lo que cuesta.
