import pandas as pd
import matplotlib.pyplot as plt

# Veri yükle
df = pd.read_csv("veriler/van_hava.csv", parse_dates=["Tarih"])

# Sıcaklık grafiği
plt.figure(figsize=(10,5))
plt.plot(df["Tarih"], df["Sıcaklık (°C)"], marker='o', label="Sıcaklık (°C)")
plt.title("Van - Son 7 Günlük Sıcaklık Değişimi")
plt.xlabel("Tarih")
plt.ylabel("Sıcaklık (°C)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("grafikler/sicaklik_grafigi.png")
plt.show()

# Günlük ortalama sıcaklık
print("Ortalama Sıcaklık:", df["Sıcaklık (°C)"].mean())
