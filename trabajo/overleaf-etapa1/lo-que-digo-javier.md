# Lo que digo yo (Javier)

## Lámina 3 · Fuentes de datos

> Los datos vienen de cuatro archivos públicos del DEMRE, del proceso de admisión 2026.
> Y esto **no es una muestra: es la población completa**.
> **La unidad es la persona.** Cada estudiante tiene un identificador anonimizado, el ID_aux, y con esa llave unimos los cuatro archivos.
> Así tenemos **variables asociadas a la persona**: el promedio de notas, el ranking, los puntajes, el sexo y el ingreso.
> Pero **esa persona estudió en un colegio**, y cada colegio tiene un **RBD**, que es su identificador único del MINEDUC. Agrupando por RBD construimos **variables asociadas al colegio**.
> El archivo de postulaciones tiene 1,7 millones de filas, porque cada alumno postula a varias carreras; lo dejamos en una fila por estudiante.
> Con eso armamos la población y **llegamos al N**, que les muestra mi compañero.

## Lámina 9 · Descriptivas (solo si sigue en la presentación)

> Acá están las **variables asociadas a la persona**, como el **promedio de notas** y el **género**.
> La mediana de notas es 6,23: postulan estudiantes de buen rendimiento, y **sin haber hecho todavía el modelo** esperamos que el puntaje suba la probabilidad de quedar arriba.
> Y hay 55 % de mujeres. Ellas tienen mejor NEM y los hombres más puntaje en matemática, así que el efecto del género no es obvio: lo tiene que decidir el modelo.

## Lámina 10 · Conclusiones

> En resumen, el objetivo de esta etapa era **armar una base de datos con la población que corresponde**, y **llegamos a un N de 108.251**.
> La Y es **el complemento**: vale 1 si quedó en sus tres primeras preferencias, y 0 **todos los que no están dentro de eso**, incluidos los que no se matricularon. Queda en 56 contra 44.
> Para la Etapa 2 **no nos vamos a quedar con los mínimos**. Vamos a **ir al MINEDUC y cruzar por RBD** para traer la **matrícula del colegio, cuántos cursos tiene y el ratio de estudiantes por profesor**. Eso nos dice si el colegio **es muy grande o muy chico**, y puede **ayudarnos a predecir la probabilidad de que el estudiante se matricule**.
> Preferimos el colegio antes que la comuna, porque **las comunas son muy heterogéneas**.

## Lámina 11 · Cierre

> Muchas gracias. ¿Preguntas?


---

# Todas las preguntas que podría hacer el profe

Respuestas cortas: una o dos frases. Si no sabes algo, di «lo vemos en la Etapa 2» en vez de improvisar.

## A. Población y N

**¿Por qué es población y no muestra?**
> Porque están todos los que cumplen los criterios, no una parte al azar. No hay error muestral.

**¿De dónde sale el 108.251?**
> De 317.700 registros: egresados 2025 regulares, 218.066; postularon por vía regular, 114.865; filtro de matrícula, 108.598; con NEM, 108.251.

**¿Por qué solo egresados 2025?**
> Para comparar estudiantes del mismo proceso, que compiten en las mismas condiciones. Los de promociones anteriores tienen otra trayectoria (preuniversitario, otro intento).

**¿Por qué sacaron a los matriculados por otra vía?**
> Porque no compitieron por sus preferencias en el proceso regular, así que no responden la pregunta.

**¿Por qué sacaron a los que tenían NEM igual a 0?**
> Sin NEM no hay puntaje de postulación válido; eran solo 345.

**¿Y los que rindieron y no postularon?**
> Quien no postuló no ordenó preferencias, así que no participa del evento que modelamos. Incluirlos mezclaría dos decisiones: postular o no, y dónde quedar. Si prefiere que los incluyamos, los agregamos en la Etapa 2.

**¿Por qué full join?**
> Para no perder a nadie al unir: los no matriculados no están en el archivo de matrícula, y los necesitamos para la Y = 0.

**¿Cuál es la unidad de análisis?**
> La persona, identificada por el ID_aux anonimizado.

## B. Variable de respuesta

**¿Cómo definieron la Y?**
> 1 si se matriculó en su preferencia 1, 2 o 3; 0 el complemento: preferencia 4 o más abajo, o no matriculado.

**¿Por qué incluyen a los no matriculados en el 0?**
> Postularon y no quedaron arriba. Sacarlos dejaría solo a los que tuvieron éxito y sobrestimaría la probabilidad.

