import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -----------------------------
# 1) Veri Uretimi
# -----------------------------
np.random.seed(42) # Rastgele sayi uretimi, 42 her defasinda ayni baslangic durumu icin yazilmaktadir. 

R_true = 220.0  # Direnc 220 ohm olarak ayarlandi.
b_true = 0.2   # Gerilimdeki kucuk kaymayi modellemek icin ekledik. (akim sifirken gerilimin sifir olmamasi durumunu temsil ediyor.)

I = np.linspace(0.0, 0.05, 12)  # linspace(a, b, N) a ile b arasinda a ve b dahil N tane esit aralikli sayi uret. a baslangic akimi b son akimi, N ise toplam olcum sayisini temsil etmektedir. 
V_err = 0.1 + 0.02*np.ones_like(I)  # ones_like(I) I dizisi ile ayni uzunlukta, her elemani 1 olan dizi uretir (0.02 olur). her elemana 0.03 ekler. Yani her V olcumunun belirsizligi 0.05V kadar olur.

V = R_true * I + b_true + np.random.normal(0.0, V_err) # gurultusuz ideal V = R_true * I. Gerilimdeki kucuk kaymanin eklenmis hali (V = R_true * I + b_true). Gaussian(normal) gurultu eklemis hali (V = R_true * I + b_true + np.random.normal(0.0, V_err))
print(V)

# -----------------------------
# 2) MODEL tanımı
# -----------------------------
def model_with_intercept(I, R, b):
    return R * I + b

def model_through_origin(I, R):
    return R * I

# -----------------------------
# 3) FİT (A) V = R I + b
# -----------------------------
"""
scipy.optimize.curve_fit, verilen modele en iyi uyan parametreleri bulur. V = R I + b gibi
model_with_intercept'in dondurdugu deger R * I + b. Sigma = V_err = 0.03 + 0.02*np.ones_like(I) seklindeydi. Ilk arguman bagimsiz degisken: I sonrakiler fit parametreleri R, b. 

absolute_sigma=True demek: "Verilen sigma degerleri gercek olcum belirsizlikleridir, olceklendirme yapma."

R_fit, b_fit = popt ( en iyi bulunan direnc, en iyi bulunan gerilimdeki kucuk kayma)


pcov Parametre kovaryans matrisi: diag(pcov) = [Var(R), Var(b)] belirsizlikler dR, db; off-diag  R ile b arasindaki korelasyon

"""
popt, pcov = curve_fit(
    model_with_intercept, I, V,
    sigma=V_err, absolute_sigma=True
)
R_fit, b_fit = popt
dR_fit, db_fit = np.sqrt(np.diag(pcov))

# -----------------------------
# 4) FİT (B) V = R I (orijinden)
# -----------------------------
popt0, pcov0 = curve_fit(
    model_through_origin, I, V,
    sigma=V_err, absolute_sigma=True
)
R0_fit = popt0[0]
dR0_fit = np.sqrt(pcov0[0, 0])

# -----------------------------
# 5) RAPORLA
# -----------------------------
print("=== FIT A: V = R*I + b ===")
print(f"R = {R_fit:.4f} +- {dR_fit:.4f} ohm")
print(f"b = {b_fit:.4f} +- {db_fit:.4f} V")

print("\n=== FIT B: V = R*I (orijinden) ===")
print(f"R = {R0_fit:.4f} +- {dR0_fit:.4f} ohm")

# -----------------------------
# 6) GRAFİK
# -----------------------------
I_plot = np.linspace(I.min(), I.max(), 200)

plt.figure()
plt.errorbar(I, V, yerr=V_err, fmt='o', capsize=3, label='Ölçüm (error bar)')
plt.plot(I_plot, model_with_intercept(I_plot, R_fit, b_fit), label='Fit: V=RI+b')
plt.plot(I_plot, model_through_origin(I_plot, R0_fit), label='Fit: V=RI (0 kesişim)')

plt.xlabel("Akım I (A)")
plt.ylabel("Gerilim V (V)")
plt.title("Ohm Yasası: V-I Verisi ve Doğrusal Fit")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

