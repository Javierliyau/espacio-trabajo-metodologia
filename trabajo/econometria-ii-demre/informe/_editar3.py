"""Genera informe-etapa-1-postulantes.tex desde informe-etapa-1-finalfinal.tex:
la Y = 0 incluye a los no matriculados (base de postulantes, 108.251 x 30)."""
import pathlib, sys

aqui = pathlib.Path(__file__).parent
src = (aqui / "informe-etapa-1-finalfinal.tex").read_text(encoding="utf-8")

R = []

# --- 1 Introducción --------------------------------------------------
R.append(("""base de 68.703 estudiantes que egresaron de enseñanza media en 2025 como
alumnos regulares y que se matricularon por vía regular, con tipo de
matrícula postulación regular. De ellos, 60.300 (87,8\\,\\%) se
matricularon en una de sus tres primeras preferencias y 8.403
(12,2\\,\\%) en la cuarta o más abajo.""",
"""base de 108.251 estudiantes que egresaron de enseñanza media en 2025
como alumnos regulares y que postularon por la vía regular. De ellos,
60.300 (55,7\\,\\%) se matricularon por vía regular en una de sus tres
primeras preferencias. Los otros 47.951 (44,3\\,\\%) se matricularon en la
cuarta preferencia o más abajo (8.403) o no se matricularon (39.548)."""))

# --- 3.3 Filtros -----------------------------------------------------
R.append(("""  \\item \\textbf{Vía y tipo de matrícula:} matriculados por vía regular
        (\\texttt{VIA} igual a 1) con tipo de matrícula «postulación
        regular» (\\texttt{TIPO\\_MATRICULA} igual a 1).""",
"""  \\item \\textbf{Postulación:} postularon al menos a una carrera por la
        vía regular (tienen \\texttt{TIPO\\_PREF} igual a REGULAR en el
        archivo D).
  \\item \\textbf{Matrícula:} se mantienen los que no se matricularon y,
        entre los matriculados, solo los de vía regular (\\texttt{VIA}
        igual a 1) con tipo de matrícula «postulación regular»
        (\\texttt{TIPO\\_MATRICULA} igual a 1). Quedan fuera los
        matriculados por otra vía o con otro tipo de matrícula."""))

# --- 3.4 Observaciones ----------------------------------------------
R.append(("""Alumnos regulares de la promoción del año & 218.066 \\\\
Vía regular y tipo de matrícula 1 & 68.704 \\\\
Inscribieron alguna prueba del proceso 2026 & 68.703 \\\\
\\rowcolor{yellow!30}
\\textbf{Con puntaje NEM distinto de 0 (base final)} & \\textbf{68.703} \\\\""",
"""Alumnos regulares de la promoción del año & 218.066 \\\\
Postularon por la vía regular & 114.865 \\\\
No matriculados, o matriculados por vía regular y tipo 1 & 108.598 \\\\
Inscribieron alguna prueba del proceso 2026 & 108.596 \\\\
\\rowcolor{yellow!30}
\\textbf{Con puntaje NEM distinto de 0 (base final)} & \\textbf{108.251} \\\\"""))
R.append(("""El filtro de puntaje NEM no saca a nadie: todos los alumnos regulares
que quedan tienen NEM.""",
"""El filtro de puntaje NEM saca a 345 estudiantes."""))

