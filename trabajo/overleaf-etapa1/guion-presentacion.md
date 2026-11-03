# Guion: Econometría II, Etapa 1 (jue 15-10, 08:15)

**Duración:** apuntar a 8 min 30 s. El profe corta en el minuto 10.
**Ritmo:** ~130 palabras por minuto. Cada bloque está escrito para decirse, no para leerse: apréndanse las ideas y las cifras en negrita, no las frases exactas.

| Bloque | Láminas | Quién | Tiempo |
|---|---|---|---|
| A. Pregunta, datos y N | 1 a 4 | _____ | 2:30 |
| B. Variable Y y variables creadas | 5 y 6 | _____ | 2:00 |
| C. Efecto a priori y variables que no son X | 7 y 8 | _____ | 3:00 |
| D. Descriptivas y cierre | 9 a 11 | _____ | 1:00 |

El bloque C es el que más pesa en la nota: que lo tome quien mejor explique el porqué de cada signo.

---

## Bloque A · Láminas 1 a 4 · 2:30

**Lámina 1, portada (10 s)**
> Buenos días. Somos David Cuevas, Javier Li-Yau, Benjamín Lizana y Ana Nacif, y vamos a presentar la Etapa 1: la construcción de la base de datos con la Admisión 2026.

**Lámina 2, objetivo (40 s)**
> Nuestra pregunta es: ¿de qué depende que un estudiante se matricule en una de sus **tres primeras preferencias**?
> Para responderla armamos una base con **108.251 estudiantes**. No es una muestra: es **toda la población** que cumple nuestros filtros, los egresados 2025 que postularon por la vía regular.
> De ellos, **60.300, el 55,7 %**, quedaron en sus tres primeras preferencias. Los otros **47.951, el 44,3 %**, quedaron en la cuarta o más abajo, o no se matricularon.
> Esta base es la que vamos a usar en la Etapa 3 para estimar un modelo logit.

**Lámina 3, fuentes (40 s)**
> Todo viene del portal del DEMRE, de cuatro archivos públicos: el de inscritos, el de notas y puntajes, el de postulaciones y el de matrícula.
> Los unimos por el identificador del estudiante, el ID_aux.
> El archivo de postulaciones tiene **1,7 millones de filas** porque cada alumno postula a varias carreras; lo dejamos en **una fila por estudiante** antes de unirlo.

**Lámina 4, embudo (60 s)**
> Partimos con **317.700** registros.
> Primero nos quedamos con los egresados 2025 que eran alumnos regulares: quedan **218.066**.
> Después, con los que postularon al menos a una carrera por la vía regular: **114.865**.
> Luego el filtro de matrícula: mantenemos a los que no se matricularon y, de los matriculados, solo los de vía regular y tipo de matrícula 1. Quedan **108.598**.
> Por último sacamos a quienes no tenían puntaje NEM. Llegamos a nuestro **N final: 108.251**.

---

## Bloque B · Láminas 5 y 6 · 2:00

**Lámina 5, variable Y (60 s)**
> Nuestra variable de respuesta es PREF_TOP3_DUMMY. Vale **1** si el estudiante se matriculó en su primera, segunda o tercera preferencia, y **0** en el resto: si quedó en la cuarta o más abajo, **o si no se matriculó**.
> Incluimos a los no matriculados a propósito: también postularon y no lograron quedar arriba. Si los dejáramos fuera, solo miraríamos a los que tuvieron éxito en matricularse.
> En el 1 hay **60.300**: la mayoría, **40.002**, quedó en su primera preferencia. En el 0 hay **47.951**: **8.403** quedaron en la cuarta o más abajo y **39.548** no se matricularon.
> Así la variable queda bastante equilibrada, 56 contra 44.

**Lámina 6, variables creadas (60 s)**
> Además de la Y creamos dos tipos de variables.
> A nivel de **colegio**, usando el RBD: **N_ALUMNOS**, cuántos inscritos tiene el colegio; **INGRESO_COLEGIO**, la mediana del tramo de ingreso de sus alumnos; y **N_MATRICULADOS**, cuántos de sus alumnos se matricularon por vía regular. Las calculamos con todos los inscritos del colegio, antes de filtrar, para que reflejen al colegio completo.
> A nivel del **estudiante**, dummies: **TP_DUMMY**, si viene de un colegio técnico profesional, que son **18.877**; y **PACE** y **BEA**, si fue preseleccionado en esos programas.
> Y un ajuste: el código **99** del ingreso familiar significa que no respondió, así que lo pasamos a NA. Son **29.199** casos.

---

