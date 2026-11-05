import json, glob, os, sys
from datetime import datetime, timezone, timedelta
from collections import defaultdict
BASE = os.path.expanduser("~/.claude/projects")
DIRS = {"C--Espacio-de-trabajo-Metodologia-de-estudio":"espacio","C--Proyecto-Metodologia-de-estudio":"proyecto","C--Proyecto-Informe-PIB-Tendencial":"informe"}
TZ = timezone(timedelta(hours=-3))  # Chile, horario de verano desde sep
INICIO = datetime(2026,9,21,tzinfo=TZ)
GAP = int(sys.argv[1]) if len(sys.argv)>1 else 15
evs = []
for d,lab in DIRS.items():
    for f in glob.glob(os.path.join(BASE,d,"*.jsonl")):
        for line in open(f,encoding="utf-8",errors="ignore"):
            try: o = json.loads(line)
            except: continue
            if o.get("isSidechain"): continue
            if o.get("type")!="user": continue   # solo turnos del estudiante = actividad humana
            m = o.get("message",{}); c = m.get("content")
            if isinstance(c,list) and all(isinstance(x,dict) and x.get("type")=="tool_result" for x in c): continue
            ts = o.get("timestamp")
            if not ts: continue
            t = datetime.fromisoformat(ts.replace("Z","+00:00")).astimezone(TZ)
            if t>=INICIO: evs.append((t,lab))
evs.sort()
# tiempo activo: tramos entre mensajes del estudiante separados por <= GAP min; +5 min por cada bloque (lectura/trabajo final)
tot=timedelta(); dia=defaultdict(timedelta); lab_t=defaultdict(timedelta); semana=defaultdict(timedelta)
prev=None
for t,lab in evs:
    if prev and t-prev[0] <= timedelta(minutes=GAP):
        d=t-prev[0]
    else:
        d=timedelta(minutes=5)
    tot+=d; dia[t.date()]+=d; lab_t[lab]+=d
    lunes=t.date()-timedelta(days=t.weekday()); semana[lunes]+=d
    prev=(t,lab)
h=lambda x: f"{x.total_seconds()/3600:.1f} h"
print("mensajes",len(evs),"umbral",GAP,"min · total",h(tot),"· días con actividad",len(dia))
for k,v in sorted(semana.items()): print(" semana",k,h(v))
for k,v in lab_t.items(): print(" ",k,h(v))
print(" día máx", max(dia.items(),key=lambda x:x[1]))
