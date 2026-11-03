import pandas as pd, numpy as np, sys
R="C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/"
A=pd.read_csv(R+"2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv",sep=";",decimal=",",low_memory=False)
B=pd.read_csv(R+"3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv",sep=";",decimal=",",low_memory=False)
C=pd.read_csv(R+"4-matricula/ArchivoMatr_Adm2026.csv",sep=";",decimal=",",low_memory=False)
print("A",A.shape,"B",B.shape,"C",C.shape, "B unicos",B.ID_aux.nunique())
print(A.SITUACION_EGRESO.value_counts(dropna=False).head())
print(A[["PROMEDIO_NOTAS","CLEC_REG_ACTUAL","MATE1_REG_ACTUAL","CIEN_REG_ACTUAL","HCSOC_REG_ACTUAL"]].describe().T)
ant=[c for c in A.columns if c.endswith("_ANTERIOR") and not c.startswith("RINDIO")]
inv=[c for c in A.columns if c.endswith("_INV_ACTUAL")]
s=[len(A)]
a=A[A.SITUACION_EGRESO==1]; s.append(len(a))
a1=a[a[ant+inv].isna().all(axis=1)]; s.append(len(a1))
a2=a1[(a1.CLEC_REG_ACTUAL>100)&(a1.MATE1_REG_ACTUAL>100)]; s.append(len(a2))
for op in [">",">="]:
  el=(a2.CIEN_REG_ACTUAL>100)|(a2.HCSOC_REG_ACTUAL>100) if op==">" else (a2.CIEN_REG_ACTUAL>=100)|(a2.HCSOC_REG_ACTUAL>=100)
  a3=a2[el]; a4=a3[a3.PROMEDIO_NOTAS!=0]
  print(op, s+[len(a3),len(a4)])
# variante: solo REG_ANTERIOR, INV_ACTUAL, INV_ANTERIOR por prueba obligatoria
