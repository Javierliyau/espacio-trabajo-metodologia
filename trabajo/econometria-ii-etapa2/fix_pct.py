import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
fix = lambda m: m.group(0).replace("\\%", "\\text{\\%}")
s = re.sub(r"(?<!\\)\$[^$\n]+?(?<!\\)\$", fix, s)
s = re.sub(r"\\\[.+?\\\]", fix, s, flags=re.S)
open(p, "w", encoding="utf-8").write(s)
print(s.count("\\text{\\%}"))
