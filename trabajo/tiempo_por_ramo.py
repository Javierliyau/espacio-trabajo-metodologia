import json, glob, os, re, sys
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter
BASE=os.path.expanduser("~/.claude/projects")
DIRS={"C--Espacio-de-trabajo-Metodologia-de-estudio":"espacio","C--Proyecto-Metodologia-de-estudio":"proyecto","C--Proyecto-Informe-PIB-Tendencial":"informe"}
TZ=timezone(timedelta(hours=-3)); INICIO=datetime(2026,9,21,tzinfo=TZ); GAP=15
R={
 "Econometría II":[r"econometr",r"\blogit",r"\bWOE\b",r"woebin",r"scoring",r"\bDiD\b",r"diferencias en diferencias",r"dicom",r"\bSLEP\b",r"wooldridge",r"incinerador",r"\bIV\b",r"tramifica"],
 "Macroeconomía II":[r"macroecon",r"macro ii",r"\bmacro\b",r"solow",r"romer",r"droller",r"schumpeter",r"capital humano",r"convergencia"],
 "Microeconomía II":[r"microecon",r"micro ii",r"\bmicro\b"],
 "Historia Económica":[r"historia econ",r"\bhistoria\b",r"o.rourke",r"feinstein",r"danilo",r"revista \d"],
 "Política Económica / Informe 43":[r"pol[ií]tica econ",r"informe",r"tema 43",r"pib tendencial",r"filtro hp",r"hodrick"],
 "Sociología Económica":[r"sociolog"],
 "Taller de Comunicación":[r"taller de comunic"],
 "Sistema y método":[r"agenda",r"metodolog[ií]a perry",r"perry",r"mazur",r"\bhook",r"\bskill",r"graphify",r"\bctx\b",r"handoff",r"kindle-estudio",r"orquestador"],
}
RX={k:[re.compile(p,re.I if not p.startswith(r"\b") or p.lower()==p else 0) for p in v] for k,v in R.items()}
def txt(c):
    if isinstance(c,str): return c
    out=[]
    for x in c or []:
        if isinstance(x,dict) and x.get("type")=="text": out.append(x.get("text",""))
    return "\n".join(out)
def clean(s):
    s=re.sub(r"<system-reminder>.*?</system-reminder>","",s,flags=re.S)
    s=re.sub(r"(?i)metodolog[ií]a de estudio|Informe PIB Tendencial","",s)
    return s
def score(s):
    c=Counter()
    for k,rs in RX.items():
        for r in rs: c[k]+=len(r.findall(s))
    return +c
evs=[]
for d,lab in DIRS.items():
    for f in glob.glob(os.path.join(BASE,d,"*.jsonl")):
        seq=[]
        for line in open(f,encoding="utf-8",errors="ignore"):
            try:o=json.loads(line)
            except: continue
            if o.get("isSidechain") or o.get("isMeta"): continue
            t=o.get("type")
            if t not in("user","assistant"): continue
            c=o.get("message",{}).get("content")
            if t=="user" and isinstance(c,list) and all(isinstance(x,dict) and x.get("type")=="tool_result" for x in c): continue
            s=clean(txt(c)); ts=o.get("timestamp")
            if not ts: continue
            seq.append((datetime.fromisoformat(ts.replace("Z","+00:00")).astimezone(TZ),t,s))
        tot=Counter()
        for _,_,s in seq: tot+=score(s)
        default="Política Económica / Informe 43" if lab=="informe" else (tot.most_common(1)[0][0] if tot else "Sin clasificar")
        cur=None; win=[]
        for tm,t,s in seq:
            sc=score(s)
            if lab=="informe": cur=default
            elif sc:
                # ventana de los últimos 4 mensajes para no saltar por una mención suelta
                win=(win+[sc])[-4:]; agg=sum(win,Counter()); cur=agg.most_common(1)[0][0]
            if t=="user" and tm>=INICIO: evs.append((tm,cur or default))
evs.sort()
ramo=defaultdict(timedelta); sem=defaultdict(lambda:defaultdict(timedelta)); prev=None
for tm,r in evs:
    d=(tm-prev) if prev and tm-prev<=timedelta(minutes=GAP) else timedelta(minutes=5)
    ramo[r]+=d; sem[tm.date()-timedelta(days=tm.weekday())][r]+=d; prev=tm
T=sum(ramo.values(),timedelta())
for r,v in sorted(ramo.items(),key=lambda x:-x[1]): print(f"{r:34s} {v.total_seconds()/3600:6.1f} h  {100*v/T:4.0f} %")
print("total",round(T.total_seconds()/3600,1))
ks=[r for r,_ in sorted(ramo.items(),key=lambda x:-x[1])]
print("semana;"+";".join(k[:10] for k in ks))
for w in sorted(sem): print(str(w)[5:]+";"+";".join(f"{sem[w][k].total_seconds()/3600:.1f}" for k in ks))
