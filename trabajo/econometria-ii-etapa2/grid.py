import pandas as pd, itertools
R="C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/"
A=pd.read_csv(R+"2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv",sep=";",decimal=",",low_memory=False)
a=A[A.SITUACION_EGRESO==1]
allc=[c for c in A.columns if (c.endswith("_ANTERIOR") or c.endswith("_INV_ACTUAL")) and not c.startswith("RINDIO")]
oblig=[c for c in allc if c.split("_")[0] in ("CLEC","MATE1")]
nomod=[c for c in allc if not c.startswith("MODULO")]
prev={"todas":allc,"oblig":oblig,"sinmod":nomod,"rindio_ant":None}
ob={"cada>100":lambda d:(d.CLEC_REG_ACTUAL>100)&(d.MATE1_REG_ACTUAL>100),
    "cada>=100":lambda d:(d.CLEC_REG_ACTUAL>=100)&(d.MATE1_REG_ACTUAL>=100),
    "suma>100":lambda d:(d.CLEC_REG_ACTUAL+d.MATE1_REG_ACTUAL)>100,
    "cada>0":lambda d:(d.CLEC_REG_ACTUAL>0)&(d.MATE1_REG_ACTUAL>0)}
el={">100":lambda d:(d.CIEN_REG_ACTUAL>100)|(d.HCSOC_REG_ACTUAL>100),
    ">=100":lambda d:(d.CIEN_REG_ACTUAL>=100)|(d.HCSOC_REG_ACTUAL>=100),
    ">0":lambda d:(d.CIEN_REG_ACTUAL>0)|(d.HCSOC_REG_ACTUAL>0),
    "ninguno":lambda d:d.CLEC_REG_ACTUAL==d.CLEC_REG_ACTUAL|True}
for (pk,pc),(ok,of),(ek,ef) in itertools.product(prev.items(),ob.items(),el.items()):
  d=a[a.RINDIO_PROCESO_ANTERIOR!=1] if pc is None else a[a[pc].isna().all(axis=1)]
  d=d[of(d)]; d=d[ef(d)] if ek!="ninguno" else d; d=d[d.PROMEDIO_NOTAS!=0]
  n=len(d); print(("*** " if abs(n-168714)<=5 else "    ")+f"{pk:10} {ok:9} {ek:7} {n}")
print(A.RINDIO_PROCESO_ANTERIOR.value_counts(dropna=False))
