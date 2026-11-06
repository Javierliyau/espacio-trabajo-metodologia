import re,sys; sys.stdout.reconfigure(encoding='utf-8')
from micro_v2 import S
f='C:/Proyecto Metodologia de estudio/datos/material/microeconomia-ii/2026-11-06-plan-conjunto-pep1-econometria-micro.md'
t=open(f,encoding='utf-8').read()
i2=t.index('## 2. Las reglas'); i4=t.index('## 4. Las sesiones'); i5=t.index('## 5. Jueves')
mid=t[i2:i4]; s4=t[i4:i5]; rest=t[i5:]
key={'vie 6':'vie','sáb 7':'sab','dom 8':'dom','lun 9':'lun','mar 10':'mar','mié 11':'mie','jue 12':'jue'}
out=[]
for ln in s4.split('\n'):
    m=re.match(r'\| \*\*(\S+ \d+)\*\* \|',ln)
    if m and m.group(1) in key:
        c=ln.split(' | '); c[2]=' · '.join(x.replace('|','\|') for x in S[key[m.group(1)]]); ln=' | '.join(c)
    out.append(ln)
s4='\n'.join(out)
s4=s4.replace('**Micro: sesiones μ1-μ7, sin cambios.**','**Micro: sesiones μ1-μ12** (704 min; cada tema vuelve 3-6 veces, espaciado).')
s4=re.sub(r'\*\*Carga de estas dos materias por día.*',"**Carga de Econometría + Micro por día (min):** vie 175 · sáb 180 · dom 165 · lun 163 · mar 195 · mié 131 · jue 55. Con Macro e Historia, ningún día pasa de ~5 h (tabla del §1). Si un día pesa, se recorta primero lo de menor peso de ese día: paquetes (M9) y Hotelling (M6).",s4)
rest=rest.replace('| 13:10-13:35 | μ7: calentamiento único de Micro, solo lo ya repasado |','| 13:10-13:35 | μ12: calentamiento único de Micro, solo lo ya repasado |')
rest=re.sub(r'- \*\*Si haces los opcionales de Econometría \(418 min\)\*\*.*',"- **Si haces los opcionales de Econometría (418 min)**: el viernes pasaría el tope. En ese caso μ2 (20:30) se queda solo con C3 y D1, y paquetes y A4 ej. 5 pasan al inicio de μ3. Los opcionales del lunes (A7) y del martes caben.",rest)
rest=re.sub(r'- \*\*Si falta tiempo\*\*.*',"- **Si falta tiempo**: primero se recortan los opcionales de Econometría (5,12 en vez de 5,25). Después, Micro baja a la versión intermedia (600 min, 5,22): μ4 se queda en 30 min (solo comentes de juegos y A4 ej. 4), μ7 en 23 min (matriz de la PEP 2026-1 y C13) y μ9 solo corrige los ítems de juegos y de 3.er grado. **Nunca se recortan** juegos estáticos (M7), 3.er grado (M1), dos partes (M2), probit (T15) ni el `glm` (T4). **Macro no se toca nunca.**",rest)
rest=rest.replace('ver μ4)','ver μ5 y μ8)').replace('μ7 se corre para que quede','μ12 se corre para que quede')
rest=rest.replace('o si el simulacro de Micro del martes sale bajo 4,5','o si el simulacro de Micro del martes (μ9) sale bajo 4,5')
rest=rest.replace('`eval_agenda.py`: evalúa las sesiones μ1-μ7 de la agenda.','`joint4.py`: Micro al máximo con franjas nuevas (vie 20:30, sáb y dom 18:30, lun 16:00, mar 21:30) y un tope de ~5 h de estudio total por día, descontando Macro e Historia.')
top=open('top.md',encoding='utf-8').read()
open(f,'w',encoding='utf-8').write(top+'\n'+mid+s4+rest)
print('ok')