# --- 4 Variable de respuesta ----------------------------------------
R.append(("""tres primeras preferencias de quienes quedaron más abajo:""",
"""tres primeras preferencias de quienes quedaron más abajo o no se
matricularon:"""))
R.append(("""0 & \\text{si se matriculó en su cuarta preferencia o más abajo}""",
"""0 & \\text{si quedó en su cuarta preferencia o más abajo, o no se matriculó}"""))
R.append(("""1 (preferencia 1 a 3)        & 60.300 & 87,8\\% \\\\
0 (preferencia 4 o más abajo) &  8.403 & 12,2\\% \\\\
\\midrule
\\textbf{Total} & \\textbf{68.703} & 100\\% \\\\""",
"""1 (preferencia 1 a 3)                          & 60.300 & 55,7\\% \\\\
0 (preferencia 4 o más abajo, o sin matrícula) & 47.951 & 44,3\\% \\\\
\\midrule
\\textbf{Total} & \\textbf{108.251} & 100\\% \\\\"""))
R.append(("""De los 8.403 con valor 0,
3.339 quedaron en la cuarta, 1.881 en la quinta y el resto se reparte
entre la sexta y la vigésima. La variable está desbalanceada: cerca de
9 de cada 10 estudiantes tienen valor 1, lo que habrá que considerar al
evaluar el porcentaje correctamente predicho del modelo.""",
"""De los 47.951 con valor 0,
8.403 se matricularon en la cuarta preferencia o más abajo y 39.548 no
se matricularon. Para estos últimos, \\texttt{PREFERENCIA}, \\texttt{VIA},
\\texttt{TIPO\\_MATRICULA} y \\texttt{PTJE\\_POND} quedan sin valor. Al
incluir a los no matriculados, la variable queda más equilibrada: 55,7\\,\\%
frente a 44,3\\,\\%."""))

# --- 5.2 Dummies -----------------------------------------------------
R.append(("""Hay 10.566 estudiantes de colegios técnico profesionales y 58.137
        del resto.""",
"""Hay 18.877 estudiantes de colegios técnico profesionales y 89.374
        del resto."""))
R.append(("""5.697 preseleccionados PACE y 7.301 BEA.""",
"""7.790 preseleccionados PACE y 9.916 BEA."""))

# --- 6 Datos sin información ----------------------------------------
R.append(("""igual a 99 & 18.409 &""", """igual a 99 & 29.199 &"""))
R.append(("""vacía & 63.006 &""", """vacía & 100.461 &"""))
R.append(("""vacía & 61.402 &""", """vacía & 98.335 &"""))
R.append(("""no entran al cálculo de las variables del colegio. \\\\""",
"""no entran al cálculo de las variables del colegio. \\\\
\\texttt{PREFERENCIA}, \\texttt{VIA}, \\texttt{TIPO\\_MATRICULA}, \\texttt{PTJE\\_POND} & 39.548 & No se matriculó: quedan sin valor y su variable de respuesta es 0. \\\\"""))
R.append(("""Después de estos ajustes, la única variable con datos faltantes es
\\texttt{INGRESO\\_PERCAPITA\\_GRUPO\\_FA}, con 18.409 casos (26,8\\,\\% de
la base).""",
"""Fuera de las variables de matrícula de los no matriculados, la única
variable con datos faltantes es \\texttt{INGRESO\\_PERCAPITA\\_GRUPO\\_FA},
con 29.199 casos (27,0\\,\\% de la base)."""))

# --- 7 Definición de las variables -----------------------------------
R.append(("""0 si en la cuarta o más abajo. \\\\""",
"""0 si en la cuarta o más abajo, o si no se matriculó. \\\\"""))
R.append(("""Preferencia en que se matriculó (1 a 20 en la base).""",
"""Preferencia en que se matriculó (1 a 20; sin valor si no se matriculó)."""))
R.append(("""Vía de matrícula (1, regular, en toda la base).""",
"""Vía de matrícula (1, regular, en todos los matriculados; sin valor si no se matriculó)."""))
R.append(("""Tipo de matrícula (1, postulación regular, en toda la base).""",
"""Tipo de matrícula (1, postulación regular, en todos los matriculados; sin valor si no se matriculó)."""))
R.append(("""Puntaje ponderado con que se matriculó.""",
"""Puntaje ponderado con que se matriculó (sin valor si no se matriculó)."""))

