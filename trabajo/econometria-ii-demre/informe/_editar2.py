"""Genera informe-etapa-1-finalfinal.tex desde informe-etapa-1-final.tex:
ediciones del grupo (PDF finalfinal) + cifras del R corregido (68.703 x 30)."""
import pathlib, sys

aqui = pathlib.Path(__file__).parent
src = (aqui / "informe-etapa-1-final.tex").read_text(encoding="utf-8")

R = []  # (viejo, nuevo)

# --- 1 Introducción --------------------------------------------------
R.append(("""base de 60.544 estudiantes que egresaron de enseñanza media en 2025 y
que se matricularon por vía regular, con tipo de matrícula postulación
regular, a lo más en su tercera preferencia. Ese filtro deja a todos
dentro de sus tres primeras opciones, así que por sí solo no permite
distinguirlos. Lo que sí cambia de uno a otro es en cuál de las tres
quedaron: 40.173 (66,4\\,\\%) lograron la primera y 20.371 (33,6\\,\\%) se
matricularon en la segunda o la tercera. Nuestro trabajo apunta a
explicar de qué depende quedar en la primera preferencia, y esa división
es la variable de respuesta, \\texttt{PREF\\_PRIMERA\\_DUMMY}.

La base tiene una fila por estudiante y 29 variables.""",
"""base de 68.703 estudiantes que egresaron de enseñanza media en 2025 como
alumnos regulares y que se matricularon por vía regular, con tipo de
matrícula postulación regular. De ellos, 60.300 (87,8\\,\\%) se
matricularon en una de sus tres primeras preferencias y 8.403
(12,2\\,\\%) en la cuarta o más abajo. Nuestro trabajo apunta a explicar
de qué depende matricularse dentro de las tres primeras preferencias.

La base tiene una fila por estudiante y 30 variables."""))
R.append(("""nosotros: inscritos en la PAES, matriculados y promedio del tramo de
ingreso de sus inscritos.""",
"""nosotros: inscritos en la PAES, matriculados y mediana del tramo de
ingreso de sus inscritos."""))

# --- 3.1 Variables del colegio --------------------------------------
R.append(("""  \\item Del archivo B: número de inscritos del colegio y promedio del
        ingreso per cápita familiar de sus inscritos.""",
"""  \\item Del archivo B: número de inscritos del colegio y mediana del
        tramo de ingreso per cápita familiar de sus inscritos."""))
R.append(("""        matriculados quedan con 0.
\\end{itemize}
""",
"""        matriculados quedan con 0.
\\end{itemize}

Antes de agrupar hicimos dos ajustes. Primero, el código 99 de
\\texttt{INGRESO\\_PERCAPITA\\_GRUPO\\_FA} («prefiero no responder») se
convierte en dato faltante (\\texttt{NA}) apenas se lee el archivo B, para
que no entre en el cálculo del colegio. Segundo, los inscritos sin
\\texttt{RBD} no se agrupan: si se agruparan, R los trataría como un solo
colegio que no existe.
"""))

# --- 3.3 Filtros -----------------------------------------------------
R.append(("""        media en 2025 (\\texttt{ANYO\\_EGRESO} igual a 2025).
  \\item \\textbf{Vía y tipo de matrícula:}""",
"""        media en 2025 (\\texttt{ANYO\\_EGRESO} igual a 2025).
  \\item \\textbf{Alumno regular:} egresados de la promoción del año como
        alumnos regulares de un colegio chileno
        (\\texttt{SITUACION\\_EGRESO} igual a 1). Quedan fuera quienes
        validaron estudios o vienen del extranjero.
  \\item \\textbf{Vía y tipo de matrícula:}"""))
R.append(("""        a 1).
  \\item \\textbf{Preferencia:} matriculados en su primera, segunda o
        tercera preferencia (\\texttt{PREFERENCIA} entre 1 y 3).
\\end{enumerate}""",
"""        a 1).
\\end{enumerate}

No filtramos por preferencia: la preferencia en que se matriculó cada
estudiante es la que define la variable de respuesta (sección 4)."""))

