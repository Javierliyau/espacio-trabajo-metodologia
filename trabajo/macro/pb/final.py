import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf8').read()

pre, doc = s.split(r'\begin{document}', 1)
pre = pre.replace(r'\newcommand{\estrella}',
    r'\newcommand{\ficha}[1]{\ifpauta\par{\small$\Rightarrow$\ #1}\fi}' + '\n' + r'\newcommand{\estrella}', 1)
pre = '% VERSIÓN FINAL FILTRADA (ruta corta, §8.1 de 2026-11-06-prediccion-final-pep-1.md). Generada desde 2026-11-07-prueba-banco-pep-1.tex.\n' + pre

# --- encabezado y nota
i_mat = doc.index(r'\section*{Ejercicios matemáticos}')
cab = doc[:i_mat]
cab = cab.replace('Prueba-banco PEP 1}}', 'Prueba-banco PEP 1 · Final}}', 1)
nota = (r'{\small\textit{Versión final filtrada para la máxima nota esperada. Trae 6 matemáticos (prioridad 1, 3, 4, 5, 2, 6), '
        r'4 definiciones, 10 comentes para \textbf{mecanizar}, agrupados por familia (el \base\ va primero y da la herramienta de los siguientes), '
        r'y 12 \textbf{fichas} de una línea. \estrella = más probable. '
        r'Sáb: 1.ª pasada escrita y tapada. Dom (tarde): 2.ª pasada oral con croquis. Lun (M5): 3.ª pasada oral y lectura de las fichas.}}' + '\n')
cab, n = re.subn(r'\{\\small\\textit\{Práctica.*?\}\}\n', lambda m: nota, cab, count=1, flags=re.S)
assert n == 1

# --- matemáticos sin el 7
i_res = doc.index('% ---------- 7. Reserva')
mat = doc[i_mat:i_res] + '\\end{enumerate}\n\n'

# --- definiciones: las 4 primeras
i_def = doc.index(r'\section*{Definiciones}')
i_vf = doc.index(r'\section*{Verdadero o Falso')
defs = doc[i_def:i_vf]
d_ini = defs.index(r'\begin{enumerate}')
d_cab = defs[:d_ini] + defs[d_ini:defs.index('\n', d_ini) + 1].replace('start=8', 'start=7')
d_items = re.split(r'(?=^\\item \(12 puntos\))', defs[defs.index('\n', d_ini) + 1:defs.rindex(r'\end{enumerate}')], flags=re.M)
d_items = [x for x in d_items if x.strip()]
assert len(d_items) == 6
defs = d_cab + ''.join(d_items[:4]) + '\\end{enumerate}\n\n'

# --- comentes
vf = doc[i_vf:doc.index(r'\end{document}')]
vf_cab = vf[:vf.index(r'\familia')]
fams = re.findall(r'^\\familia.*$', vf, flags=re.M)
assert len(fams) == 5
items = [x for x in re.split(r'(?=^\\item \(12 puntos\))', vf, flags=re.M)[1:]]
items = [re.sub(r'\\end\{enumerate\}.*', '', x, flags=re.S).strip() + '\n' for x in items]
assert len(items) == 22
num = {14 + k: it.replace(r'\base ', '') for k, it in enumerate(items)}

grupos = [[14, 16, 17], [19, 21], [26, 28, 29], [31], [33]]
opts = r'label=\arabic*.,leftmargin=1.6em,itemsep=0.6em'
out = [vf_cab]
for k, g in enumerate(grupos):
    out.append(fams[k] + '\n')
    out.append(r'\begin{enumerate}[%s,%s]' % (opts, 'start=11' if k == 0 else 'resume') + '\n')
    for j, c in enumerate(g):
        it = num[c]
        if j == 0:
            it = it.replace(r'\item (12 puntos)', r'\item (12 puntos) \base', 1)
        out.append(it + '\n')
    out.append('\\end{enumerate}\n\n')

# --- fichas
lineas = {
 15: r'\textbf{V} · base 14: mismo $k^*$; la pobre tiene más brecha en el gráfico de tasas. Es convergencia entre economías con los mismos parámetros.',
 18: r'\textbf{I} · base 16: $\dot y/y=g+\alpha\,\dot{\tilde k}/\tilde k<g$; solo decrece si $\alpha|\dot{\tilde k}/\tilde k|>g$ (muy lejos del EE).',
 20: r'\textbf{V} · base 19: en el EE, $g_y=\alpha g_k=0$ por la $PMgK$ decreciente; $g$ es exógeno, y eso motiva el modelo de Romer.',
 22: r'\textbf{F} · base 21: la 1.ª parte es V ($\tilde y^*$ menor, recta $\delta+n+g$ más alta), pero $g_y=g$ en ambos: nivel, no tasa.',
 23: r'\textbf{V} · bases 19 y 21: $\tilde y^*$ baja, pero $g_Y=n+g$ sube.',
 24: r'\textbf{V} · base 19: $\tilde k^*$ baja (nivel), pero $y(t)=A(0)e^{gt}\tilde y^*$ y domina el crecimiento.',
 25: r'\textbf{F} · base 26: no rival $\neq$ no excluible. Las patentes hacen las ideas parcialmente excluibles, y eso permite $p>CMg$.',
 27: r'\textbf{F} · base 28: misma forma reducida, pero $A$ es endógena ($\dot A=\theta L_A^{\lambda}A^{\phi}$), con $s_R$ y monopolio.',
 30: r'\textbf{F} · base 29: $y\propto s_R(1-s_R)$, que tiene el máximo en $s_R=0{,}5$.',
 32: r'\textbf{V} · base 31: $f^\prime(k^*)<n+\delta$ (ineficiencia dinámica); bajar $s$ sube $c$ hoy y en el largo plazo.',
 34: r'\textbf{F} · base 33: $e^{0{,}2}=1{,}221$, o sea $+22{,}1\%$; el 20\% es la aproximación logarítmica.',
 35: r'\textbf{V} (con matiz) · base 33: es lo que no explican $K$ ni $H$; «una medida de nuestra ignorancia».',
}
out.append(r'\section*{Fichas de una línea}' + '\n' + r'{\small Di el veredicto y cuál comente te sirve de base, en 30 segundos. No se escriben.}' + '\n')
out.append(r'\begin{enumerate}[label=F\arabic*.,leftmargin=2.2em,itemsep=0.4em]' + '\n')
nuevo = {c: 11 + k for k, c in enumerate(sum(grupos, []))}
for c, l in lineas.items():
    l = re.sub(r'bases? ([\d y]+):', lambda m: re.sub(r'\d+', lambda d: str(nuevo[int(d.group())]), m.group()), l)
    enun = num[c].split(r'\begin{resp}')[0].replace(r'\item (12 puntos)', r'\item', 1).strip()
    out.append(enun + '\n' + r'\ficha{' + l + '}\n')
out.append('\\end{enumerate}\n\n')

open(dst, 'w', encoding='utf8').write(pre + r'\begin{document}' + cab + mat + defs + ''.join(out) + '\\end{document}\n')
print('ok')