## Bloque C · Láminas 7 y 8 · 3:00

**Lámina 7, efecto esperado a priori (2:00)**
> Antes de estimar nada, ¿qué esperamos de cada variable?
> **Rendimiento:** NEM, ranking, lectora y matemática deberían tener signo **positivo**. Más puntaje sube el puntaje ponderado y abre más carreras, así que es más probable alcanzar el corte de las que uno puso primero. BEA también positivo: es el 10 % mejor del curso y trae beca. PACE, positivo, porque da cupos garantizados.
> **Socioeconómico:** el ingreso per cápita y el ingreso del colegio, **positivos**: más recursos para prepararse y para pagar. Aunque con la **gratuidad** este efecto podría ser más chico de lo que uno piensa, y eso es justamente algo que el modelo va a medir.
> El colegio técnico profesional lo esperamos **negativo**: prepara menos para la PAES y muchos egresados siguen hacia un CFT o al trabajo.
> **Colegio:** N_MATRICULADOS positivo, porque refleja una cultura de seguir estudiando.
> Y hay dos que dejamos con **signo abierto**. El tamaño del colegio: más grande puede significar más recursos, pero también menos atención por alumno. Y el sexo: las mujeres tienen en promedio mejor NEM, los hombres mejor puntaje en matemática, así que a priori no sabemos hacia dónde va.

**Lámina 8, variables que no pueden ser X (60 s)**
> Hay cuatro variables que están en la base pero **no pueden usarse como explicativas**.
> PREFERENCIA, porque con ella construimos la Y. El puntaje ponderado, porque es el de la carrera en que ya quedó: es un resultado, no una causa. Y la vía y el tipo de matrícula, porque están vacías para los **39.548** que no se matricularon.
> Usarlas sería explicar la Y con la misma Y. Las dejamos en la base solo como información.

---

## Bloque D · Láminas 9 a 11 · 1:00

**Lámina 9, descriptivas (20 s)**
> Acá está el resumen de la base final. Solo destacamos que el promedio de notas mediano es **6,23** y que hay más mujeres que hombres: **55,2 %** frente a **44,8 %**.

**Lámina 10, conclusiones (35 s)**
> En resumen: tenemos una base de **108.251** estudiantes, armada con cuatro archivos del DEMRE, con una variable de respuesta equilibrada.
> En la Etapa 2 vamos a cruzar cada X con la Y y a traer variables del **MINEDUC** por RBD, como ruralidad o alumnos por profesor. También vamos a evaluar tratar a los que no respondieron el ingreso como un tramo más, para no perder esas observaciones.

**Lámina 11 (5 s)**
> Muchas gracias. ¿Preguntas?

---

## Preguntas probables

**¿Por qué incluyen a los que no se matricularon?**
> Porque postularon y no quedaron en sus tres primeras preferencias. Dejarlos fuera sería mirar solo a los que se matricularon, y el modelo sobrestimaría la probabilidad de éxito.

**¿Y los que rindieron la PAES pero no postularon?** → mostrar la lámina de respaldo (tecla Fin).
> La pregunta es en qué preferencia quedó el estudiante. Quien no postuló no ordenó preferencias, así que no participa de ese evento. Si se incluyeran, la Y mezclaría dos decisiones: postular o no, y dónde quedar. Si usted prefiere que los incluyamos, los agregamos en la Etapa 2.

**¿De dónde sale el 108.251?**
> Volver a la lámina 4 y recorrer el embudo: 317.700 → 218.066 → 114.865 → 108.598 → 108.251.

**¿Por qué el sexo tiene signo "?"?**
> Porque hay dos efectos opuestos: las mujeres tienen mejor NEM y ranking, los hombres mejor puntaje en matemática. Cuál pesa más es algo que tiene que decir el modelo.

**¿Por qué la mediana y no el promedio en INGRESO_COLEGIO?**
> El tramo de ingreso es una variable ordinal, del 1 al 10, y la mediana no se deja llevar por pocos alumnos en los extremos.

**¿Por qué el código 99 pasa a NA y no se elimina la fila?**
> Porque son casi 30 mil estudiantes. Eliminarlos achicaría mucho la base y sacaría a un grupo que puede ser distinto. En la Etapa 2 evaluamos tratarlo como un tramo más.

---

## Antes de entrar
- [ ] Ensayo completo con cronómetro (meta: menos de 9 min).
- [ ] Cada uno sabe en qué lámina entra y quién le pasa la palabra.
- [ ] PDF en el computador y en un pendrive o correo, por si falla el proyector.
- [ ] Escuchar el audio del 08-10 en el minuto 55:43.
