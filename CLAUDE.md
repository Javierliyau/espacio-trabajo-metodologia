# Espacio de trabajo: Metodología de estudio

Chat liviano para trabajar: ejercicios, dudas y temas de los ramos, preparar pruebas. Aquí no se guarda nada permanente.

## Fuente única: `C:/Proyecto Metodologia de estudio` (PROYECTO)

Todo se lee directo del PROYECTO (siempre al día, sin copias). Leer solo lo que el pedido necesita, por rango:

| Qué | Dónde (dentro del PROYECTO) |
|---|---|
| Protocolo de cada ramo (leer primero al tratar un ramo) | `datos/programas/<ramo>-protocolo-chat.md` |
| Reglas comunes de los chats de ramo | `metodologia-perry-mazur/11-protocolo-chat-ramos.md` |
| Clases registradas | `datos/clases/AAAA-MM-DD-<ramo>-*.md` |
| Material por ramo | `datos/material/<ramo>/` |
| Programas, bibliografía, tema semestral | `datos/programas/`, `datos/bibliografia-textos.md`, `datos/tema-semestral/` |
| Metodología | `metodologia-perry-mazur/` |
| Pruebas y pautas pasadas | skill `banco-evaluaciones` |
| Costo en tokens de cada archivo | `.claude/ctx/INDICE.md` |

Preguntas amplias sobre el contenido: `cd "C:/Proyecto Metodologia de estudio" && graphify query "<pregunta>"`.

## Reglas

- Borradores y ejercicios en curso: `trabajo/` de este espacio (desechable).
- Lo que vale la pena conservar (clase nueva, ejercicio resuelto, resumen, prueba, pauta, cambio de método) se guarda en el PROYECTO, en su carpeta y con el formato de los archivos vecinos. Avisa en una línea qué archivo creaste o editaste.
- No edites `CLAUDE.md` ni `.claude/` del PROYECTO desde aquí.

## Agenda (fechas, plan del día y bitácora)

Vive en el PROYECTO: `datos/agenda/` (ver su `README.md`). Al abrir el chat, un hook muestra la agenda del día.
`AG` = `"C:/Users/javie/AppData/Local/Python/pythoncore-3.14-64/python.exe" "C:/Proyecto Metodologia de estudio/datos/agenda/agenda.py"`

- «¿Qué hacemos hoy?» / «¿qué viene?» → `AG hoy` y proponer sobre eso.
- Fecha nueva, cambiada o cumplida → editar `datos/agenda/calendario.md` (estado incluido) antes que cualquier otro archivo.
- Al terminar cada tarea → `AG anotar "<ramo>" "<qué se hizo, archivo, qué queda>"` y marcar `[x]` en `datos/agenda/semanas/<lunes>.md`.
- Planificar una semana → `AG nueva-semana <fecha>` y repartir en los días según `horario.md`.

## Informe de Politica Economica (Tema 43)
Se trabaja en su propio proyecto: `C:\Proyecto Informe PIB Tendencial` (abrir esa carpeta y usar `/retomar informe-43`). No se trabaja aqui.
- **Aporte automático:** al cerrar una sesión de Macro II (u otro ramo con líneas «para el informe»), anotar esas líneas como entrada fechada en `datos/informe-pe/aportes-desde-ramos.md` del PROYECTO (aporte · sección · rigor V/C · estado `nuevo`; formato de las entradas vecinas) y avisar en una línea. No hace falta que el estudiante lo pida.
