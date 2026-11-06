# Micro v2 (704 min, nota 5,34): reemplaza las lineas de Micro en la agenda y la columna Micro del §4 del plan conjunto
import re,sys
sys.stdout.reconfigure(encoding='utf-8')
FB='`2026-11-01-feedback-control-1.md`'
S={
'vie':["**μ1** (17:00, 25 min): **C1** de la predicción (competencia monopolística a LP, con gráfico; M5) y **C2 del Control 1** en frío (dos partes con consumidores idénticos: p = CMg, T = EC; M2). Corregir con "+FB,
       "**μ2** (20:30, 34 min): **paquetes, nuevo** (slides de juegos pp. 41-44 y comente C11; M9) · **A4 ej. 5** (competencia monopolística; M5) · **C3 del Control 1** (3.er grado y Pareto) y el **D1** en 5 líneas (M3)"],
'sab':["**μ3** (15:30, 97 min, bloques de 25 + 5; Macro va en la mañana): **juegos, nuevo (60)**: pretest de 5 min con los comentes C2, C4 y C6 sin saber, slides `2026-11-01-teoria-de-juegos.pdf` pp. 20-76 en modo activo (tapar cada ejemplo y resolverlo antes de mirar) y una matriz 3×3 sin mirar · **A3 ej. 5** (dos partes) · comente **C10** (1.er grado) · un comente de paquetes de `2026-10-21-correccion-2do-grado-y-paquetes.md` · **Hotelling**: slides pp. 58-79",
       "**μ4** (18:30, 48 min): comentes **C2, C4, C6 y C14** escritos (juegos) · **A4 ej. 4** (dos partes con dos tipos) · comente **C3** de Hotelling con gráfico, sin mirar · un comente de competencia monopolística (C1 con otras palabras)"],
'dom':["**μ5** (16:00, 89 min; Macro va en la mañana): **secuenciales, nuevo (37)**: slides de juegos secuenciales y el árbol de la Suficiencia 2026-1 (inducción hacia atrás, amenaza no creíble) · **A2 ej. 2** sin mirar (3.er grado frente a precio único, ¿excluir un grupo?) · 3 comentes del caso Daraprim (`2026-10-13-caso-daraprim-6-comentes.html`; Lerner) · paquetes en 3 líneas · Hotelling: centro frente a 1/4-3/4",
       "**μ6** (18:30, 38 min): matemático del **Control 2026-1** sin mirar (`2026-10-21-control-2026-1-matematico-resuelto.md`, 3.er grado) · comente **C13** (1.er grado). Después, nada más: a dormir temprano por Macro"],
'lun':["**μ7** (16:00, 39 min, antes de Historia): la **matriz de la PEP 1 2026-1** sin mirar · comente C13 o C10 con otras palabras · A4 ej. 5 rehecho en 5 líneas · paquetes: ¿cuándo conviene el paquete mixto?",
       "**μ8** (20:00, 88 min): **A4 ej. 3** sin mirar (3.er grado) · **A3 ej. 4** b) (dos partes) · un árbol nuevo (te lo genero en el chat) · una matriz nueva 3×3 · Hotelling en 3 líneas · PIE de 1.er grado en 3 líneas. *Si el martes dicen que no entran secuenciales, el árbol pasa a otra matriz*"],
'mar':["**μ9** (15:00, 112 min): **simulacro** `2026-11-04-simulacro-pep-1-mundaca.pdf` cronometrado (80 min) y corrección con `…-PAUTA-no-abrir.md` (30 min). Armar la **lista de errores de Micro** y pegar la nota en el chat (para recalibrar)",
       "**μ10** (21:30, 30 min, después de Historia): rehacer sin mirar lo que fallaste del simulacro en **dos partes** y en **juegos** (una matriz nueva). Después, a dormir"],
'mie':["**μ11** (18:30, 79 min, después de Sociología): **A3 ej. 4** (3.er grado con arbitraje) · un árbol con amenaza no creíble · Hotelling y bienestar · dos partes con dos tipos en 5 líneas · paquetes · paradoja del 1.er grado. **Micro queda cerrada aquí**"],
'jue':["**μ12** (13:10, 25 min, calentamiento único): una matriz rápida · el comente de competencia monopolística a LP · la lista de errores (veredicto en la primera palabra, IMg = P(1 − 1/|ε|), ES_CP − ES = PIE, ¿excluir un grupo?). Nada nuevo"]}
DAYS={'2026-11-02.md':{'vie':'2026-11-06','sab':'2026-11-07','dom':'2026-11-08'},
      '2026-11-09.md':{'lun':'2026-11-09','mar':'2026-11-10','mie':'2026-11-11','jue':'2026-11-12'}}
if __name__=='__main__':
    base='C:/Proyecto Metodologia de estudio/datos/agenda/semanas/'
    for fn,dd in DAYS.items():
        L=open(base+fn,encoding='utf-8').read().split('\n'); out=[]; day=None
        for ln in L:
            m=re.match(r'### (\d{4}-\d\d-\d\d)',ln)
            if m: day=next((k for k,v in dd.items() if v==m.group(1)),None)
            if ln.startswith('- [ ] Micro · **μ') and day:
                out+=['- [ ] Micro · '+x for x in S[day]]; continue
            out.append(ln)
        open(base+fn,'w',encoding='utf-8').write('\n'.join(out)); print(fn,'ok')
