p=r'C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-02-lectura-pep1-casos-reales.tex'
s=open(p,encoding='utf-8').read()
BS='\'
for key in ['Atributo: puntos} ','más de 51: 105 ','Cheque, MasterCard u otras: 99 ','tiene: 93 ','más de 2,55 MM: 105 ']:
    old=key+BS+'\n'; new=key+BS+BS+'\n'
    assert s.count(old)==1,(key,s.count(old)); s=s.replace(old,new)
s=s.replace(BS+'tema{4.3. El caso SLEP',BS+'tema{4.2. El caso SLEP').replace(BS+'tema{4.4. Supuestos',BS+'tema{4.3. Supuestos')
s=s.replace('& 50'+BS+',\% & 5 & 4.3 '.replace('\%',BS+'%'),'& 50'+BS+','+BS+'% & 5 & 4.2 ')
open(p,'w',encoding='utf-8').write(s)
