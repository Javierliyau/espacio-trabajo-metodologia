import re,sys
p=sys.argv[1]; s=open(p,encoding='utf8').read()
I='\x5citem'  # backslash-item
# macros
s=s.replace('\x5cnewcommand{\x5cestrella}', '\x5cnewcommand{\x5coblig}[1]{\x5cfbox{\x5cfootnotesize\x5ctextbf{OBLIGATORIO} · $p\x5capprox #1$}\x5c,}\n\x5cnewcommand{\x5copc}[1]{\x5cfbox{\x5cfootnotesize opcional · $p\x5capprox #1$}\x5c,}\n\x5cnewcommand{\x5cestrella}',1)
# matemáticos
a=s.index('% ---------- 1. S1'); b=s.index('\x5csection*{Definiciones}')
mat=s[a:b]; fin=mat.rindex('\x5cend{enumerate}')
bl=re.split(r'(?=^% ---------- \d\. )',mat[:fin],flags=re.M); bl=[x for x in bl if x.strip()]
assert len(bl)==6
tag={0:'\x5coblig{0{,}95}',2:'\x5coblig{0{,}90}',3:'\x5coblig{0{,}55}',4:'\x5copc{0{,}50}',1:'\x5copc{0{,}50}',5:'\x5copc{0{,}45}'}
orden=[0,2,3,4,1,5]
def tg(x,t): return re.sub(r'(\x5citem \(\d+ puntos\))', lambda m:m.group(1)+' '+t, x, count=1)
nuevo=''.join(tg(bl[i],tag[i]) for i in orden)
nuevo=nuevo.replace('datos del ejercicio 1','datos del ejercicio 1, el primero')
s=s[:a]+nuevo+mat[fin:]+s[b:]
# definiciones
a=s.index('\x5csection*{Definiciones}'); b=s.index('\x5csection*{Verdadero o Falso')
d=s[a:b]; h=d.index('\n',d.index('\x5cbegin{enumerate}'))+1; e=d.rindex('\x5cend{enumerate}')
it=re.split(r'(?=^\x5citem \(12 puntos\))',d[h:e],flags=re.M); it=[x for x in it if x.strip()]
assert len(it)==4
tg2={1:'\x5coblig{0{,}35}',2:'\x5coblig{0{,}35}',3:'\x5copc{0{,}30}',0:'\x5copc{0{,}25}'}
d=d[:h]+''.join(tg(it[i],tg2[i]) for i in [1,2,3,0])+d[e:]
s=s[:a]+d+s[b:]
s=s.replace('Trae 6 matemáticos (prioridad 1, 3, 4, 5, 2, 6), 4 definiciones,','Trae 6 matemáticos y 4 definiciones \x5ctextbf{ordenados por probabilidad} (\x5coblig{} = obligatorio, \x5copc{} = opcional; $p$ = probabilidad de que salga ese tipo de pregunta),',1)
open(p,'w',encoding='utf8').write(s); print('ok')
