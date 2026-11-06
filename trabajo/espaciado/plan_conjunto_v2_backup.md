# Plan conjunto · PEP 1 de Econometría II y de Microeconomía II (las dos el jue 12-11)

Hecho el vie 6-11 y **reescrito ese mismo día para la PEP de Econometría en dos bloques (jue 12-11, 08:15-11:10, ~160 min)**, el mismo día que la de Micro (¿13:45?). Une dos planes: el plan espaciado de Econometría, **versión 3** (`material/econometria-ii/2026-11-06-plan-repaso-espaciado-pep1.md`, §2-§3), y las sesiones de Micro μ1-μ7, armadas aquí sobre la predicción de Mundaca (`2026-11-04-prediccion-pep-1-mundaca.pdf`).

**Decisión:** Econometría pasa a la **versión 3**: 10 sesiones A-J, 360 min, con pesos de dos bloques y dos temas nuevos (probit a mano y primeras diferencias). **Micro no cambia:** volví a optimizarla alrededor de la versión 3 y no gana nada (4,91 frente a 4,94 de las sesiones actuales, que es ruido). μ1-μ7 quedan como están en la agenda.

## 1. Resultado

| Plan | Econometría (min) | Micro (min) | Nota Econometría (P ≥ 5) | Nota Micro (P ≥ 5) | Días más cargados (estas dos materias) |
|---|---:|---:|---|---|---|
| Antes: Econometría v2 + μ1-μ7 | 307 | 457 | 4,94 (42 %)¹ | 4,94 (40 %) | mar 159 · vie 107 |
| **Este: Econometría v3 + μ1-μ7** | **360** | **457** | **5,12 (65 %)¹ · 5,02 (53 %) con fatiga²** | **4,94 (40 %)** | **mar 165 · vie 139** · el resto ≤ 121 |
| v3 con todos los opcionales | 418 | 457 | 5,25 (81 %)¹ · 5,16 (70 %)² | 4,94 (41 %) | vie 163, con μ1 movida al sábado (ver §6) |
| Micro reoptimizado desde cero | 360 | 448 | 5,02² | 4,91 (36 %) | mar 165 |
| Micro ligero (si falta tiempo) | 360 | 390 | 5,03² | 4,80 (24 %) | ≤ 143 |

¹ Modelo del plan de Econometría (Monte Carlo con 3.000 escenarios).
² Modelo conjunto, que supone más fatiga por las dos PEP del mismo día: presión de 0,83-0,96 en Econometría y de 0,78-0,92 en Micro (2.000 escenarios). La diferencia de 0,1 viene de ese supuesto mío, no de datos.

**Lectura:** Econometría v3 suma 53 min (+17 % de tiempo) y sube entre +0,1 y +0,2. Lo que más pesa es que ahora entran el `glm`, la matriz de confusión, AUC/KS y las amenazas con su sesgo, que en dos bloques pesan casi el doble. Micro queda en 4,94, con un rango del 80 % de 4,6-5,3. Para subirla, la palanca no son más minutos (de 450 a 510 min no gana nada): es que el simulacro del martes (μ5) recalibre la q de cada tema. Si sale peor de lo esperado, reoptimizo con esos datos.

## 2. Las reglas de la literatura que se aplicaron

