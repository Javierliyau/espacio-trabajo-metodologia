import pathlib
p = pathlib.Path(r"C:/Espacio de trabajo Metodologia de estudio/trabajo/libro/estilo_libro.py")
L = p.read_text(encoding="utf-8").split("\n")
i = [k for k, l in enumerate(L) if l.startswith('    cuerpo = cuerpo.replace(r"\\section*{"')][0]
L[i:i + 2] = ['    cuerpo = cuerpo.replace(r"\\section*{", r"\\needspace{8\\baselineskip}\\section*{")']
p.write_text("\n".join(L), encoding="utf-8")
print(L[i])
