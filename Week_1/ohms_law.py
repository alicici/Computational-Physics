import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -----------------------------
# 1) VERİYİ OKU
# -----------------------------
# CSV aynı klasörde olmalı. (Gerekirse tam path ver.)
data = np.genfromtxt("VoltAmperData.csv", delimiter=",", names=True)

# Kolon isimleri I ve V (senin dosyada böyle)
I = data["I"].astype(float)
V = data["V"].astype(float)

# -----------------------------
# 2) TEK MODEL: V = R*I + b
# -----------------------------
def model(I, R, b):
    return R * I + b

# -----------------------------
# 3) FİT
# -----------------------------
popt, pcov = curve_fit(model, I, V)   # sigma yok: eşit ağırlıklı fit
R_fit, b_fit = popt

# (Opsiyonel) belirsizlik istersen:
dR_fit, db_fit = np.sqrt(np.diag(pcov))

# -----------------------------
# 4) SONUÇLARI YAZDIR
# -----------------------------
print("=== TEK MODEL FIT: V = R*I + b ===")
print(f"R = {R_fit:.6f} ohm")
print(f"b = {b_fit:.6f} V")

# İstersen belirsizlikleri de bas:
print(f"(opsiyonel) dR = {dR_fit:.6f} ohm, db = {db_fit:.6f} V")

# -----------------------------
# 5) GRAFİK (opsiyonel)
# -----------------------------
idx = np.argsort(I)
I_sorted = I[idx]
V_sorted = V[idx]

I_plot = np.linspace(I_sorted.min(), I_sorted.max(), 300)
V_plot = model(I_plot, R_fit, b_fit)

plt.figure()
plt.plot(I_sorted, V_sorted, "o", label="Ölçüm (CSV)")
plt.plot(I_plot, V_plot, "-", label="Fit: V = R I + b")
plt.xlabel("Akım I (A)")
plt.ylabel("Gerilim V (V)")
plt.title("Ohm Yasası: V-I Verisi ve Fit (Tek Model)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