| # | Regla | Evidencia | Dónde se nota |
|---|---|---|---|
| 1 | Cada tema, **≥ 2 pasadas de recuperación separadas por 1-3 días**. Con el examen a ~1 semana, el intervalo óptimo es ~3 días | Cepeda et al. 2008: +64 % de recuerdo con el intervalo óptimo frente a todo seguido (d ≈ 1,1); Cepeda et al. 2006 | Juegos (M7): sáb → dom → lun → mar → mié → jue. 3.er grado (M1): dom → mar → mié |
| 2 | El tiempo se va en **hacer sin mirar y corregir con pauta**, no en releer | Rowland 2014: g = 0,50; con corrección, g = 0,73. Adesope et al. 2017. Dunlosky et al. 2013: práctica con pruebas y espaciada, «utilidad alta»; releer, subrayar y resumir, «baja» | Cada sesión parte con un pretest o un ejercicio en frío |
| 3 | Lo aprendido recuperando **aguanta el estrés** de la prueba | Smith et al. 2016 (Science). Ojo: Wolf y Kluge 2017 discuten la causa | Simulacro cronometrado el martes |
| 4 | **Intercalar dentro de cada materia** (monopolio, discriminación, Hotelling y juegos mezclados) | Rohrer y Taylor 2007: 63 % frente a 20 % a la semana. Brunmair y Richter 2019: g = 0,42 (0,34 en matemáticas). Firth et al. 2021 | Un tema aparece una vez por sesión y las sesiones mezclan 3-9 temas |
| 5 | **Entre materias, alternar por bloque, no dentro del bloque**: mezclar dos temas no relacionados no ayuda | Hausman y Kornell 2014. Brunmair y Richter 2019: el intercalado sirve cuando las categorías se parecen | Cada sesión es de una sola materia |
| 6 | **Mini-prueba de 5 min al cerrar el bloque**, antes de cambiar de materia: frena la interferencia | Szpunar et al. 2008: el doble de recuerdo y menos intrusiones | Últimos 5 min de cada sesión: 3 preguntas de memoria |
| 7 | **El último bloque antes de dormir es corto y de recuperación**, y el miércoles es de Econometría (la primera prueba). Micro se cierra antes | Gais et al. 2006; Ellenbogen et al. 2006: dormir pronto después de estudiar protege de la interferencia. *El orden exacto es una inferencia; la interferencia entre materias distintas es baja* | Mié: Micro 18:30, Econometría I 22:30, dormir |
| 8 | **Nada de trasnoche**: ni el domingo (PEP de Macro) ni el miércoles. Dormir 7-8 h | Cousins et al. 2018; Huang et al. 2016 (dormir 5 h daña lo estudiado en bloque, no lo espaciado); Mazza et al. 2016 (dormir entre sesiones reduce a la mitad el reaprendizaje); Okano et al. 2019; Rasch y Born 2013 | Ninguna sesión de estas materias después de las 22:45 |
| 9 | **El tiempo va a lo «casi sabido»** y a lo que más pesa; un ítem se deja cuando ya no avanza | Metcalfe y Kornell 2005 (región de aprendizaje próximo) | El optimizador elige por ganancia de nota por minuto. Monopolio (37/40 en el Control 1) aparece solo 1 vez |
| 10 | **Pausas fijas**: 25 min de trabajo y 5 de pausa, no «cuando me canse» | Biwer et al. 2023: menos fatiga y la misma tarea en menos tiempo | Las sesiones de más de 30 min van en bloques de 25 + 5 |
| 11 | **Entre las dos pruebas del jueves: 30 min de pausa real** (comer, sin pantalla, sin comentar Econometría) y después un calentamiento corto. Nada nuevo el jueves | Sievertsen et al. 2016: el rendimiento cae con la hora del día y una pausa de 20-30 min lo recupera (efecto pequeño). Gill 2026: dos pruebas el mismo día rinden algo menos | Jueves: solo ítems cortos y ya repasados ≥ 2 veces |
| 12 | **10 min de escritura expresiva** antes de cada prueba (escribir lo que te preocupa) y leer la activación como algo útil | Ramirez y Beilock 2011 (Science); Jamieson et al. 2010 | 07:50 y 13:30 del jueves |
| 13 | Cafeína: **tu dosis habitual**; no experimentar el jueves | Borota et al. 2014: U invertida | — |

No se encontró un límite de horas diarias con respaldo. El tope que usa el plan, **≤ 2 h 40 de estas dos materias por día**, sumando lo demás ≤ ~4,5 h de estudio, es un criterio propio para no sobrecargar.

Referencias (DOI): Cepeda 2006 10.1037/0033-2909.132.3.354 · Cepeda 2008 10.1111/j.1467-9280.2008.02209.x · Rowland 2014 10.1037/a0037559 · Adesope 2017 10.3102/0034654316689306 · Smith 2016 10.1126/science.aah5067 · Rohrer y Taylor 2007 10.1007/s11251-007-9015-8 · Brunmair y Richter 2019 10.1037/bul0000209 · Hausman y Kornell 2014 10.1016/j.jarmac.2014.03.003 · Firth 2021 10.1002/rev3.3266 · Szpunar 2008 JEP:LMC 34(6):1392 · Gais 2006 10.1101/lm.132106 · Ellenbogen 2006 10.1016/j.cub.2006.05.024 · Rasch y Born 2013 10.1152/physrev.00032.2012 · Mazza 2016 10.1177/0956797616659930 · Huang 2016 10.5665/sleep.6092 · Okano 2019 npj Sci. Learn. (PMC6773696) · Metcalfe y Kornell 2005 10.1016/j.jml.2004.12.001 · Biwer 2023 10.1111/bjep.12593 · Sievertsen 2016 PNAS 113(10):2621 · Gill 2026 10.17863/CAM.127731 · Ramirez y Beilock 2011 10.1126/science.1199427 · Jamieson 2010 10.1016/j.jesp.2009.08.015 · Borota 2014 10.1038/nn.3623 · Dunlosky 2013 10.1177/1529100612453266. Las cifras de Cepeda 2008, Rowland 2014, Rohrer y Taylor 2007 y Gill 2026 se verificaron en el texto; las demás vienen del resumen.

