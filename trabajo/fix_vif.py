import sys
p=sys.argv[1]
s=open(p,encoding='utf-8',newline='').read()
nl='\r\n' if '\r\n' in s else '\n'
s=s.replace('\r\n','\n')
a=s.index(r"una. Usamos el umbral del curso")
b=s.index(r"\textbf{Variables definitivas y signo esperado.}")
new=open(sys.argv[2],encoding='utf-8').read()
s=s[:a]+new+s[b:]
s=s.replace(r"\usepackage{caption}", r"\usepackage{caption}"+"\n"+r"\usepackage{needspace}")
open(p,'w',encoding='utf-8',newline='').write(s.replace('\n',nl))
