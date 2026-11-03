from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

wb = Workbook()
ws = wb.active
ws.title = "Ejercicio b"

F = "Arial"
azul = Font(name=F, color="0000FF")
negro = Font(name=F)
neg = Font(name=F, bold=True)
tit = Font(name=F, bold=True, size=13)
amarillo = PatternFill("solid", fgColor="FFFF00")
gris = PatternFill("solid", fgColor="D9E1F2")
verde = PatternFill("solid", fgColor="E2EFDA")
borde = Border(*(Side(style="thin", color="999999"),) * 4)

ws["A1"] = "Logit: P(Buy=1 | price, income) = Λ(β0 + β1·price + β2·income) = 1 / (1 + e^(−z))"
ws["A1"].font = tit
ws["A2"] = "Celdas en azul con fondo amarillo = datos que puedes cambiar. Todo lo demás son fórmulas."
ws["A2"].font = Font(name=F, italic=True, color="666666")

# Parámetros
ws["A4"] = "Parámetros del modelo"; ws["A4"].font = neg
params = [("β0 (constante)", 3.5), ("β1 (price)", -0.05), ("β2 (income)", 0.0003)]
for i, (n, v) in enumerate(params, start=5):
    ws.cell(i, 1, n).font = negro
    c = ws.cell(i, 2, v); c.font = azul; c.fill = amarillo; c.border = borde
ws["B6"].comment = Comment("En la foto no se ve el signo entre 3,5 y 0,05; se asume negativo (más precio, menos compra).", "Claude")

def tabla(fila0, titulo, ingresos, nota):
    ws.cell(fila0, 1, titulo).font = neg
    heads = ["Individuo", "price", "income", "Paso 1: z = β0 + β1·price + β2·income",
             "e^(−z)", "Paso 2: P = 1/(1+e^(−z))", "P (%)"]
    for j, h in enumerate(heads, start=1):
        c = ws.cell(fila0 + 1, j, h); c.font = neg; c.fill = gris; c.border = borde
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    for k, (precio, ing) in enumerate(zip([50, 80], ingresos)):
        r = fila0 + 2 + k
        ws.cell(r, 1, f"Individuo {k+1}").font = negro
        for col, val in ((2, precio), (3, ing)):
            c = ws.cell(r, col, val); c.font = azul; c.fill = amarillo
        ws.cell(r, 4, f"=$B$5+$B$6*B{r}+$B$7*C{r}")
        ws.cell(r, 5, f"=EXP(-D{r})")
        ws.cell(r, 6, f"=1/(1+E{r})")
        ws.cell(r, 7, f"=F{r}")
        ws.cell(r, 4).number_format = "0.0000"
        ws.cell(r, 5).number_format = "0.000000"
        ws.cell(r, 6).number_format = "0.000000"
        ws.cell(r, 7).number_format = "0.00%"
        for j in range(1, 8):
            ws.cell(r, j).border = borde
            if j >= 4: ws.cell(r, j).font = negro
        ws.cell(r, 6).fill = verde; ws.cell(r, 7).fill = verde
    r = fila0 + 4
    ws.cell(r, 1, "Diferencia (2 − 1)").font = neg
    ws.cell(r, 4, f"=D{r-1}-D{r-2}").number_format = "0.0000"
    ws.cell(r, 6, f"=F{r-1}-F{r-2}").number_format = "0.000000"
    ws.cell(r, 7, f"=G{r-1}-G{r-2}").number_format = "0.00%"
    ws.cell(r + 1, 1, nota).font = Font(name=F, italic=True, color="666666")

tabla(9, "A) Lectura literal: income en dólares (28 mil = 28.000)", [28000, 28000],
      "Los dos están en la parte plana de la S (z alto): subir el precio en 30 casi no cambia P.")
tabla(16, "B) Alternativa: income en miles (28)", [28, 28],
      "Si el profesor usó el ingreso en miles, la diferencia de precio sí mueve mucho la probabilidad.")

ws.column_dimensions["A"].width = 26
for col, w in zip("BCDEFG", [11, 11, 26, 13, 20, 11]):
    ws.column_dimensions[col].width = w
ws.row_dimensions[10].height = 32; ws.row_dimensions[17].height = 32
for row in ws.iter_rows():
    for c in row:
        if c.font.name != F:
            c.font = Font(name=F, bold=c.font.bold, italic=c.font.italic, color=c.font.color)

wb.save("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-logit/logit-ejercicio-b.xlsx")
