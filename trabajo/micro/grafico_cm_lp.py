import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out = sys.argv[1]
q = np.linspace(0, 14, 400)
cme = lambda x: 4 + 0.1 * (x - 10) ** 2
d = lambda x: 10.4 - 0.8 * x
img = lambda x: 10.4 - 1.6 * x
cmg = lambda x: 0.8 * x - 4

fig, ax = plt.subplots(figsize=(9, 6.5), dpi=200)
qa = np.linspace(2.6, 14, 300); ax.plot(qa, cme(qa), color="#534AB7", lw=2.4)
qb = np.linspace(5.4, 13.5, 100); ax.plot(qb, cmg(qb), color="#D85A30", lw=2.4)
qc = np.linspace(0, 13, 100); ax.plot(qc, d(qc), color="#0F6E56", lw=2.4)
qd = np.linspace(0, 6.5, 100); ax.plot(qd, img(qd), color="#0F6E56", lw=1.8, ls="--")
ax.fill([6, 6, 9], [5.6, 0.8, 3.2], color="#EF9F27", alpha=0.35)

kw = dict(color="gray", lw=0.8, ls=":")
ax.plot([0, 6], [5.6, 5.6], **kw); ax.plot([0, 6], [0.8, 0.8], **kw)
ax.plot([0, 10], [4, 4], **kw)
ax.plot([6, 6], [0, 5.6], **kw); ax.plot([10, 10], [0, 4], **kw)
ax.plot(6, 5.6, "o", color="#534AB7", ms=7); ax.plot(6, 0.8, "o", color="#D85A30", ms=7)
ax.plot(10, 4, "o", color="#534AB7", ms=7)

f = 13
ax.text(12.6, 0.9, "d", fontsize=f, color="#0F6E56", weight="bold")
ax.text(6.6, 0.3, "IMg", fontsize=f, color="#0F6E56", weight="bold")
ax.text(13.6, 6.9, "CMg", fontsize=f, color="#D85A30", weight="bold")
ax.text(13.9, 5.0, "CMe", fontsize=f, color="#534AB7", weight="bold")
ax.text(6.4, 3.0, "PIE", fontsize=f, weight="bold")
ax.annotate("Tangencia: P = CMe  →  π = 0", xy=(6, 5.6), xytext=(6.8, 8.3), fontsize=11,
            arrowprops=dict(arrowstyle="->", color="black"))
ax.annotate("IMg = CMg", xy=(6, 0.8), xytext=(1.6, 2.0), fontsize=11,
            arrowprops=dict(arrowstyle="->", color="black"))
ax.annotate("", xy=(5.92, 0.85), xytext=(5.92, 5.55), arrowprops=dict(arrowstyle="<->", color="#D85A30"))
ax.text(0.5, 3.1, "margen P* − CMg > 0 →", fontsize=10.5, color="#D85A30")
ax.annotate("", xy=(6.05, -0.75), xytext=(9.95, -0.75), annotation_clip=False,
            arrowprops=dict(arrowstyle="<->", color="#D85A30", lw=1.4))
ax.text(8, -1.3, "exceso de capacidad", ha="center", fontsize=11, color="#D85A30")

ax.set_xlim(0, 15); ax.set_ylim(0, 11)
ax.set_xticks([6, 10]); ax.set_xticklabels(["Q*", "Q mín CMe"], fontsize=12)
ax.set_yticks([0.8, 4, 5.6]); ax.set_yticklabels(["CMg", "CMe mín", "P* = CMe"], fontsize=12)
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("Q", fontsize=13, loc="right"); ax.set_ylabel("$", fontsize=13, loc="top", rotation=0)
ax.set_title("Competencia monopolística: equilibrio de largo plazo (una empresa)", fontsize=13)
fig.text(0.5, 0.015, "P = CMe > CMg  →  PIE y exceso de capacidad.  En CP: P = CMg = CMe mín.",
         ha="center", fontsize=11.5)
fig.subplots_adjust(bottom=0.2)
fig.savefig(out, bbox_inches="tight", facecolor="white")
print("ok")
