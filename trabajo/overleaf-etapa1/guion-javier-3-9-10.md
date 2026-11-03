# Guion de Javier: láminas 3, 9 y 10

**Tiempo total:** 1 min 45 s. Las frases en negrita son las que el profe dijo en clase que quiere escuchar: díganlas tal cual.

---

## Lámina 3 · Fuentes de datos (40 s)

*Entras después de la lámina 2.*

> Todo viene del portal del DEMRE, admisión 2026, en cuatro archivos públicos. No trabajamos con una muestra: **es la población completa**.
> **La unidad de análisis es la persona**: cada estudiante tiene un ID_aux, anonimizado, y con esa llave unimos los cuatro archivos.
> De los archivos de inscritos y de puntajes sacamos **las variables asociadas a la persona**: notas, ranking, puntajes, sexo, ingreso. Y como cada estudiante viene de un colegio, con el **RBD** construimos **variables asociadas al colegio**.
> El archivo de postulaciones tiene 1,7 millones de filas porque cada alumno postula a varias carreras; lo dejamos en una fila por estudiante. Con eso **llegamos al N**, que les muestra mi compañero.

*Pasas la palabra para la lámina 4.*

---

## Lámina 9 · Descriptivas (25 s)

*Entras después de la lámina 8.*

> Los descriptivos ya **son coherentes con lo que esperamos a priori**.
> La mediana del promedio de notas es 6,23: los que postulan son estudiantes de buen rendimiento, y por eso el puntaje debería pesar en quedar arriba.
> Y hay 55 % de mujeres: como ellas tienen mejor NEM pero los hombres más puntaje en matemática, **el signo del sexo no es obvio**, y es algo que el modelo tiene que resolver.

---

## Lámina 10 · Conclusiones (40 s)

> En resumen: **llegamos al N de 108.251**, que es la población completa de egresados 2025 que postularon por la vía regular. La Y queda equilibrada, 56 contra 44, porque incluimos a los no matriculados.
> Para la Etapa 2 **no nos vamos a quedar con las variables disponibles**: vamos a ir al **MINEDUC y cruzar por RBD** para traer **matrícula del colegio, número de cursos y ratio estudiantes por profesor**, que nos dicen si el colegio es grande o chico y cuánta atención recibe cada alumno.
> Para medir el entorno preferimos el colegio antes que la comuna, porque **las comunas son muy heterogéneas**: dentro de una misma comuna hay realidades muy distintas, y el colegio describe mejor el entorno del estudiante.

*Pasas a la lámina 11: «Muchas gracias, ¿preguntas?».*

---

## Si te preguntan

**¿Por qué dicen que es población y no muestra?**
> Porque están todos los que cumplen los criterios, no una parte elegida al azar. No hay error muestral.

**¿Por qué full join?**
> Para no perder a nadie al unir: los no matriculados no aparecen en el archivo de matrícula, y los necesitamos para la Y = 0.

**¿Qué signo esperan de las variables del MINEDUC?**
> El ratio estudiantes por profesor, negativo: menos atención por alumno. El tamaño del colegio, ambiguo: más recursos, pero menos atención.
