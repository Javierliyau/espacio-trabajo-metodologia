# Genera versiones "pagina de libro" del simulacro final y su pauta.
# El cuerpo (enunciados, numeros, puntajes) se copia tal cual; solo cambia el preambulo,
# la portada del capitulo y la caja de instrucciones (de tcolorbox en linea a entorno 'nota').
import pathlib, sys

base = pathlib.Path(sys.argv[1])

COMUN = r"""\documentclass[11pt,a4paper,twoside]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[spanish,es-noshorthands]{babel}
\usepackage{amsmath}
\usepackage{newpxtext,newpxmath}
\usepackage[a4paper,inner=2.5cm,outer=2.7cm,top=2.7cm,bottom=2.5cm,headsep=0.7cm,headheight=14pt]{geometry}
\usepackage{booktabs,array,enumitem,xcolor,microtype,fancyhdr,titlesec,needspace}
\usepackage[most]{tcolorbox}
\definecolor{libro}{RGB}{0,70,127}
\definecolor{libroclaro}{RGB}{229,238,247}
\definecolor{tinta}{RGB}{35,35,35}
\definecolor{alerta}{RGB}{160,40,30}
\definecolor{alertaclaro}{RGB}{250,236,232}
\definecolor{verde}{RGB}{30,105,60}
\definecolor{verdeclaro}{RGB}{233,245,237}
\color{tinta}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\newcommand{\sansc}[1]{{\sffamily\scshape #1}}
% --- Cabeceras de libro (pares e impares)
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{libro}\leaders\hrule height \headrulewidth\hfill}}
\fancyhead[LE]{\small\bfseries\textcolor{libro}{\thepage}\quad\normalfont\sffamily\footnotesize CAPÍTULO DE REPASO\quad\textcolor{libro}{\textbullet}\quad Elección binaria, \emph{scoring} y evaluación de impacto}
\fancyhead[RO]{\sffamily\footnotesize ECONOMETRÍA II\quad\textcolor{libro}{\textbullet}\quad PEP 1 · Simulacro final%%ETIQUETA%%\quad\normalfont\small\bfseries\textcolor{libro}{\thepage}}
\fancypagestyle{apertura}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}\fancyfoot[C]{\small\textcolor{libro}{\thepage}}}
% --- Portada de capitulo
\newcommand{\apertura}[4]{%
  \thispagestyle{apertura}%
  \vspace*{-1.2cm}%
  {\color{libro}\rule{\textwidth}{3pt}}\par\vspace{2pt}
  {\sffamily\small\color{libro}\scshape #1}\par\vspace{2pt}
  \noindent\begin{minipage}[b]{0.72\textwidth}\raggedright{\fontsize{26}{30}\selectfont\bfseries\color{libro}#3}\end{minipage}\hfill{\sffamily\fontsize{46}{46}\selectfont\bfseries\color{libro!25}#2}\par\vspace{4pt}
  {\color{libro}\rule{\textwidth}{0.6pt}}\par\vspace{3pt}
  {\itshape\small #4}\par\vspace{4pt}}
"""

SIMULACRO = COMUN + r"""% --- Ejercicios con formato de libro
\newcommand{\pts}[1]{\hfill{\sffamily\footnotesize\bfseries\color{libro}(#1)}}
\def\pregpartir#1. #2\relax{\pregnum{#1}\pregtit{#2}}
\newcommand{\pregnum}[1]{\gdef\elnum{#1}}
\newcommand{\pregtit}[1]{\gdef\eltit{#1}}
\newenvironment{preg}[2]{%
  \pregpartir#1\relax
  \par\addvspace{12pt}\needspace{9\baselineskip}\noindent
  \begin{tcolorbox}[enhanced,breakable,frame hidden,sharp corners,colback=white,boxrule=0pt,
     left=0pt,right=0pt,top=0pt,bottom=0pt,
     borderline north={1.2pt}{0pt}{libro},before skip=0pt,after skip=4pt]
  {\sffamily\bfseries\Large\color{libro}\elnum}\hspace{8pt}{\large\bfseries\eltit}\hfill{\sffamily\footnotesize\color{libro}\MakeUppercase{#2}}\par\vspace{6pt}
}{\end{tcolorbox}}
\newtcolorbox{nota}{enhanced,breakable,sharp corners,colback=libroclaro,colframe=libro,boxrule=0pt,
  leftrule=3pt,left=8pt,right=8pt,top=5pt,bottom=5pt,
  title={\sffamily\bfseries\footnotesize CONCEPTO CLAVE\enspace·\enspace INSTRUCCIONES PARA EL SIMULACRO},
  coltitle=white,colbacktitle=libro,toptitle=2pt,bottomtitle=2pt}
\setlist[enumerate,1]{label={\bfseries\color{libro}\alph*)},leftmargin=*,itemsep=3pt}
"""

