import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv

np.random.seed(42) # Rastgele sayi uretimi, 42 her defasinda ayni baslangic durumu icin yazilmaktadir. 

R_true = 220.0  # Direnc 220 ohm olarak ayarlandi.
b_true = 0.2   # Gerilimdeki kucuk kaymayi modellemek icin ekledik. (akim sifirken gerilimin sifir olmamasi durumunu temsil ediyor.)

I = np.linspace(0.0, 0.05, 100)  # linspace(a, b, N) a ile b arasinda a ve b dahil N tane esit aralikli sayi uret. a baslangic akimi b son akimi, N ise toplam olcum sayisini temsil etmektedir. 
V_err = 0.1 + 0.02*np.ones_like(I)  # ones_like(I) I dizisi ile ayni uzunlukta, her elemani 1 olan dizi uretir (0.02 olur). her elemana 0.03 ekler. Yani her V olcumunun belirsizligi 0.05V kadar olur.

V = R_true * I + b_true + np.random.normal(0.0, V_err) # gurultusuz ideal V = R_true * I. Gerilimdeki kucuk kaymanin eklenmis hali (V = R_true * I + b_true). Gaussian(normal) gurultu eklemis hali (V = R_true * I + b_true + np.random.normal(0.0, V_err))





with open("VoltAmperData.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["I", "V"])
    writer.writerows(zip(I, V))
