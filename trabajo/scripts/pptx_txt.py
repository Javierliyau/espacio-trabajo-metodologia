import sys
from pptx import Presentation
from pptx.util import Emu
for path in sys.argv[1:]:
    p = Presentation(path)
    print("=====", path.split("/")[-1], len(p.slides), "slides")
    for i, s in enumerate(p.slides, 1):
        print(f"--- diap {i}")
        for sh in s.shapes:
            kinds = []
            if sh.has_text_frame:
                t = "\n".join(par.text for par in sh.text_frame.paragraphs if par.text.strip())
                if t: print(t)
            elif getattr(sh, "has_table", False) and sh.has_table:
                for r in sh.table.rows:
                    print(" | ".join(c.text.strip() for c in r.cells))
            elif getattr(sh, "has_chart", False) and sh.has_chart:
                print("[GRAFICO]", sh.chart.chart_title.text_frame.text if sh.chart.has_title else "")
            elif sh.shape_type == 13:
                print("[IMAGEN]")
            elif sh.shape_type == 6:
                for x in sh.shapes:
                    if x.has_text_frame and x.text_frame.text.strip(): print(x.text_frame.text)
        if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
            print("[NOTAS]", s.notes_slide.notes_text_frame.text)
