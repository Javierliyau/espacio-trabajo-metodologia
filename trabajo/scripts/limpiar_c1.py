import json, re, sys
ruta = sys.argv[1]
d = json.load(open(ruta, encoding='utf-8'))
P = d['preguntas']
of = {p['n']: p for p in P if p.get('pauta')}
p2 = of['2']
p2['enunciado'] = 'Defina qué es un sendero de crecimiento balanceado.'
nuevas = []
for n in ['1', '2', '3', '4', '5']:
    p = of[n]
    e = p['enunciado']
    e = re.sub(r'^Verdadero o Falso\. Justifique su respuesta\.\s*', '', e)
    e = re.sub(r'^\d\. \(12 puntos\)\s*', '', e)
    if n in ('3', '4', '5'):
        e = 'Verdadero o Falso. Justifique su respuesta. ' + e
    p['enunciado'] = e
    p['puntaje'] = '12 puntos'
    p['pauta_origen'] = 'oficial'
    nuevas.append(p)
d['preguntas'] = nuevas
d['resumen'] = ('Control de lectura de Macroeconomía II (Droller, 2026-2), rendido el 26-10-2026, texto oficial con pauta. '
                'Modelo de Solow sin progreso técnico: P1 derivar k̇/k = s·y/k − (δ+n) y graficar s·y/k contra n+δ (12 pts); '
                'P2 definir sendero de crecimiento balanceado (12); P3-P5 verdadero/falso con el mismo gráfico: '
                'terremoto que destruye la mitad de K (F: el crecimiento es rápido al inicio), dos países con igual y que crecen distinto (F: s_X > s_Y), '
                'caída de n (V: acelera en el corto plazo, igual g de largo plazo). Total 60 pts.')
d['dudas'] = []
d['parcial'] = False
d['fuentes'] = [f for f in d['fuentes'] if f.get('contenido') == 'ambos'] + [f for f in d['fuentes'] if f.get('contenido') != 'ambos']
json.dump(d, open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
for p in nuevas: print(p['n'], p['tipo_pregunta'], p['temas'], p['enunciado'][:60])
