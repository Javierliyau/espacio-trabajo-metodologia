# Lista de errores · PEP 1 Micro II

Formato: ítem · qué escribí · **frase correcta** · marcas. Se pregunta tapado al inicio de cada sesión (`plan-paro.md` §4); con 2 aciertos seguidos sale de la lista. Llenada el 10-11 con lo que consta en la bitácora.
**R** = error recurrente (salió en 2 o más sesiones, o con seguridad alta): va primero en los 10 min de errores.

| # | Ítem | Qué escribí | Frase correcta | Marcas |
|---|---|---|---|---|
| 1 | Árbol de entrada (simulacro final D1) | Una rama de más | El árbol solo tiene las decisiones reales: el entrante elige entrar o no entrar; el incumbente decide (pelear o acomodar) solo después de «entrar» | |
| 2 | R · Árbol de entrada | «No entrar está dominada» | Falso: si el incumbente pelea, no entrar es la mejor respuesta. Por eso hay 2 EN; la inducción hacia atrás deja uno solo (ENPS), porque pelear es una amenaza no creíble | ✓ 11-11 |
| 3 | R · Matriz 3×3, eliminación iterada | Pasos sin números | Cada eliminación lleva la comparación de pagos escrita (p. ej. «4 > 2, 3 > 1, 5 > 0 ⇒ X domina a Z») | ✗ 11-11 (seg. 80 %) |
| 4 | R · Matriz 3×3, equilibrio | EN como pagos: (3, 2) | El EN es un **perfil de estrategias**: (Y, Q). Los pagos se informan aparte | ✓ 11-11 |
| 5 | Matriz 3×3, a) | Revisé solo al jugador A | La dominancia se revisa para los dos jugadores antes de eliminar | |
| 6 | R · Dilema repetido | Llamé «cooperar» a confesar | Cooperar = no confesar (mantener el acuerdo). Confesar = desviarse | ✓ 11-11 |
| 7 | R · Dilema repetido | El papel del castigo, al revés | La amenaza de castigo **reduce** el incentivo a desviarse: la ganancia de hoy se compara con la pérdida futura descontada | ✗ 11-11 (respondió V) |
| 8 | R · Comentes (Control 1 y simulacros) | Respondí V siendo F | Primero buscar el caso que lo hace falso. Primera línea: V, F o I; después el mecanismo y, si hay precio, el número | |
| 9 | R · Precio de monopolio | Sin Lerner ni ε | Todo resultado de precio cierra con L = (P − CMg)/P = 1/|ε|: más inelástico, más margen | |
| 10 | Mecanismo IMg < 0 | Mecanismo ausente | El monopolista nunca produce en el tramo inelástico (|ε| < 1, IMg < 0): ahí bajar q sube el ingreso y baja el costo | |
| 11 | Dominada estricta vs débil (Mi3) | Definí a la que domina («da un pago mayor»), sin «ante todas las del rival» | **Dominada** = existe otra estrategia que da un pago estrictamente mayor (estricta) o ≥ en todas y > en al menos una (débil) **ante todas las estrategias del rival**. Al eliminar débilmente dominadas se puede perder un EN | ✗ 11-11 |
| 12 | Árbol de entrada: pagos de quién | «I acomoda porque 3 > 1» | Se comparan los pagos **del que decide**: I: 4 > 1. Nombrar al jugador en cada comparación | ✗ 11-11 |