## 3. Inventario de Micro

Peso = puntos esperados de 60, según la predicción (§2-§4), normalizados a 4 comentes × 5 + 2 desarrollos × 10 + matemático × 20. q = probabilidad de ejecutarlo bien si lo recuerdas, estimada con el Control 1 (42/60).

| Tema | Qué es | Peso (pts) | Estado | q |
|---|---|---:|---|---:|
| **M7** | Juegos estáticos: matriz 3×3, dominancia iterada, EN, dilema del prisionero, sin dominantes, EN en puras | **13,8** | **Nunca practicado** | 0,45 |
| **M1** | 3.er grado frente a precio único: demanda agregada por tramos, ¿excluir un grupo?, excedentes y gráfico (el matemático) | **12,8** | Ayudantías de octubre; nunca sin mirar | 0,55 |
| **M2** | Tarifa en dos partes y 2.º grado: p = CMg y T = EC con idénticos; p* > CMg con dos tipos; renta de información | 8,1 | **C2 del Control 1: 1/5** | 0,30 |
| M4 | Monopolio: Lerner, elasticidad, tramo inelástico, monopolio natural | 7,0 | 37/40 en el Control 1 | 0,88 |
| M5 | Competencia monopolística, CP y LP: P = CMe > CMg, exceso de capacidad | 6,0 | No evaluado | 0,50 |
| M3 | 1.er grado, PIE y Pareto | 4,4 | **C3 1/5 y D1 3/10** | 0,35 |
| M6 | Hotelling: el centro frente al óptimo social (1/4 y 3/4) | 3,7 | No evaluado | 0,50 |
| M8 | Juegos secuenciales: árbol, inducción hacia atrás, amenaza no creíble | 2,2 | Nuevo; **no se sabe si entra** (peso × 0,7) | 0,35 |
| M9 | Paquetes: correlación negativa de las valoraciones | 1,1 | Nuevo | 0,40 |

## 4. Las sesiones, día a día

**Econometría: sesiones A-J de la versión 3** (el detalle y el material están en el §3 del plan de Econometría y en la agenda). **Micro: sesiones μ1-μ7, sin cambios.** Formato de cada sesión de Micro: **pretest o ejercicio en frío → pauta → rehacer lo fallado (criterio) → mini-prueba de 5 min**. Los comentes se escriben con el veredicto en la primera palabra.

