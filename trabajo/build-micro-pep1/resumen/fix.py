import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
BS = chr(92)
s = s.replace(chr(8) + "eckmark", "eckmark")
s = s.replace(chr(8), "")
s = s.replace("$eckmark$", "$" + BS + "checkmark$")
open(p, "w", encoding="utf-8").write(s)
print(s.count(BS + "checkmark"), s.count(chr(8)))