**¿Por qué el corte en la tercera preferencia y no en la primera?**
> Fue la definición del trabajo. Además, con solo la primera, el 1 incluiría a pocos y perderíamos a los que igual quedaron en algo que valoraban mucho.

**¿La Y está balanceada?**
> Sí: 55,7 contra 44,3. Sin los no matriculados era 88 contra 12, y eso complicaba evaluar el modelo.

**¿Por qué importa que esté balanceada?**
> Porque con una Y muy desbalanceada el modelo puede acertar mucho solo prediciendo siempre 1, y el porcentaje correctamente predicho engaña.

## C. Variables creadas

**¿Qué es el RBD?**
> El identificador único de cada colegio que asigna el MINEDUC. Con él agrupamos a los estudiantes por colegio, y en la Etapa 2 lo usamos para traer datos del MINEDUC.

**¿Por qué calcularon las variables del colegio antes de filtrar?**
> Para que describan al colegio completo, no solo a los alumnos que quedaron en nuestra base.

**¿Por qué la mediana en INGRESO_COLEGIO y no el promedio?**
> El tramo es ordinal, del 1 al 10, y la mediana no se deja llevar por pocos alumnos en los extremos.

**¿Por qué el código 99 pasa a NA y no borran la fila?**
> Son 29.199 estudiantes, el 27 %. Borrarlos achica la base y saca a un grupo que puede ser distinto. En la Etapa 2 evaluamos tratarlos como un tramo más.

**N_MATRICULADOS incluye al propio estudiante, ¿no es circular?**
> Buena observación: el estudiante aporta a su propio colegio. En la Etapa 2 la vamos a usar como tasa, matriculados sobre inscritos, y se puede calcular excluyendo al propio estudiante.

**¿Qué son PACE y BEA?**
> PACE es un programa que da cupos garantizados en universidades a estudiantes de liceos vulnerables. BEA es la Beca de Excelencia Académica, para el 10 % mejor de cada curso.

**¿Por qué TP es una dummy aparte?**
> Porque la formación técnica prepara distinto para la PAES y muchos egresados siguen a un CFT; es un perfil distinto.

## D. Efecto a priori

**¿Qué signo esperan del NEM y los puntajes?**
> Positivo: suben el puntaje ponderado y abren más carreras, así que es más probable alcanzar el corte de las primeras preferencias.

**¿Y del ingreso?**
> Positivo, por recursos para prepararse y pagar. Pero con la gratuidad podría pesar menos de lo esperado; eso lo mide el modelo.

**¿Por qué TP negativo?**
> Prepara menos para la PAES y más para la salida a CFT o al trabajo.

**¿Por qué el sexo tiene signo «?»?**
> Dos efectos opuestos: las mujeres tienen mejor NEM y ranking; los hombres, más puntaje en matemática.

**¿Por qué el tamaño del colegio es «?»?**
> Un colegio grande puede tener más recursos, pero menos atención por alumno.

**¿Qué signo esperan del ratio estudiantes por profesor?**
> Negativo: más alumnos por profesor es menos atención por alumno.

**¿Y de la ruralidad?**
> Negativo: menos acceso a preparación y a oferta universitaria cercana.

## E. Variables que no pueden ser X

**¿Por qué no usan PREFERENCIA?**
> Con ella se construye la Y: sería explicar la Y con la misma Y.

**¿Por qué no PTJE_POND?**
> Es el puntaje con que ya quedó en una carrera: es consecuencia del resultado, no causa.

**¿Por qué no VIA ni TIPO_MATRICULA?**
> Están vacías en los 39.548 no matriculados, y además describen la matrícula, que es el resultado.

## F. Modelo (Etapa 3, por si acaso)

**¿Por qué logit y no MCO (modelo de probabilidad lineal)?**
> Porque con MCO la probabilidad estimada puede salir menor que 0 o mayor que 1. El logit la transforma con la función logística y la deja entre 0 y 1.

**¿Cómo se interpreta un coeficiente del logit?**
> El signo dice la dirección del efecto. La magnitud no se lee directo: hay que calcular el efecto parcial, que depende de los valores de las X.

**¿Cómo se calcula el efecto parcial de una dummy?**
> Como la diferencia de probabilidad entre que la variable valga 1 y que valga 0, dejando las demás fijas.

**¿Se pueden comparar los coeficientes del logit, el probit y MCO?**
> No: cada modelo mide en una escala distinta. Lo que se compara son los efectos parciales.

**¿Cómo van a evaluar el modelo?**
> Con la matriz de confusión y el porcentaje correctamente predicho, mirando aciertos en los 1 y en los 0.
