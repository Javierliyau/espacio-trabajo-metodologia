---
tema: econometria-pep1
fecha: 2026-11-03 11:35
resumen: Lectura y P1 de logit hechas; hoy falta la primera pasada de WOE/IV/scorecard y DiD; desde el mié, solo práctica
---
## Objetivo
PEP 1 de Econometría II (Pfeng), **vie 6-11**, escrita, un bloque (~80 min, 100 pts), con calculadora. Hora asumida 13:45 (V4) y sala sin confirmar. Entra hasta DiD; panel no. Meta del estudiante: la mejor nota con las menos horas (estimación: ~5,5, piso ~4,0). Tope de ~5 h efectivas de Econometría por día.

## Hecho en esta sesión
- Lectura de estudio reescrita y leída: 10 pp., logit → clasificación → scoring → DiD, con pistas, frases modelo, trampas y hoja de cierre. Respaldo de la versión anterior en `trabajo/respaldo-lectura-pep1/`.
- Explicados en el chat: los 4 pasos de P̂, e^β̂ y odds (etimología incluida), EPeP frente a EPP (ejemplo inventado con 3 alumnos: EPeP 0,230, EPP 0,308), 1/(1+e^−z) frente a e^z/(1+e^z), notación científica y la matriz explicada «como a un niño de 3 años».
- P1 de práctica (riesgo de crédito, 35 pts) en `trabajo/p1-logit-practica/p1-logit-practica.pdf`, con cuadriculado de 5 mm para GoodNotes. El estudiante resolvió a)-c) (c correcta: 0,4066 y −59,34 %). La d) se hizo **guiada** (matriz 42/18/21/119; exactitud 0,805, sensibilidad 0,70, especificidad 0,85, precisión 0,667).
- Pauta verificada en Python: P̂ = 0,1020 (PROP 0) y 0,0442 (PROP 1), efecto −5,79 pp. EM de CARGA: 0,00504 y 0,00232, o sea ≈5,0 y 2,3 pp por 10 puntos.
- Bitácora anotada (`AG anotar`, 3-11).

## Decisiones tomadas (no re-litigar)
- Prioridad del cálculo: P̂ con la dummy 0/1 y la resta (~90 %); WOE/IV (~80 %); DiD desde las medias (~80 %); matriz (~65 %); SLEP no significativo (~50 %); leer una *scorecard* (~35 %).
- WOE = ln(%B/%M)·100, con los buenos arriba. Fuera: RV/McFadden, VIF, *stepwise*, PDO a mano, probit, PSI y panel.
- Teoría: solo los 22 ítems (núcleo y refuerzo) de la sección «Selección» del banco.
- Practicar con números nuevos; la interpretación pesa tanto como el cálculo. Los ejercicios en curso van en `trabajo/` del espacio.

## Próximo paso exacto
Ejercicio de **WOE, IV y *scorecard*** con números nuevos (tabla de 4-5 tramos: WOE ×100, IV, monotonía y fusión ponderando por N, con qué valor entra una persona y número de β, y sumar puntos de una *scorecard*). Primero uno guiado y después uno sola. Formato PDF con recuadros cuadriculados de 5 mm, como `trabajo/p1-logit-practica/p1-logit-practica.tex`. Verificar en Python antes de entregar. Al cierre del bloque: T37, T52, T59, T33, T34 + T42, T43, T55, T23, T27 en frío.

## Pendientes
- Hoy: DiD (2×2 guiado + SLEP; T62, T69, T77 + T61, T63, T66) y cierre (núcleo de teoría en V/F, ~20 min). Sin teoría en frío todavía: T6, T11, T14, T22, T1 y T13.
- Una matriz de confusión **en frío** con otros números (la d) fue guiada).
- Mié 4-11: simulacro cronometrado de 80 min (P1-P4 + T14, T34, T43, T63, T66, T77) y corrección. Jue: solo lo que falló y la hoja de memoria.
- Calibrar con las PEP 2025 de Pfeng en `C:/Users/javie/Downloads/` («PEP 1 Trabajos Aplicados», «PEP 2 Ejer.»).
- Confirmar la hora y la sala de la PEP y el estado de la Etapa 2. Marcar `[x]` en `datos/agenda/semanas/2026-11-02.md` al cerrar cada bloque.

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
1. `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-02-lectura-pep1-casos-reales.tex`, §3 Scoring (pp. 5-7 del PDF; buscar `Scoring: WOE`).
2. `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-03-banco-teoria-pep1.md`, sección «Selección: los 22 que se estudian».
3. `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-03-pistas-profe-pep1-transcripciones.md`, §4 «Scoring» (líneas 40-52).
4. `C:/Espacio de trabajo Metodologia de estudio/trabajo/p1-logit-practica/p1-logit-practica.tex` (plantilla del formato).
