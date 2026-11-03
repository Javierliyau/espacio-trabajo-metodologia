"""Convierte la lectura del caso Moore (md) a PDF con xelatex. Soporta solo lo que ese md usa."""
import re
import subprocess
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
BASE = SRC.parent
SPLIT = re.compile(r"(\$\$.*?\$\$|\$[^$]+\$)")


def texto(s):
    out = []
    for p in SPLIT.split(s):
        if p.startswith("$"):
            out.append(p)
            continue
        p = p.replace("\\", r"\textbackslash{}")
        for a, b in (("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_"), ("≈", r"$\approx$"), ("⇒", r"$\Rightarrow$"), ("×", r"$\times$")):
            p = p.replace(a, b)
        p = re.sub(r"`([^`]+)`", r"\\texttt{\1}", p)
        p = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p)
        out.append(p)
    s = "".join(out)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<![\*\w])\*([^*]+?)\*", r"\\emph{\1}", s)
    return s


out, lista, tabla = [], None, []


def cerrar_lista():
    global lista
    if lista:
        out.append(r"\end{%s}" % lista)
        lista = None


def cerrar_tabla():
    global tabla
    if not tabla:
        return
    n = len(tabla[0])
    spec = r"p{0.6cm}p{9.4cm}p{1.8cm}p{1.9cm}" if tabla[0][0] == "#" else r"p{2.6cm}p{5.6cm}p{2.7cm}p{3.2cm}"
    out.append(r"\begin{center}\small\begin{tabular}{%s}\toprule" % spec)
    for k, f in enumerate(tabla):
        out.append(" & ".join(texto(c) for c in f) + r" \\" + (r"\midrule" if k == 0 else ""))
    out.append(r"\bottomrule\end{tabular}\end{center}")
    tabla = []


ls = SRC.read_text(encoding="utf-8").split("\n")
i = 0
while i < len(ls):
    l = ls[i]
    if l.startswith("|"):
        cerrar_lista()
        if not re.match(r"^\|[-| ]+\|$", l):
            tabla.append([c.strip() for c in l.strip("|").split("|")])
        i += 1
        continue
    cerrar_tabla()
    if l.startswith("$$"):
        cerrar_lista()
        eq = l.strip("$")
        m = re.search(r"\\tag\{([^}]+)\}", eq)
        out.append(r"\begin{equation*}" + eq + r"\end{equation*}")
    elif l.startswith("!["):
        cerrar_lista()
        ruta = re.search(r"\(([^)]+)\)", l).group(1)
        out.append(r"\begin{center}\includegraphics[width=0.62\linewidth]{%s}\end{center}" % (BASE / ruta).as_posix())
    elif l.startswith("# "):
        out.append(r"\begin{center}{\LARGE\bfseries %s}\end{center}" % texto(l[2:]))
    elif l.startswith("## "):
        cerrar_lista()
        out.append(r"\section*{%s}" % texto(l[3:]))
    elif l.startswith("### "):
        cerrar_lista()
        out.append(r"\subsection*{%s}" % texto(l[4:]))
    elif l.startswith("- ") or re.match(r"^\d+\. ", l):
        tipo = "itemize" if l.startswith("- ") else "enumerate"
        if lista != tipo:
            cerrar_lista()
            out.append(r"\begin{%s}[leftmargin=*,itemsep=2pt,topsep=2pt]" % tipo)
            lista = tipo
        out.append(r"\item " + texto(re.sub(r"^(- |\d+\. )", "", l)))
    elif not l.strip():
        cerrar_lista()
        out.append("")
    else:
        out.append(texto(l))
    i += 1
cerrar_lista()
cerrar_tabla()

tex = r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=2.2cm]{geometry}
\usepackage{fontspec,amsmath,amssymb,booktabs,graphicx,enumitem,parskip,xcolor}
\setmainfont{Cambria}
\usepackage{unicode-math}
\setmathfont{Cambria Math}
\usepackage[spanish,es-noshorthands]{babel}
\pagestyle{plain}
\begin{document}
""" + "\n".join(out) + "\n\\end{document}\n"
dst = Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
t = dst / (SRC.stem + ".tex")
t.write_text(tex, encoding="utf-8")
for _ in range(2):
    r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-output-directory", str(dst), str(t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.returncode)
print("\n".join(x for x in r.stdout.split("\n") if x.startswith("!") or "Output written" in x or "Missing character" in x)[:1500])