# --- 3.4 Observaciones ----------------------------------------------
R.append(("""Egresados en 2025 & 218.989 \\\\
Vía regular y tipo de matrícula 1 & 69.004 \\\\
Inscribieron alguna prueba del proceso 2026 & 69.002 \\\\
Matriculados en preferencia 1 a 3 & 60.558 \\\\
\\rowcolor{yellow!30}
\\textbf{Con puntaje NEM distinto de 0 (base final)} & \\textbf{60.544} \\\\
\\bottomrule
\\end{tabular}
\\end{center}
""",
"""Egresados en 2025 & 218.989 \\\\
Alumnos regulares de la promoción del año & 218.066 \\\\
Vía regular y tipo de matrícula 1 & 68.704 \\\\
Inscribieron alguna prueba del proceso 2026 & 68.703 \\\\
\\rowcolor{yellow!30}
\\textbf{Con puntaje NEM distinto de 0 (base final)} & \\textbf{68.703} \\\\
\\bottomrule
\\end{tabular}
\\end{center}

El filtro de puntaje NEM no saca a nadie: todos los alumnos regulares
que quedan tienen NEM.
"""))

# --- 4 Variable de respuesta ----------------------------------------
R.append(("""Por los filtros, todos los estudiantes de la base se matricularon en una
de sus tres primeras preferencias. Por eso la variable de respuesta separa
a quienes quedaron en su primera preferencia de quienes quedaron en la
segunda o la tercera:

\\[
\\texttt{PREF\\_PRIMERA\\_DUMMY}_i =
\\begin{cases}
1 & \\text{si se matriculó en su primera preferencia} \\\\[4pt]
0 & \\text{si se matriculó en su segunda o tercera preferencia}
\\end{cases}
\\]""",
"""La variable de respuesta separa a quienes se matricularon en una de sus
tres primeras preferencias de quienes quedaron más abajo:

\\[
\\texttt{PREF\\_TOP3\\_DUMMY}_i =
\\begin{cases}
1 & \\text{si se matriculó en su primera, segunda o tercera preferencia} \\\\[4pt]
0 & \\text{si se matriculó en su cuarta preferencia o más abajo}
\\end{cases}
\\]"""))
R.append(("""1 (primera preferencia) & 40.173 & 66,4\\% \\\\
0 (segunda o tercera)   & 20.371 & 33,6\\% \\\\
\\midrule
\\textbf{Total} & \\textbf{60.544} & 100\\% \\\\""",
"""1 (preferencia 1 a 3)        & 60.300 & 87,8\\% \\\\
0 (preferencia 4 o más abajo) &  8.403 & 12,2\\% \\\\
\\midrule
\\textbf{Total} & \\textbf{68.703} & 100\\% \\\\"""))
R.append(("""De los 20.371 que no quedaron en su primera preferencia, 13.322 se
matricularon en la segunda y 7.049 en la tercera.""",
"""De los 60.300 con valor 1, 40.002 quedaron en la primera preferencia,
13.270 en la segunda y 7.028 en la tercera. De los 8.403 con valor 0,
3.339 quedaron en la cuarta, 1.881 en la quinta y el resto se reparte
entre la sexta y la vigésima. La variable está desbalanceada: cerca de
9 de cada 10 estudiantes tienen valor 1, lo que habrá que considerar al
evaluar el porcentaje correctamente predicho del modelo."""))

# --- 5.1 Variables del establecimiento -------------------------------
R.append(("""  \\item \\texttt{INGRESO\\_COLEGIO}: promedio de
        \\texttt{INGRESO\\_PERCAPITA\\_GRUPO\\_FA} de los inscritos del
        colegio. El promedio incluye el código 99 («prefiero no
        responder»), así que no queda en la escala de 1 a 10 de los
        tramos: su promedio es 31,8 (sección 8).""",
"""  \\item \\texttt{INGRESO\\_COLEGIO}: mediana de
        \\texttt{INGRESO\\_PERCAPITA\\_GRUPO\\_FA} de los inscritos del
        colegio, sin contar a quienes respondieron 99. Usamos la mediana
        y no el promedio porque los tramos son una escala ordinal de
        ancho desigual: el último tramo es abierto hacia arriba, y
        promediar los números de los tramos supondría que la distancia
        entre ellos es siempre la misma. La variable queda en la escala de 1 a
        10; cuando un colegio tiene un número par de respuestas, la
        mediana puede terminar en ,5."""))
