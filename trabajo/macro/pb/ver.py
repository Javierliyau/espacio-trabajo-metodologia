import re,sys
s=open(sys.argv[1],encoding='utf8').read()
vf=s[s.index(r'\section*{Verdadero o Falso'):]
it=re.split(r'(?=^.item \(12 puntos\))',vf,flags=re.M)[1:]
for k,x in enumerate(it):
    n=14+k
    if n in (15,18,20,22,23,24,25,27,30,32,34,35):
        r=x.split(r'\begin{resp}')[1]
        print(n, re.sub(r'\s+',' ',r)[:150])