| Día | Econometría (v3) | **Micro** | Lo demás (fijo) |
|---|---|---|---|
| **vie 6** | **A** 11:00, o 13:45 si hay clases (60): T6 y T4 nuevos (A2 y A1) + ATT y tendencias paralelas · **B** 16:00 (45): WOE ×100, 6 V/F, P̂ y odds + **probit a mano A6, nuevo** *(opcional, +45: A7, una amenaza, A2 d-e, MPL)* · **C** 22:30 (14): EP en X = 4, los 4 problemas del MPL + Card-Krueger en 3 líneas | **μ1 · 17:00 (23 min)** · M2, M3: rehacer en frío el **C2** (dos partes con idénticos) y el **C3** (3.er grado y Pareto) del Control 1, y el **D1** en 5 líneas (paradoja del 1.er grado). Corregir con `2026-11-01-feedback-control-1.md` | Ayudantía de Macro 09:50; predicción final de Macro (tarde) |
| **sáb 7** | **D** 13:00 (35): PDO, 2 amenazas con su sesgo, WOE e IV, ATT en voz alta + **A1 b-d con la pauta tapada** | **μ2 · 16:00 (86 min, 3 bloques de 25 + 5)** · **M7 juegos (60)**: pretest de 5 min con los comentes C2, C4 y C6 de la predicción, sin saber; slides `2026-11-01-teoria-de-juegos.pdf` pp. 20-76, activo (cada ejemplo, taparlo y resolverlo antes de mirar); al final, una matriz 3×3 de las slides sin mirar · **M5 (10)**: comente C1 (competencia monopolística a LP) con gráfico · **M9 (16)**: slides pp. 41-44 y comente C11 | Macro ~2 h (demostraciones) |
| **dom 8** | **E** 13:00 (38): cuadrático, scorecard, β/4, un WOE, matriz y mover el corte + **una amenaza (STAR o ECA) con su sesgo** | **μ3 · 16:00 (60 min)** · **M1 (30)**: A2 ej. 2 sin mirar (3.er grado frente a precio único; revisar si conviene excluir) · **M2 (15)**: A3 ej. 5 (dos partes) · **M7 (15)**: escribir los comentes C2, C4, C6 y C14 y una matriz nueva que te genero en el chat | Simulacro de Macro (2 h) y hoja de memoria. **Dormir temprano** |
| **lun 9** | **F** 12:00 (36): WOE/IV en frío, Card-Krueger, A1 y A2 a-c tapadas, EP de una dummy *(opcional: A7 tapada)* | **μ4 · 20:00 (85 min)** · **M7 (15)**: la matriz de la PEP 1 2026-1, sin mirar · **M8 (37)**: slides de secuenciales y el árbol de la Suficiencia 2026-1. *Si el profesor dijo que no entran: esos 37 min van a una 2.ª matriz y al A3 ej. 4 (3.er grado con arbitraje)* · **M2 (15)**: A4 ej. 4 (dos partes con dos tipos) · **M5 (10)**: A4 ej. 5 · **M3 (8)**: comentes C10 y C13 | **PEP de Macro 09:50**; presentación de Historia (~2 h, tarde) |
| **mar 10** | **G** 13:00 (53): mini-simulacro mezclado de 9 ítems + **probit con la pauta tapada** | **μ5 · 15:00 (112 min)** · **Simulacro** `2026-11-04-simulacro-pep-1-mundaca.pdf` cronometrado (80 min), con pausa de 5 min a la mitad si te la permites. Corregir con `…-PAUTA-no-abrir.md` (30 min) y armar la **lista de errores de Micro**. Cubre M1-M9 | Clase de Micro 08:15 (**preguntar hora, sala y duración de la PEP y si entran los secuenciales**); **presentación L8** 09:50; Historia noche (1,5 h) |
| **mié 11** | **H** 12:45 (37): Gini y KS, DiD 2×2 desde medias, PDO, A1 d), MPL, lista de fallas · **I** 22:30 (15), **el último bloque del día**: 100(e^β − 1), las 4 métricas, 3 V/F de scoring | **μ6 · 18:30 (53 min)** · **M1 (30)**: A4 ej. 3 sin mirar · **M7 (15)**: una matriz nueva + los EN en puras · **M6 (8)**: Hotelling (slides pp. 58-79) y el comente C3 con gráfico. **Micro queda cerrada aquí** | Historia: trabajo escrito L8 (11:10) y L5 (13:45). **La Historia de la noche baja a 1 h** (L6 con protocolo, 20:00-21:00); las fichas de la L3 y la 3.ª de la L4 pasan al jue en la tarde |
| **jue 12** | **J** 06:45 (30): «Las 15 frases», un WOE, un EP, una amenaza, ATT en una frase · **PEP 08:15-11:10** | **μ7 · 13:10 (25 min, único)** · §6 de la predicción (respuestas en pocas líneas), una matriz rápida, dos partes en 2 líneas y la lista de errores (veredicto en la primera palabra, IMg = P(1 − 1/\|ε\|), ES_CP − ES = PIE, ¿excluir un grupo?) | Taller 11:25-12:45; **PEP de Micro ¿13:45?**; Historia desde las ~17:00 |

**Carga de estas dos materias por día (min), sin opcionales:** vie 139 · sáb 121 · dom 98 · lun 121 · mar 165 · mié 105 · jue 55, más dos escrituras expresivas de 10 min. El martes queda 5 min sobre el tope de 2 h 40, porque el simulacro de Micro es un solo bloque. Si ese día pesa, G deja fuera la pregunta de Econometría I (T13, la de menor peso).

## 5. Jueves 12, minuto a minuto