# --- 8 Base final ----------------------------------------------------
R.append(("""\\textbf{68.703 filas y 30
columnas}""", """\\textbf{108.251 filas y 30
columnas}"""))
R.append(("""3.125 colegios distintos.""", """3.196 colegios distintos."""))
R.append(("""\\texttt{PROMEDIO\\_NOTAS}   & 4,50  & 6,30  & 6,25  & 7,00 \\\\
\\texttt{PTJE\\_NEM}         & 259   & 799   & 786   & 1.000 \\\\
\\texttt{PTJE\\_RANKING}     & 259   & 814   & 801   & 1.000 \\\\
\\texttt{CLEC\\_REG\\_ACTUAL} & 316   & 663   & 663   & 1.000 \\\\
\\texttt{MATE1\\_REG\\_ACTUAL}& 320   & 672   & 694   & 1.000 \\\\
\\texttt{PTJE\\_POND}        & 354,6 & 710,7 & 713,6 & 998,4 \\\\
\\texttt{N\\_ALUMNOS}        & 8     & 127   & 162   & 947 \\\\
\\texttt{INGRESO\\_COLEGIO}  & 1,0   & 4,0   & 4,9   & 10,0 \\\\
\\texttt{N\\_MATRICULADOS}   & 1     & 55    & 71    & 447 \\\\""",
"""\\texttt{PROMEDIO\\_NOTAS}   & 4,20  & 6,23  & 6,19  & 7,00 \\\\
\\texttt{PTJE\\_NEM}         & 163   & 779   & 767   & 1.000 \\\\
\\texttt{PTJE\\_RANKING}     & 163   & 793   & 781   & 1.000 \\\\
\\texttt{CLEC\\_REG\\_ACTUAL} & 0     & 634   & 640   & 1.000 \\\\
\\texttt{MATE1\\_REG\\_ACTUAL}& 0     & 645   & 668   & 1.000 \\\\
\\texttt{PTJE\\_POND}        & 354,6 & 710,7 & 713,6 & 998,4 \\\\
\\texttt{N\\_ALUMNOS}        & 8     & 129   & 164   & 947 \\\\
\\texttt{INGRESO\\_COLEGIO}  & 1,0   & 4,0   & 4,8   & 10,0 \\\\
\\texttt{N\\_MATRICULADOS}   & 0     & 54    & 70    & 447 \\\\"""))
R.append(("""En la base hay 36.237 mujeres (52,7\\%) y 32.466 hombres (47,3\\%).""",
"""\\texttt{PTJE\\_POND} se resume solo para los 68.703 matriculados. Los
mínimos de 0 en \\texttt{CLEC\\_REG\\_ACTUAL} y \\texttt{MATE1\\_REG\\_ACTUAL}
corresponden a quienes no rindieron esa prueba (77 y 161 estudiantes).
En la base hay 59.799 mujeres (55,2\\%) y 48.452 hombres (44,8\\%)."""))

# --- 9 Conclusión ----------------------------------------------------
R.append(("""quedó compuesta por 68.703 estudiantes egresados de enseñanza media en
2025 como alumnos regulares, matriculados por vía regular y bajo
postulación regular.""",
"""quedó compuesta por 108.251 estudiantes egresados de enseñanza media en
2025 como alumnos regulares que postularon por la vía regular: 68.703 se
matricularon por vía regular y bajo postulación regular, y 39.548 no se
matricularon."""))
R.append(("""matricularse en una de sus tres primeras preferencias o quedó en la
cuarta o más abajo. En la base final, un 87,8\\,\\% de los estudiantes se
matriculó dentro de sus tres primeras preferencias, mientras que un
12,2\\,\\% lo hizo más abajo.""",
"""matricularse en una de sus tres primeras preferencias o, en cambio,
quedó en la cuarta o más abajo o no se matriculó. En la base final, un
55,7\\,\\% de los estudiantes se matriculó dentro de sus tres primeras
preferencias, mientras que un 44,3\\,\\% quedó más abajo o no se
matriculó."""))

out = src
for i, (viejo, nuevo) in enumerate(R, 1):
    n = out.count(viejo)
    if n != 1:
        sys.exit(f"reemplazo {i}: encontrado {n} veces:\n{viejo[:120]}")
    out = out.replace(viejo, nuevo)

(aqui / "informe-etapa-1-postulantes.tex").write_text(out, encoding="utf-8")
print(f"ok: {len(R)} reemplazos")