R.append(("""Los 244 estudiantes sin colegio de egreso registrado (sección 6) quedan
agrupados en el cálculo como si fueran un solo colegio, con 3.169
inscritos y 902 matriculados. Para ellos estas tres variables no
describen un establecimiento real. Sin ese grupo, el colegio más grande
tiene 947 inscritos y 447 matriculados.""",
"""Los inscritos sin \\texttt{RBD} quedan fuera de este cálculo (sección
3.1). En la base final no hay ninguno: casi todos los que no tienen
colegio registrado validaron estudios o vienen del extranjero, y salen con
el filtro de alumno regular. El colegio más grande tiene 947 inscritos y
447 matriculados."""))

# --- 5.2 Dummies -----------------------------------------------------
R.append(("""  \\item \\texttt{PREF\\_PRIMERA\\_DUMMY}: variable de respuesta (sección 4).
  \\item \\texttt{TP\\_DUMMY}: 1 si el colegio es técnico profesional
        (rama T1 a T5), 0 si no. Hay 9.110 estudiantes de colegios
        técnico profesionales y 51.434 del resto. Entre esos 51.434 están los
        244 sin colegio registrado, que quedan con 0 aunque no se conoce
        su rama.""",
"""  \\item \\texttt{PREF\\_TOP3\\_DUMMY}: variable de respuesta (sección 4).
  \\item \\texttt{TP\\_DUMMY}: 1 si el colegio es técnico profesional
        (rama T1 a T5), 0 si no, y sin valor si no se conoce la rama.
        Hay 10.566 estudiantes de colegios técnico profesionales y 58.137
        del resto.
  \\item \\texttt{PACE} y \\texttt{BEA}: en el archivo B vienen con texto
        para los preseleccionados y vacías para el resto. Las
        convertimos en dummies: 1 si fue preseleccionado y 0 si no. Hay
        5.697 preseleccionados PACE y 7.301 BEA."""))

# --- 6 Datos sin información ----------------------------------------
R.append(("""\\textbf{Variable} & \\textbf{Casos} & \\textbf{Qué significa} \\\\
\\midrule
\\texttt{RBD}, \\texttt{RAMA\\_EDUCACIONAL}, \\texttt{GRUPO\\_DEPENDENCIA},
\\texttt{CODIGO\\_COMUNA} & 244 & Estudiante sin colegio de egreso registrado. \\\\
\\texttt{CODIGO\\_REGION} & 10 & Región del colegio sin dato. \\\\
\\texttt{PACE} & 55.382 & No fue preseleccionado PACE. \\\\
\\texttt{BEA} & 53.805 & No fue preseleccionado a la Beca de Excelencia Académica. \\\\
\\texttt{INGRESO\\_PERCAPITA\\_GRUPO\\_FA} igual a 99 & 16.235 & «Prefiero no responder». \\\\""",
"""\\textbf{Variable} & \\textbf{Casos} & \\textbf{Qué hicimos} \\\\
\\midrule
\\texttt{INGRESO\\_PERCAPITA\\_GRUPO\\_FA} igual a 99 & 18.409 & Es «prefiero no responder», no un tramo: lo convertimos en \\texttt{NA}. \\\\
\\texttt{PACE} vacía & 63.006 & No fue preseleccionado: lo codificamos como 0. \\\\
\\texttt{BEA} vacía & 61.402 & No fue preseleccionado: lo codificamos como 0. \\\\
\\texttt{RBD} y variables del colegio & 0 & Los estudiantes sin colegio salen con el filtro de alumno regular y no entran al cálculo de las variables del colegio. \\\\"""))
R.append(("""En el resto de las variables no hay datos faltantes. Para los 244
estudiantes sin colegio, sin embargo, \\texttt{N\\_ALUMNOS},
\\texttt{INGRESO\\_COLEGIO}, \\texttt{N\\_MATRICULADOS} y \\texttt{TP\\_DUMMY}
tienen valores que no corresponden a un colegio (sección 5).""",
"""Después de estos ajustes, la única variable con datos faltantes es
\\texttt{INGRESO\\_PERCAPITA\\_GRUPO\\_FA}, con 18.409 casos (26,8\\,\\% de
la base). Si se deja así, el logit descartaría a esos estudiantes; para
la Etapa 3 evaluaremos tratar «prefiero no responder» como una categoría
más del tramo de ingreso."""))

