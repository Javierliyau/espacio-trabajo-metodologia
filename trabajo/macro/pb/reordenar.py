import re, sys
p = sys.argv[1]
s = open(p, encoding='utf8').read()

ini = s.index(r'\begin{enumerate}[label=\arabic*.,leftmargin=1.6em,itemsep=0.6em,start=14]')
fin = s.index(r'\end{document}')
bloque = s[ini:fin]
cuerpo = bloque[bloque.index('\n') + 1: bloque.rindex(r'\end{enumerate}')]
cuerpo = re.sub(r'^% ----.*\n', '', cuerpo, flags=re.M)
items = [x.strip() + '\n' for x in re.split(r'(?=^\\item \(12 puntos\))', cuerpo, flags=re.M) if x.strip()]
assert len(items) == 22, len(items)

# índice 0 = comente 14 del orden anterior ... 21 = comente 35
fam = [
 ('1', 'Transición y convergencia',
  r'gráfico de tasas: $\dfrac{\dot k}{k}=s\dfrac{y}{k}-(\delta+n)$ como distancia vertical (la $PMgK$ decreciente hace que la curva baje); con $A$: $\dfrac{\dot k}{k}=(\delta+n+g)\left(\dfrac{\tilde k^*}{\tilde k}\right)^{1-\alpha}-(\delta+n)$.',
  [1, 0, 5, 4, 21]),
 ('2', 'Sendero de crecimiento balanceado y nivel vs.\ crecimiento',
  r'logaritmo y derivada; $y^*(t)=A(t)\left(\frac{s}{\delta+n+g}\right)^{\frac{\alpha}{1-\alpha}}$; en el SCB, $g_y=g$ (nada más mueve la tasa de largo plazo). Frase de cierre: «efecto nivel, no crecimiento».',
  [11, 10, 2, 3, 20, 12]),
 ('3', 'Romer',
  r'ideas no rivales $\Rightarrow$ rendimientos crecientes $\Rightarrow$ hace falta $\pi>0$ ($p=r/\alpha$, $P_A=\pi/(r-n)$); $\dfrac{\dot A}{A}=\theta\dfrac{L_A^{\lambda}}{A^{1-\phi}}$ y $g_A=\dfrac{\lambda n}{1-\phi}$.',
  [16, 6, 19, 17, 7, 18]),
 ('4', 'Regla de oro',
  r'$c^*=f(k^*)-(n+\delta)k^*$; $f^\prime(k_{oro})=n+\delta$; con Cobb-Douglas, $s_{oro}=\alpha$; gráfico de niveles.',
  [8, 9]),
 ('5', 'Capital humano y residuo',
  r'$y^*(t)=A(t)\,e^{\psi u}\left(\frac{s}{\delta+n+g}\right)^{\frac{\alpha}{1-\alpha}}$: $u$ mueve el nivel ($e^{\psi\Delta u}$, exacto), no la tasa.',
  [13, 14, 15]),
]
assert sorted(i for f in fam for i in f[3]) == list(range(22))

opts = r'label=\arabic*.,leftmargin=1.6em,itemsep=0.6em'
out = []
for k, (n, nom, base, idx) in enumerate(fam):
    out.append(r'\familia{%s}{%s}{%s}' % (n, nom, base) + '\n')
    out.append(r'\begin{enumerate}[%s,%s]' % (opts, 'start=14' if k == 0 else 'resume') + '\n')
    for j, i in enumerate(idx):
        it = items[i]
        if j == 0:
            it = it.replace(r'\item (12 puntos)', r'\item (12 puntos) \base', 1)
        out.append(it + '\n')
    out.append(r'\end{enumerate}' + '\n\n')
s = s[:ini] + ''.join(out) + s[fin:]

# macros y nota inicial
s = s.replace(r'\newcommand{\estrella}{$^\bigstar$\,}',
  r'\newcommand{\estrella}{$^\bigstar$\,}' + '\n' +
  r'\newcommand{\base}{\textsc{[base]}\,}' + '\n' +
  r'\newcommand{\familia}[3]{\par\medskip\noindent\textbf{Familia #1 · #2.}\\{\small\textit{Herramienta común:} #3}\par\smallskip}', 1)
s = s.replace(r'\estrella = comente más probable (va primero).',
  r'Los comentes van agrupados en \textbf{familias}, de la más probable a la menos probable. Dentro de cada familia, el primero (\base) da la herramienta que usan los siguientes. \estrella = comente más probable.', 1)
open(p, 'w', encoding='utf8').write(s)
print('ok')
