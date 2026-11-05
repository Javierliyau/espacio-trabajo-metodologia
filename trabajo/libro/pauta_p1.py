# Pauta completa de la P1 (formato libro) como documento aparte, con la d) ampliada.
import pathlib
d = pathlib.Path(r"C:/Proyecto Metodologia de estudio/datos/material/econometria-ii")
L = (d / "2026-11-04-simulacro-final-pep1-pauta-libro.tex").read_text(encoding="utf-8").split("\n")
pre = L[:53]          # preambulo + \begin{document}
renew = L[53]         # \renewcommand{\%}...
i58 = next(k for k, l in enumerate(L) if r"\section*{P1." in l)
i_p2 = next(k for k, l in enumerate(L) if r"\section*{P2." in l)
cuerpo = "\n".join(L[i58:i_p2]).rstrip().rstrip("% =").rstrip()

viejo_d_fin = "Son \\textbf{odds}, no probabilidades: no es «3 veces más probable». Va en veces o en \\%, nunca en pp.\n\\end{trampa}"
assert viejo_d_fin in cuerpo
nuevo_d_fin = viejo_d_fin + r"""
\textbf{Cómo se calcula el 200\,\%:} $(e^{\beta}-1)\cdot100=(3{,}0-1)\cdot100=200\,\%$. «3 veces» compara niveles; «200\,\% mayores» mide el aumento.\\
\textbf{Verificación con las probabilidades de la b)}, por cada 1.000 clientes:
\begin{center}\small
\begin{tabular}{lccc}\toprule
 & Incumplen & Pagan & Odds $=P/(1-P)$\\\midrule
Sin atraso ($\hat P_0=0{,}0522$) & 52 & 948 & $0{,}0551$: 1 por cada 18\\
Con atraso ($\hat P_1=0{,}1419$) & 142 & 858 & $0{,}1654$: 1 por cada 6\\\bottomrule
\end{tabular}
\end{center}
Razón de odds: $0{,}1654/0{,}0551=3{,}00=e^{1{,}1}$. Las probabilidades no se triplican (pasan de 5,2\,\% a 14,2\,\%).
\begin{trampa}
El 3 es una \textbf{razón entre las odds de dos grupos}, no las odds de un grupo. «3 morosos por cada 1 que paga» serían odds $=3$, es decir, $P=75\,\%$, y el cliente con atraso tiene $P=14{,}2\,\%$.
\end{trampa}"""
cuerpo = cuerpo.replace(viejo_d_fin, nuevo_d_fin)

apertura = r"\apertura{Econometría II · PEP 1 · Simulacro final}{P1}{Pauta: logit y clasificación}{Pauta completa de la P1 (35 pts), con la d) ampliada.}"
pre_txt = "\n".join(pre).replace(r"Simulacro final · \textcolor{alerta}{Pauta}", r"Simulacro final · \textcolor{alerta}{Pauta P1}")
(d / "2026-11-04-simulacro-final-pep1-pauta-p1-libro.tex").write_text(
    pre_txt + "\n" + renew + "\n\n" + apertura + "\n\n" + cuerpo + "\n\n\\end{document}\n", encoding="utf-8")
print("ok")