# --- 7 Definición de las variables -----------------------------------
R.append(("""\\texttt{PREF\\_PRIMERA\\_DUMMY} & Creada & Variable de respuesta: 1 si se matriculó en su primera preferencia, 0 si en la segunda o tercera. \\\\""",
"""\\texttt{PREF\\_TOP3\\_DUMMY} & Creada & Variable de respuesta: 1 si se matriculó en una de sus tres primeras preferencias, 0 si en la cuarta o más abajo. \\\\"""))
R.append(("""Mes y año de nacimiento (MMAAAA). Es numérica, así que los meses 1 a 9 quedan sin el cero inicial: 42006 es abril de 2006. \\\\""",
"""Mes y año de nacimiento, en formato MMAAAA. \\\\"""))
R.append(("""de 1 a 10; 99 es «prefiero no responder». \\\\""",
"""de 1 a 10. El 99 («prefiero no responder») se convirtió en \\texttt{NA}. \\\\"""))
R.append(("""\\texttt{PACE} & B & Preseleccionado PACE por el MINEDUC. \\\\
\\texttt{BEA} & B & Preseleccionado a la Beca de Excelencia Académica. \\\\
\\texttt{ANYO\\_EGRESO} & B & Año de egreso de enseñanza media (2025 en toda la base). \\\\""",
"""\\texttt{PACE} & B & 1 si fue preseleccionado PACE por el MINEDUC, 0 si no. \\\\
\\texttt{BEA} & B & 1 si fue preseleccionado a la Beca de Excelencia Académica, 0 si no. \\\\
\\texttt{ANYO\\_EGRESO} & B & Año de egreso de enseñanza media (2025 en toda la base). \\\\
\\texttt{SITUACION\\_EGRESO} & B & Situación de egreso (1, promoción del año, alumno regular, en toda la base). \\\\"""))
R.append(("""Preferencia en que se matriculó (1 a 3 en la base).""",
"""Preferencia en que se matriculó (1 a 20 en la base)."""))
R.append(("""Promedio de \\texttt{INGRESO\\_PERCAPITA\\_GRUPO\\_FA} de los inscritos del colegio, incluido el código 99. \\\\""",
"""Mediana de \\texttt{INGRESO\\_PERCAPITA\\_GRUPO\\_FA} de los inscritos del colegio, sin el código 99. \\\\"""))