| Hora | Qué |
|---|---|
| 06:45-07:15 | Sesión J de Econometría (calentamiento, nada nuevo) |
| 07:50-08:00 | **10 min de escritura expresiva**: anotar lo que te preocupa de la prueba y botar la hoja. Leer los nervios como energía útil |
| 08:15-11:10 | **PEP 1 de Econometría (dos bloques)**. Si hay recreo entre bloques: agua y algo de comer, sin repasar. Reparte el tiempo según el puntaje (~1 min por punto) y deja 10 min al final para revisar los cálculos |
| 11:10-11:25 | Snack, caminar. No comentar ni revisar la prueba (ya no se puede cambiar y gasta atención) |
| 11:25-12:45 | Taller de Comunicación: cuenta como descanso de las dos materias. Nada de Micro ahí |
| 12:45-13:10 | **Almuerzo de verdad, sin pantalla** (la pausa real del día) |
| 13:10-13:35 | μ7: calentamiento único de Micro, solo lo ya repasado |
| 13:35-13:45 | 10 min de escritura expresiva |
| 13:45 | **PEP 1 de Micro** (hora sin confirmar) |

## 6. Reglas de ajuste

- **Si fallas un tema en una sesión**: rehazlo en esa misma sesión hasta que te salga y anótalo. Vuelve en la próxima sesión de esa materia (regla del §4 del plan de Econometría). En Econometría, la corrección del simulacro en la sesión A recalibra la tabla: cada tema fallado baja a S = 1 d.
- **Si haces los opcionales de Econometría (418 min)**: el viernes llega a 186 min, sobre el tope. En ese caso μ1 pasa al sábado, al inicio de μ2 (15:35-16:00). El modelo da la misma nota de Micro (4,94) y el viernes queda en 163 min. Los opcionales del lunes (A7) y del martes no mueven nada.
- **Si falta tiempo**: primero se recortan los opcionales de Econometría (5,12 en vez de 5,25). Después, la versión ligera de Micro (390 min, 4,80): se quitan M8, M9 y M6 de los días intermedios y quedan μ2, μ3, μ5 y μ6. **Nunca se recortan** juegos estáticos (M7), 3.er grado (M1), dos partes (M2), probit (T15) ni el `glm` (T4).
- **Si el martes se confirma que los secuenciales no entran**: los minutos de M8 pasan a M7 y M1 (ver μ4).
- **Si la PEP de Micro no es a las 13:45**: μ7 se corre para que quede justo antes de la prueba, siempre con al menos 30 min de pausa después de Econometría.
- **Si aparece la hora o el formato real de alguna PEP, o si el simulacro de Micro del martes sale bajo 4,5**: avisar en el chat para recalibrar los pesos y la q y reoptimizar (`trabajo/espaciado/joint2.py`, con `V3=360` o `V3=420`).

## 7. Cómo se calculó

Scripts del espacio de trabajo:
- `trabajo/espaciado/joint.py`: el modelo conjunto. Carga Econometría v3 desde `v3_360.json` o `v3_420.json`.
- `joint2.py`: deja Econometría fija y optimiza Micro.
- `eval_agenda.py`: evalúa las sesiones μ1-μ7 de la agenda.

Usan el mismo modelo que el plan de Econometría: FSRS-6 con ganancia × 0,4 y q por Beta-binomial. Encima se agregan:
- el recuerdo previo de cada tema (días desde el Control 1 o la ayudantía);
- escalas distintas: Econometría con 60 % de exigencia y Micro con 50 %, porque 42/60 = 5,2;
- presión de 0,83-0,96 en Econometría y de 0,78-0,92 en Micro, por las dos pruebas del mismo día.

En Econometría se usan los pesos de dos bloques: glm 70 %, matriz 75 %, AUC/KS 60 %, amenazas 65 %, V/F 80 %, probit 25 % y primeras diferencias 15 %. Los temas nuevos se aprenden a más tardar el domingo.

Restricciones:
- los topes diarios;
- una materia por sesión;
- juegos aprendidos a más tardar el sábado;
- Micro cerrada el miércoles, con Econometría como último bloque de esa noche;
- el jueves, solo ítems cortos repasados ≥ 2 veces.

Se optimiza con voraz + recocido simulado (40.000 pasos, 4 reinicios que coinciden en ±0,02) y se valida con Monte Carlo (2.000 escenarios).

**Límite:** los pesos de Micro vienen de una sola PEP pasada de Mundaca y de los controles; los de Econometría, de ninguna PEP pasada. El paisaje es plano: diferencias menores a ±0,05 son ruido.
