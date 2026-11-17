import re, sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
P = "`agenda/plan-pep-noviembre.md`"
new = {
 "2026-11-23": ["08:00 caja de ecuaciones de Macro (20) → **PEP Macro** 09:50", "**Base 15:00** (65): E6 · μ4 · post-mortem de Macro (15)"],
 "2026-11-24": ["**Base 15:00** (65): E7 · μ5"],
 "2026-11-25": ["**Base 11:30** (65): E8 · μ6 (si E8 se adelantó: errores de Econometría y caja de fórmulas)", "**Base 13:45** (65): E9 · H2 (antes de Sociología 15:20)"],
 "2026-11-26": ["**PEP Econometría** 08:15", "12:50 caja de ecuaciones de Micro (20) → **PEP Micro** 13:45 (si se confirma)"],
 "2026-11-27": ["**Base 08:15** (65): H3 · H4 → **PEP Historia** 11:25"],
 "2026-11-28": ["Barrido y plan propio de **Política Económica** (PEP única 9-12) y **exposición de Sociología** (2-12); se retoma el informe de Política Económica"],
 "2026-11-29": ["**Libre.** Si abres el chat, «barrido» (5 min)"],
}
for d, items in new.items():
    block = "".join(f"- [ ] {x} ({P})\n" for x in items)
    t = re.sub(rf'(### {d} · \w+\n(?:(?!### ).*\n)*?)- \[ \] *\n?', lambda m: m.group(1) + block, t, count=1)
t = t.replace("Plan día a día.", f"Plan día a día. **Hasta el vie 27 manda el plan híbrido ({P}); si hay marcha blanca, usar su §6 (escenario B).**", 1)
open(p, 'w', encoding='utf-8').write(t)