# --- 8 Base final ----------------------------------------------------
R.append(("""\\textbf{60.544 filas y 29
columnas}""", """\\textbf{68.703 filas y 30
columnas}"""))
R.append(("""Los estudiantes vienen de 3.108 colegios distintos.""",
"""Los estudiantes vienen de 3.125 colegios distintos."""))
R.append(("""\\texttt{PROMEDIO\\_NOTAS}   & 4,50  & 6,33  & 6,27  & 7,00 \\\\
\\texttt{PTJE\\_NEM}         & 259   & 808   & 792   & 1.000 \\\\
\\texttt{PTJE\\_RANKING}     & 259   & 822   & 806   & 1.000 \\\\
\\texttt{CLEC\\_REG\\_ACTUAL} & 316   & 663   & 667   & 1.000 \\\\
\\texttt{MATE1\\_REG\\_ACTUAL}& 320   & 682   & 698   & 1.000 \\\\
\\texttt{PTJE\\_POND}        & 354,6 & 716,1 & 718,6 & 998,4 \\\\
\\texttt{N\\_ALUMNOS}        & 8     & 127   & 172   & 3.169 \\\\
\\texttt{INGRESO\\_COLEGIO}  & 1,0   & 29,7  & 31,8  & 94,1 \\\\
\\texttt{N\\_MATRICULADOS}   & 1     & 55    & 74    & 902 \\\\""",
"""\\texttt{PROMEDIO\\_NOTAS}   & 4,50  & 6,30  & 6,25  & 7,00 \\\\
\\texttt{PTJE\\_NEM}         & 259   & 799   & 786   & 1.000 \\\\
\\texttt{PTJE\\_RANKING}     & 259   & 814   & 801   & 1.000 \\\\
\\texttt{CLEC\\_REG\\_ACTUAL} & 316   & 663   & 663   & 1.000 \\\\
\\texttt{MATE1\\_REG\\_ACTUAL}& 320   & 672   & 694   & 1.000 \\\\
\\texttt{PTJE\\_POND}        & 354,6 & 710,7 & 713,6 & 998,4 \\\\
\\texttt{N\\_ALUMNOS}        & 8     & 127   & 162   & 947 \\\\
\\texttt{INGRESO\\_COLEGIO}  & 1,0   & 4,0   & 4,9   & 10,0 \\\\
\\texttt{N\\_MATRICULADOS}   & 1     & 55    & 71    & 447 \\\\"""))
R.append(("""En la base hay 31.981 mujeres (52,8\\%) y 28.563 hombres (47,2\\%).""",
"""En la base hay 36.237 mujeres (52,7\\%) y 32.466 hombres (47,3\\%)."""))

# --- 9 Conclusión (redacción del grupo, cifras nuevas) --------------
R.append(("""La base final tiene 60.544 estudiantes, uno por fila: el 66,4\\,\\% quedó
en su primera preferencia y el 33,6\\,\\% en la segunda o la tercera. Como
todos cumplen los mismos filtros, esa diferencia se estudiará con sus
notas, sus puntajes, su ingreso familiar y las variables de su colegio.
\\texttt{PREFERENCIA} y \\texttt{PTJE\\_POND} quedan fuera del modelo porque
dependen del resultado. Antes de estimar hay que recalcular
\\texttt{INGRESO\\_COLEGIO} sin el código 99 y dejar sin valor las
variables del colegio de los 244 estudiantes sin \\texttt{RBD}.""",
"""La construcción de la base de datos permitió integrar en un único data
frame la información académica, socioeconómica, de postulación, matrícula
y establecimiento educacional de los estudiantes participantes del
proceso de admisión 2026.

Luego de aplicar los filtros establecidos en el trabajo, la muestra final
quedó compuesta por 68.703 estudiantes egresados de enseñanza media en
2025 como alumnos regulares, matriculados por vía regular y bajo
postulación regular. Asimismo, se incorporaron variables construidas a
nivel de establecimiento y variables dummy que permitirán facilitar el
análisis econométrico posterior. Los problemas de la base se corrigieron
antes de construirlas: el código 99 del ingreso se convirtió en
\\texttt{NA}, el ingreso del colegio se calcula con la mediana y los
estudiantes sin colegio registrado no forman un colegio ficticio.

La variable de respuesta definida corresponde a
\\texttt{PREF\\_TOP3\\_DUMMY}, la cual identifica si el estudiante logró
matricularse en una de sus tres primeras preferencias o quedó en la
cuarta o más abajo. En la base final, un 87,8\\,\\% de los estudiantes se
matriculó dentro de sus tres primeras preferencias, mientras que un
12,2\\,\\% lo hizo más abajo.

En términos generales, la base construida cumple con las condiciones
establecidas para esta primera etapa y entrega una estructura adecuada
para avanzar hacia el análisis descriptivo y la posterior estimación de
un modelo Logit, con el objetivo de estudiar qué características
individuales, académicas y del establecimiento influyen en la
probabilidad de matricularse dentro de las tres primeras preferencias."""))

out = src
for i, (viejo, nuevo) in enumerate(R, 1):
    n = out.count(viejo)
    if n != 1:
        sys.exit(f"reemplazo {i}: encontrado {n} veces:\n{viejo[:120]}")
    out = out.replace(viejo, nuevo)

(aqui / "informe-etapa-1-finalfinal.tex").write_text(out, encoding="utf-8")
print(f"ok: {len(R)} reemplazos")
