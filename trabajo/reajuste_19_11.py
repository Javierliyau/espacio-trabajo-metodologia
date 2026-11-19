import re, os
os.chdir("C:/Proyecto Metodologia de estudio/datos/agenda")
R = '(`agenda/plan-pep-noviembre.md` §3 bis)'
INF = 'con `/retomar informe-43`'
plan = {
 '2026-11-23': ['**Base 10:00** (65): E5 · μ4 ' + R,
   '**Política Económica 11:30** (45): lecturas de la PEP única, en el orden de `material/politica-economica/2026-11-09-lecturas-pep-unica.md` ' + R,
   '**Informe I4** (15:00-17:00, ' + INF + '): columna G (16 cifras contra el PDF) y Figura 2 (erizo) (`agenda/plan-pep-noviembre.md` §4 bis)'],
 '2026-11-24': ['**Base 10:00** (65): E6 · H2 = ficha R2 ' + R,
   '**Política Económica 11:30** (45): lecturas ' + R,
   '**Informe I5** (15:00-17:00, ' + INF + ') (`agenda/plan-pep-noviembre.md` §4 bis)'],
 '2026-11-25': ['**Base 10:00** (65): E7 · μ5 ' + R,
   '**Política Económica 11:30** (45): lecturas ' + R,
   '**Informe H3** (15:00-17:00, ' + INF + '): hoja de sensibilidad (`agenda/plan-pep-noviembre.md` §4 bis)',
   '*Seguro:* 21:00 caja de fórmulas de Econometría (20), por si la PEP va el jue 26 ' + R],
 '2026-11-26': ['**Vuelta a clases.** Si la PEP de Econometría va hoy, se rinde; si no, clases normales ' + R,
   '**Base 17:00** (65): E8 · μ6 (si hubo PEP de Econometría: su post-mortem (15) + μ6) ' + R,
   '*Seguro:* si la PEP de Historia se confirma para el vie 27, en la noche H3 · H4 (fichas R4, C e índice) ' + R],
 '2026-11-27': ['**Base 16:45** (65): H3 = ficha R4 · H4 = fichas C + índice (si no se hicieron ayer) · si sobra, E9 ' + R],
 '2026-11-28': ['**Macro 10:00: mini-ensayo de 50 min con reloj** (D−2, si la PEP es el lun 30) + corrección (20) ' + R,
   '**Tarde** (60): exposición de Bauman con Ana, guion y reparto (30) · plan propio de Política Económica hasta el 9-12 (30) ' + R],
 '2026-11-29': ['**Macro 10:00** (30): errores del mini-ensayo y caja de ecuaciones (D−1) ' + R,
   '**Historia 11:00** (30): pregunta con reloj y con las fichas en la mano (formato §9 del método de fichas) ' + R,
   'El resto del día libre; dormir temprano'],
 '2026-11-30': ['08:00 caja de Macro (20) → **PEP Macro** 09:50 *(fecha supuesta)* ' + R,
   '**Base 15:00** (65): **Micro: mini-ensayo de 50 min con reloj** (D−3) · post-mortem de Macro (15) ' + R],
 '2026-12-01': ['**Base 15:00** (65): **Econometría: mini-ensayo de 50 min con reloj** (D−2) + corrección ' + R,
   '17:00 ensayo de la exposición con Ana, con reloj, ≤ 15 min (20) ' + R],
 '2026-12-02': ['**11:15-12:15**: errores de Econometría y de Micro, más las dos cajas de fórmulas (D−1) ' + R,
   '**EXPOSICIÓN de Sociología: Bauman con Ana** (16:55)',
   'Noche: Historia, ordenar el mazo y leer las tesis (15) ' + R],
 '2026-12-03': ['**PEP Econometría** 08:15 · 12:50 caja de Micro (20) → **PEP Micro / Control 2** 13:45 *(fechas supuestas)* ' + R],
 '2026-12-04': ['**PEP Historia** 11:25 *(fecha supuesta)* · desde la tarde, plan de Política Económica (PEP del mié 9) ' + R],
}
paro = {'2026-11-23', '2026-11-24', '2026-11-25'}
for f in ['semanas/2026-11-23.md', 'semanas/2026-11-30.md']:
    s = open(f, encoding='utf-8').read()
    parts = re.split(r'(?m)^(### \d{4}-\d\d-\d\d · \w+)$', s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        h = parts[i]; body = parts[i + 1]; d = h[4:14]
        if d in paro:
            body = body.replace('\nClases: ', '\nClases (**en paro, no hay**): ', 1)
        items = plan.get(d)
        if items:
            assert '- [ ] \n' in body, d
            body = body.replace('- [ ] \n', '\n'.join('- [ ] ' + x for x in items) + '\n', 1)
        out += h + body
    if f.endswith('23.md'):
        out = out.replace('Plan día a día.', 'Plan día a día. **Paro FEUSACH hasta el mié 25 (23:59); vuelta el jue 26. Fechas de PEP supuestas: Macro lun 30, Econometría y Micro jue 3-12, Historia vie 4-12; los seguros cubren Econometría el 26 e Historia el 27** (`agenda/plan-pep-noviembre.md` §3 bis).', 1)
    open(f, 'w', encoding='utf-8').write(out)

f = 'semanas/2026-11-16.md'; s = open(f, encoding='utf-8').read()
for a, b in [
    ('**Base 10:00** (65): μ1 · M5', '**Base 10:00** (65): μ1 · M4 (ítem 0 de la cola; reajuste 19-11, §3 bis)'),
    ('**Base 15:00** (65): E3 · M6', '**Base 15:00** (65): E3 · M5'),
    ('**Base 15:00** (65): E4 · M7', '**Base 15:00** (65): E4 · M6'),
    ('**Base 10:00** (65): μ3 · E5', '**Base 10:00** (65): μ3 · M7 (E5 pasa al lun 23)'),
    ('- [ ] *(opcional)* **Ensayo Econometría 15:00**: Bloque 1 completo', '- [~] *(opcional)* **Ensayo Econometría 15:00**: Bloque 1 completo → pasa al mini-ensayo del mar 1-12 (§3 bis); la tarde del sáb queda libre'),
]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(f, 'w', encoding='utf-8').write(s)

f = 'plan-pep-noviembre.md'; s = open(f, encoding='utf-8').read()
bis = open('C:/Espacio de trabajo Metodologia de estudio/trabajo/seccion_3bis.md', encoding='utf-8').read()
a = '## 4. Cola de trozos extra'
assert s.count(a) == 1
s = s.replace(a, bis + '\n' + a, 1)
s = s.replace('(**solo hasta el sáb 21**', '(**hasta el sáb 28**, reajuste 19-11')
open(f, 'w', encoding='utf-8').write(s)
print('ok')
