import pandas as pd
R="C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/"
A=pd.read_csv(R+"2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv",sep=";",decimal=",",low_memory=False)
B=pd.read_csv(R+"3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv",sep=";",decimal=",",low_memory=False)
C=pd.read_csv(R+"4-matricula/ArchivoMatr_Adm2026.csv",sep=";",decimal=",",low_memory=False)
prev=[c for c in A.columns if (c.endswith("_ANTERIOR") or c.endswith("_INV_ACTUAL")) and not c.startswith("RINDIO")]
a=A[A.SITUACION_EGRESO==1]; print("egreso",len(a))
a=a[a[prev].isna().all(axis=1)]; print("primera vez",len(a))
a=a[(a.CLEC_REG_ACTUAL>=100)&(a.MATE1_REG_ACTUAL>=100)]; print("oblig",len(a))
a=a[(a.CIEN_REG_ACTUAL>=100)|(a.HCSOC_REG_ACTUAL>=100)]; print("electiva",len(a))
a=a[a.PROMEDIO_NOTAS!=0]; print("notas",len(a))
print("prev cols:",prev)
Bu=B.ID_aux.unique(); print("B unicos",len(Bu), "B TIPO_PREF", B.TIPO_PREF.value_counts().to_dict())
a["flag_postula"]=a.ID_aux.isin(Bu).astype(int); print("flag",a.flag_postula.value_counts().to_dict())
Cf=C[(C.VIA==1)&(C.TIPO_MATRICULA==1)]; print("C filtrado",len(Cf), "dup", Cf.ID_aux.duplicated().sum())
m=a.merge(Cf[["ID_aux","PREFERENCIA","VIA","TIPO_MATRICULA"]],on="ID_aux",how="left")
m["I"]=m.PREFERENCIA.isin([1,2,3]).astype(int)
print("N",len(m), m.I.value_counts().to_dict(), round(m.I.mean()*100,2))
print("matriculados regulares en A'",m.PREFERENCIA.notna().sum(), " pref4+",(m.PREFERENCIA>=4).sum(), " pref0",(m.PREFERENCIA==0).sum())
print(pd.crosstab(m.flag_postula,m.I,margins=True))
# matriculados sin postular?
print("matric sin flag", ((m.flag_postula==0)&m.PREFERENCIA.notna()).sum())
# matriculados en C pero otra via, dentro de A'
Co=C[~((C.VIA==1)&(C.TIPO_MATRICULA==1))]; print("otra via en A'", a.ID_aux.isin(Co.ID_aux).sum())
