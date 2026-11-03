# Guion final de Javier · láminas 3, 9 y 10 (+11)

Cada frase en negrita repite lo que dijo el profe en la clase del 08-10 (entre corchetes, el minuto). Si el grupo pasó la 9 a respaldo, sáltala: lo del sexo ya lo dice la lámina 7.

**Tiempo total:** 1 min 45 s (1 min 20 s sin la 9).

---

## Lámina 3 · Fuentes de datos · 40 s

> Los datos vienen de cuatro archivos públicos del DEMRE, admisión 2026. Y esto **no es una muestra, es la población completa** [00:55:43].
> **La unidad es la persona** [00:55:43]: cada estudiante tiene un ID_aux **anonimizado** [01:59:41], y con esa llave unimos los cuatro archivos.
> Así tenemos **variables asociadas a la persona** [01:59:41], como el promedio de notas, el ranking, el sexo y el ingreso.
> Pero **esa persona estudió en un colegio, y el colegio tiene un RBD** [02:01:08]: agrupando por RBD construimos **variables asociadas al colegio**.
> El archivo de postulaciones tiene 1,7 millones de filas, porque cada alumno postula a varias carreras; lo dejamos en una fila por estudiante. Con eso armamos la población y **llegamos al N** [00:54:17], que muestra mi compañero.

*Pasas la palabra para la lámina 4.*

---

## Lámina 9 · Descriptivas · 25 s (solo si sigue en la presentación)

> Estos descriptivos ya **conversan con la interpretación a priori** [00:55:43].
> La mediana de notas es 6,23: postulan estudiantes de buen rendimiento, y por eso esperamos que el puntaje **afecte la probabilidad de que se matricule** arriba [01:59:41].
> Y hay 55 % de mujeres: ellas tienen mejor NEM y los hombres más puntaje en matemática, así que el signo del sexo **no es obvio** y lo tiene que decidir el modelo.

---

## Lámina 10 · Conclusiones · 40 s

> En resumen, el objetivo de esta etapa era **armar una base de datos que contenga la población que corresponde** [00:54:17]: **llegamos a un N de 108.251**.
> La Y es **el complemento**: 1 si quedó en sus tres primeras preferencias y 0 **todos los que no están dentro de eso** [00:22:29], incluidos los no matriculados. Queda en 56 contra 44.
> Para la Etapa 2 **no nos vamos a quedar con los mínimos** [02:02:13]: vamos a **ir al MINEDUC y usar el RBD** [02:01:08] para traer **matriculados, cuántos cursos tiene el colegio y un ratio estudiantes-profesores** [02:01:08], que nos dicen si el colegio **es muy grande o muy chico** y nos pueden **ayudar a predecir la probabilidad de que el estudiante se matricule** [02:01:08].
> Preferimos el colegio antes que la comuna, porque **las comunas son muy heterogéneas** [02:02:13].

---

## Lámina 11 · Cierre · 5 s

> Muchas gracias. ¿Preguntas?

---

## Si te preguntan

**¿Por qué dicen que es población?**
> Porque están todos los que cumplen los criterios, no una parte al azar. Como usted dijo, **esto no es una muestra, es la población completa**.

**¿Y los que rindieron y no postularon?** → lámina de respaldo.
> Lo consideramos: quien no postuló no ordenó preferencias, así que no participa del evento que modelamos. Si prefiere que los incluyamos, los agregamos en la Etapa 2.

**¿Qué signo esperan del ratio estudiantes-profesor?**
> Negativo: más alumnos por profesor es menos atención por alumno, y eso debería bajar el puntaje.

**¿Por qué full join?**
> Para no perder a nadie: los no matriculados no están en el archivo de matrícula y los necesitamos para la Y = 0.
