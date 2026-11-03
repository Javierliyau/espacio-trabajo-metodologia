import re,glob,os,sys
D=sys.argv[1]
pat=re.compile(r"prueba|\bpep\b|calculadora|va a entrar|entra en|entrar[áa]|evaluar|eval[uú]e|eval[uú]o|examen|un bloque|dos bloques|les voy a preguntar|le voy a preguntar|voy a preguntar|tienen que aprender|aprend[ée]nselo|tienen que saber|ojo con|importante|pregunta de|en la prueba",re.I)
out=[]
for f in sorted(glob.glob(os.path.join(D,'*.txt'))):
    t=open(f,encoding='utf-8',errors='replace').read()
    ts=[(m.start(),m.group(1)) for m in re.finditer(r"\[(\d\d:\d\d:\d\d)\]",t)]
    last=-10**9
    out.append("\n######## "+os.path.basename(f))
    for m in pat.finditer(t):
        if m.start()-last<500: continue
        last=m.start()
        stamp=max([s for s in ts if s[0]<=m.start()] or [(0,'?')])[1]
        a=max(0,m.start()-280); b=min(len(t),m.end()+320)
        out.append(f"[{stamp}] ({m.group(0)}) ..."+re.sub(r"\s+"," ",t[a:b])+"...")
open(os.path.join(os.path.dirname(__file__),'pistas-crudas.txt'),'w',encoding='utf-8').write("\n".join(out))
print(len(out))
