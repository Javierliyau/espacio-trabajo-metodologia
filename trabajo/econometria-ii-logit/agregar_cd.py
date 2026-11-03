from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

ruta = "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-logit/logit-ejercicio-b.xlsx"
wb = load_workbook(ruta)
F = "Arial"
azul = Font(name=F, color="0000FF"); verdeF = Font(name=F, color="008000")
negro = Font(name=F); neg = Font(name=F, bold=True); tit = Font(name=F, bold=True, size=13)
nota = Font(name=F, italic=True, color="666666")
amarillo = PatternFill("solid", fgColor="FFFF00"); gris = PatternFill("solid", fgColor="D9E1F2")
verde = PatternFill("solid", fgColor="E2EFDA")
borde = Border(*(Side(style="thin", color="999999"),) * 4)
B = "'Ejercicio b'!"

def enc(ws, fila, heads):
    for j, h in enumerate(heads, start=1):
        c = ws.cell(fila, j, h); c.font = neg; c.fill = gris; c.border = borde
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    ws.row_dimensions[fila].height = 45

def put(ws, r, col, val, fmt=None, font=negro, fill=None):
    c = ws.cell(r, col, val); c.font = font; c.border = borde
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    return c

# ---------- (c) ----------
ws = wb.create_sheet("Ejercicio c")
ws["A1"] = "(c) Interpretación de β_price y efecto de bajar el precio en 1 dólar"; ws["A1"].font = tit
ws["A2"] = "Verde = vínculo a la hoja 'Ejercicio b'. Amarillo = dato editable."; ws["A2"].font = nota

ws["A4"] = "β1 (price)"; put(ws, 4, 2, f"={B}B6", "0.0000", verdeF)
ws["A5"] = "Cambio en price (Δprice)"; put(ws, 5, 2, -1, "0", azul, amarillo)
ws["A7"] = "1) En logit (log-odds)"; ws["A7"].font = neg
ws["A8"] = "Cambio en z = β1·Δprice"; put(ws, 8, 2, "=B4*B5", "0.0000")
ws["A9"] = "2) En odds"; ws["A9"].font = neg
ws["A10"] = "Factor de las odds = e^(β1·Δprice)"; put(ws, 10, 2, "=EXP(B4*B5)", "0.0000")
ws["A11"] = "Cambio % en las odds = 100·(e^(β1·Δ) − 1)"; put(ws, 11, 2, "=B10-1", "0.00%")
ws["A12"] = "3) En probabilidad: efecto máximo (en P = 0,5, g = 0,25)"; ws["A12"].font = neg
ws["A13"] = "|ΔP| máx ≈ 0,25·|β1·Δprice|"; put(ws, 13, 2, "=0.25*ABS(B8)", "0.00%")

ws["A15"] = "Efecto en la probabilidad para los individuos de (b): depende de dónde estén en la curva"; ws["A15"].font = neg
enc(ws, 16, ["Caso", "price", "income", "z", "P", "g(z) = P·(1−P)",
             "ΔP aprox = g·β1·Δprice", "P nueva (exacta)", "ΔP exacto"])
casos = [("A) Ind. 1 (income $)", 11), ("A) Ind. 2 (income $)", 12),
         ("B) Ind. 1 (income miles)", 18), ("B) Ind. 2 (income miles)", 19)]
for k, (n, rb) in enumerate(casos):
    r = 17 + k
    put(ws, r, 1, n)
    put(ws, r, 2, f"={B}B{rb}", "0", verdeF)
    put(ws, r, 3, f"={B}C{rb}", "#,##0", verdeF)
    put(ws, r, 4, f"={B}$B$5+{B}$B$6*B{r}+{B}$B$7*C{r}", "0.0000")
    put(ws, r, 5, f"=1/(1+EXP(-D{r}))", "0.0000%")
    put(ws, r, 6, f"=E{r}*(1-E{r})", "0.000000")
    put(ws, r, 7, f"=F{r}*$B$4*$B$5", "0.0000%", fill=verde)
    put(ws, r, 8, f"=1/(1+EXP(-(D{r}+$B$4*$B$5)))", "0.0000%")
    put(ws, r, 9, f"=H{r}-E{r}", "0.0000%", fill=verde)
ws["A22"] = "Lectura: el coeficiente es fijo, pero el efecto en P es g(z)·β, máximo cerca de P = 0,5 y casi cero en los extremos."
ws["A22"].font = nota

# ---------- (d) ----------
ws = wb.create_sheet("Ejercicio d")
ws["A1"] = "(d) Mismo precio (40), ingresos de 1000 y 500 dólares"; ws["A1"].font = tit
ws["A2"] = "Verde = vínculo a la hoja 'Ejercicio b'. Amarillo = dato editable."; ws["A2"].font = nota
enc(ws, 4, ["Persona", "price", "income", "Paso 1: z", "e^(−z)", "Paso 2: P", "Odds = e^z"])
for k, ing in enumerate([1000, 500]):
    r = 5 + k
    put(ws, r, 1, f"Persona {'AB'[k]}")
    put(ws, r, 2, 40, "0", azul, amarillo)
    put(ws, r, 3, ing, "#,##0", azul, amarillo)
    put(ws, r, 4, f"={B}$B$5+{B}$B$6*B{r}+{B}$B$7*C{r}", "0.0000")
    put(ws, r, 5, f"=EXP(-D{r})", "0.000000")
    put(ws, r, 6, f"=1/(1+E{r})", "0.00%", fill=verde)
    put(ws, r, 7, f"=EXP(D{r})", "0.0000")
put(ws, 7, 1, "Diferencia (A − B)", font=neg)
put(ws, 7, 4, "=D5-D6", "0.0000")
put(ws, 7, 6, "=F5-F6", "0.00%", fill=verde)
ws["A9"] = "Razón de odds A/B"; put(ws, 9, 2, "=G5/G6", "0.0000")
ws["A10"] = "Comprobación: e^(β2·Δincome)"; put(ws, 10, 2, f"=EXP({B}B7*(C5-C6))", "0.0000")
ws["A11"] = "Cambio % en las odds"; put(ws, 11, 2, "=B9-1", "0.00%")
ws["A13"] = "Lectura: 500 dólares más de ingreso suben z en 0,15; las odds suben ~16 % y la probabilidad ~1,9 pp."
ws["A13"].font = nota

for name in ("Ejercicio c", "Ejercicio d"):
    s = wb[name]; s.column_dimensions["A"].width = 44
    for col in "BCDEFGHI": s.column_dimensions[col].width = 15
wb.save(ruta)
