import sys,io
P='material/microeconomia-ii/2026-11-06-plan-conjunto-pep1-econometria-micro.md'
def ed(fn,f):
    L=open(fn,encoding='utf-8').read().split('\n'); L=f(L); open(fn,'w',encoding='utf-8',newline='\n').write('\n'.join(L))
def after(L,key,new,start=0):
    i=next(j for j in range(start,len(L)) if key in L[j]); L.insert(i+1,new); return L
def repl(L,key,new):
    i=next(j for j,x in enumerate(L) if key in x); L[i]=new; return L
def w1(L):
    L=after(L,'**sesión B**',f'- [ ] Micro · **μ1** (17:00, 23 min): rehacer en frío C2 (dos partes, idénticos) y C3 (3.er grado y Pareto) del Control 1 y el D1 en 5 líneas; corregir con `2026-11-01-feedback-control-1.md`. Plan conjunto: `{P}`')
    L=after(L,'**sesión D**','- [ ] Micro · **μ2** (16:00, 86 min, bloques 25 + 5): **juegos (nuevo)**: pretest C2, C4 y C6 · slides de juegos pp. 20-76, activo · una matriz 3×3 sin mirar · comente C1 de competencia monopolística con gráfico · paquetes (slides pp. 41-44) y C11 · mini-prueba de 5 min')
    L=after(L,'**sesión E**','- [ ] Micro · **μ3** (16:00, 60 min): A2 ej. 2 sin mirar (3.er grado frente a precio único, ¿excluir?) · A3 ej. 5 (dos partes) · comentes C2, C4, C6 y C14 escritos + una matriz nueva (pedirla en el chat). Después, Macro y a dormir temprano')
    return L
def w2(L):
    L=repl(L,'Micro II (noche, ~1,5 h): **diagnóstico**',f'- [ ] Micro · **μ4** (20:00, 85 min): matriz de la PEP 1 2026-1 sin mirar · secuenciales: slides y árbol de la Suficiencia 2026-1 (si no entran: 2.ª matriz y A3 ej. 4) · A4 ej. 4 (dos partes, dos tipos) · A4 ej. 5 (comp. monopolística) · comentes C10 y C13. Plan: `{P}`')
    L=repl(L,'Micro II (tarde, ~3 h): **discriminación en cálculo**','- [ ] Micro · **μ5** (15:00, 112 min): **simulacro** `2026-11-04-simulacro-pep-1-mundaca.pdf` cronometrado (80 min) + corrección con `…-PAUTA-no-abrir.md` (30 min) → **lista de errores de Micro**')
    L=after(L,'### 2026-11-10','- [ ] Micro II (clase 08:15): **preguntar** hora, sala y duración de la PEP y si entran los juegos secuenciales')
    L=repl(L,'Micro II (mañana, ~3 h): **simulacro**','- [ ] Micro · **μ6** (18:30, 53 min, después de Sociología): A4 ej. 3 sin mirar · una matriz nueva + EN en puras · Hotelling (slides pp. 58-79) y comente C3 con gráfico. **Micro queda cerrada aquí**')
    L=repl(L,'Historia (noche, después de Sociología, ~2 h)','- [ ] Historia (20:00-21:00, 1 h): **L6** (O\'Rourke, 14 pp.) con protocolo. Las fichas de la L3 y la 3.ª de la L4 pasan al jue en la tarde (plan conjunto: no cargar la noche antes de dos PEP)')
    L=after(L,'**sesión J**','- [ ] (07:50, 10 min) escritura expresiva antes de la PEP: anotar lo que preocupa y botar la hoja (Ramirez y Beilock 2011)')
    i=next(j for j,x in enumerate(L) if 'Econometría (08:15, asumida): **PEP 1**' in x)
    L.insert(i+1,'- [ ] (09:35-10:05) **pausa real**: comer, caminar, sin pantalla, sin comentar la prueba')
    L.insert(i+2,'- [ ] Micro · **μ7** (10:05, 33 min): §6 de la predicción (respuestas en pocas líneas) y una matriz rápida. Nada nuevo')
    L=repl(L,'Micro II (12:45-13:45, después de Taller, 1 h)','- [ ] Micro · **μ8** (13:15, 15 min, después de almorzar): dos partes en 2 líneas · lista de errores: veredicto en la primera palabra, IMg = P(1 − 1/|ε|), ES_CP − ES = PIE, ¿excluir un grupo? · 13:30: 10 min de escritura expresiva')
    return L
ed('2026-11-02.md',w1); ed('2026-11-09.md',w2); print('ok')