PAUTA = COMUN + r"""% --- Soluciones con formato de libro
\newtcolorbox{ejemplar}{enhanced,breakable,sharp corners,colback=verdeclaro,colframe=verde,boxrule=0pt,leftrule=3pt,
  left=8pt,right=8pt,top=4pt,bottom=4pt,before skip=6pt,after skip=6pt,
  title={\sffamily\bfseries\footnotesize RESPUESTA EJEMPLAR},coltitle=verde,colbacktitle=verdeclaro,
  toptitle=1pt,bottomtitle=0pt,titlerule=0pt}
\newtcolorbox{trampa}{enhanced,breakable,sharp corners,colback=alertaclaro,colframe=alerta,boxrule=0pt,leftrule=3pt,
  left=8pt,right=8pt,top=4pt,bottom=4pt,before skip=6pt,after skip=6pt,
  title={\sffamily\bfseries\footnotesize\textcolor{alerta}{\large !}\enspace TRAMPAS},coltitle=alerta,colbacktitle=alertaclaro,
  toptitle=1pt,bottomtitle=0pt,titlerule=0pt}
\titleformat{\section}{\Large\bfseries\color{libro}}{}{0pt}{}[\vspace{2pt}{\color{libro}\titlerule[1.2pt]}]
\titlespacing*{\section}{0pt}{18pt}{8pt}
\titleformat{\subsection}{\large\bfseries}{}{0pt}{\color{libro}}
\titlespacing*{\subsection}{0pt}{12pt}{4pt}
\newcommand{\sub}[2]{\subsection*{#1\hfill{\sffamily\footnotesize\bfseries(#2)}}}
"""

def armar(origen, destino, preambulo, etiqueta, apertura):
    txt = (base / origen).read_text(encoding="utf-8")
    i = txt.index(r"\begin{document}")
    cuerpo = txt[i:]
    # quitar el titulo centrado original (primer bloque center tras \begin{document})
    a = cuerpo.index(r"\begin{center}")
    b = cuerpo.index(r"\end{center}", a) + len(r"\end{center}")
    cuerpo = cuerpo[:a] + apertura + cuerpo[b:]
    # caja de instrucciones del enunciado: eliminada a pedido del estudiante (5-11)
    if r"\begin{tcolorbox}[" in cuerpo:
        s = cuerpo.index(r"\begin{tcolorbox}[")
        e = cuerpo.index(r"\end{tcolorbox}", s) + len(r"\end{tcolorbox}")
        cuerpo = cuerpo[:s] + cuerpo[e:]
    # el \% redefinido se comia el espacio siguiente ("90 %y"): cerrar el numero con \relax
    cuerpo = cuerpo.replace(r"\else\char37\fi}", r"\else\char37\relax\fi}")
    # dos lineas que se salian del margen mas angosto del libro
    cuerpo = cuerpo.replace(r"p{7.2cm}", r"p{6.0cm}")
    cuerpo = cuerpo.replace("\\[\n(0{,}20)(0{,}693)", "{\\small\\[\n(0{,}20)(0{,}693)")
    cuerpo = cuerpo.replace("=\\mathbf{0{,}319}\n\\]", "=\\mathbf{0{,}319}\n\\]}")
    cuerpo = cuerpo.replace(r"\section*{", r"\needspace{8\baselineskip}\section*{")
    pre = preambulo.replace("%%ETIQUETA%%", etiqueta)
    (base / destino).write_text(pre + cuerpo, encoding="utf-8")

armar("2026-11-04-simulacro-final-pep1.tex", "2026-11-04-simulacro-final-pep1-libro.tex", SIMULACRO, "",
      "")
armar("2026-11-04-simulacro-final-pep1-pauta.tex", "2026-11-04-simulacro-final-pep1-pauta-libro.tex", PAUTA, r" · \textcolor{alerta}{Pauta}",
      r"\apertura{Econometría II · PEP 1 · Simulacro final}{PEP 1}{Soluciones: \textcolor{alerta}{pauta}}{No abrir antes de terminar los 80 minutos. Corregir con lápiz de otro color y anotar las fallas en la tabla final.}")
print("ok")
