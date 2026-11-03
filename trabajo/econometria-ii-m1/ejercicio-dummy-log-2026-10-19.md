# M1 · β con dummy y con log (19-10) · ejercicio en curso (sin responder)

Base de postulantes, sin los 161 MATE1 = 0 (n = 108.090). Script: `m1-dummy-log.R`. TP_DUMMY = 1 si egresó de un liceo técnico-profesional (rama T1-T5).

| Modelo | Ecuación estimada | R² |
|---|---|---|
| A | MATE1 = 685,7 − 97,5·TP | 0,062 |
| B | MATE1 = −294,7 + 157,8·NOTAS − 78,0·TP | 0,290 |
| C | ln(MATE1) = 4,979 + 0,2427·NOTAS | 0,248 |

a) En A, ¿qué son 685,7 y −97,5?
b) Con B, MATE1 esperado de un TP con promedio 6,0.
c) Interpreta 0,2427 (por décima y por punto; trampa en el punto).
d) ¿Por qué la brecha TP pasa de −97,5 (A) a −78,0 (B)? Regla del signo. Notas: TP 6,09 · HC 6,21.
e) Comente: «El −78,0 es lo que le cuesta a un alumno estudiar en un TP». Supuesto violado y dirección del sesgo.
