import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# =============================
# 1) VERI
# =============================
np.random.seed(42)

g_true = 9.81      # m/s^2
y0_true = 1.5      # m
v0_true = 0.2      # m/s

t = np.linspace(0.0, 0.6, 12)     # s
y_err = 0.01 * np.ones_like(t)    # m (her noktada 1 cm belirsizlik)

# Olculen y: model + guruktu
y = y0_true + v0_true*t - 0.5*g_true*t**2 + np.random.normal(0.0, y_err)


# =============================
# 2) MODEL
# =============================
def free_fall_model(t, y0, v0, g):
    return y0 + v0*t - 0.5*g*t**2

# =============================
# 3) FIT
# =============================
"""
curve_fit(...) fonksiyonu
veri olarak aldigimiz noktalar t ve y (bunlari yukarida kendimiz olusturduk. Deneyden elde edilen veriler gibi dusunulebilir.) Matematiksel modelimiz ise y0 + v0*t - 0.5*g*t**2. Bu modele en uygun y0, v0 ve g degerlerini bulmayi amacliyoruz.
sigma=y_err: her noktanin y belirsizligini fit'e verir (kucuk hata -> daha fazla agirlik)
absolute_sigma=True: y_err mutlak olcum hatasi kabul edilir, bu sayede parametre hatalari dogru olceklenir.
popt = [y0_fit, v0_fit, g_fit] -> fitten cikan en iyi parametreler
pcov: parametre kovaryans matrisi; diag(pcov) = [Var(y0), Var(v0), Var(g)]
sqrt(diag(pcov)) -> [dy0, dv0, dg] (1-sigma belirsizlikler)
"""

popt, pcov = curve_fit(
    free_fall_model, t, y,
    sigma=y_err, absolute_sigma=True
)
y0_fit, v0_fit, g_fit = popt
dy0, dv0, dg = np.sqrt(np.diag(pcov))

print("=== Serbest Dusme Fit Sonuclari ===")
print(f"y0 = {y0_fit:.5f} +- {dy0:.5f} m")
print(f"v0 = {v0_fit:.5f} +- {dv0:.5f} m/s")
print(f"g  = {g_fit:.5f} +- {dg:.5f} m/s^2")

print("\n Karsilastirma:")
print(f"Bilinen g = 9.81 m/s^2 | Fark = {g_fit - 9.81:+.5f} m/s^2")

# =============================
# 4) GRAFIK
# =============================
t_plot = np.linspace(t.min(), t.max(), 300)
y_fit_curve = free_fall_model(t_plot, y0_fit, v0_fit, g_fit)

plt.figure()
plt.errorbar(t, y, yerr=y_err, fmt='o', capsize=3, label='Olcumm (error bar)')
plt.plot(t_plot, y_fit_curve, label='Quadratic fit: y0+v0 t - 1/2 g t^2')

plt.xlabel("Zaman t (s)")
plt.ylabel("Yukseklik y (m)")
plt.title("Serbest Dusme: y(t) Verisi ve Fit ile g Tahmini")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

