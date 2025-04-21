import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import os

# Sayfa ayarları
st.set_page_config(page_title="Van Hava Durumu", layout="centered")
st.title("🌤️ Van Hava Durumu Analiz Paneli")

# CSV dosyasının yolu
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "veriler", "van_hava.csv"))
if not os.path.exists(csv_path):
    st.error(f"CSV dosyası bulunamadı: {csv_path}")
    st.stop()

# Veri yükleme
df = pd.read_csv(csv_path, parse_dates=["Tarih"])
df.sort_values("Tarih", inplace=True)

# 🌍 Anlık Hava Durumu (OpenWeatherMap API)
st.subheader("📡 Gerçek Zamanlı Van Hava Durumu (API)")

if st.button("API'den Güncel Veriyi Al ve Kaydet"):
    api_key = "c4d50e3f84b0bd9a07b38ac859b9fc68e"
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Van,tr&appid={api_key}&units=metric&lang=tr"
    r = requests.get(url)
    if r.status_code == 200:
        veri = r.json()
        sicaklik = veri["main"]["temp"]
        nem = veri["main"]["humidity"]
        ruzgar = veri["wind"]["speed"]
        tarih = datetime.now().strftime("%Y-%m-%d")
        yeni_veri = pd.DataFrame({
            "Tarih": [tarih],
            "Sıcaklık (°C)": [sicaklik],
            "Nem (%)": [nem],
            "Rüzgar Hızı (km/s)": [ruzgar]
        })
        df = pd.concat([df, yeni_veri], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.success("✅ Yeni veri eklendi!")
    else:
        st.error("❌ API'den veri alınamadı.")

# 📋 Veri Tablosu
st.subheader("📊 Veri Tablosu")
st.dataframe(df.tail(10))

# 📈 Grafikler
st.subheader("📅 Tarih Aralığı Seç")
min_date, max_date = df["Tarih"].min(), df["Tarih"].max()
tarih_aralik = st.date_input("Tarih aralığını seçin", [min_date, max_date])

if len(tarih_aralik) == 2:
    baslangic, bitis = tarih_aralik
    filtreli_df = df[(df["Tarih"] >= pd.to_datetime(baslangic)) & (df["Tarih"] <= pd.to_datetime(bitis))]

    st.subheader("🌡️ Sıcaklık Grafiği")
    fig1, ax1 = plt.subplots()
    ax1.plot(filtreli_df["Tarih"], filtreli_df["Sıcaklık (°C)"], marker='o', color='tomato')
    ax1.set_xlabel("Tarih")
    ax1.set_ylabel("Sıcaklık (°C)")
    ax1.set_title("Seçili Tarihler Arası Sıcaklık")
    ax1.grid(True)
    st.pyplot(fig1)

    st.subheader("💧 Nem Grafiği")
    fig2, ax2 = plt.subplots()
    ax2.plot(filtreli_df["Tarih"], filtreli_df["Nem (%)"], marker='s', color='skyblue')
    ax2.set_xlabel("Tarih")
    ax2.set_ylabel("Nem (%)")
    ax2.set_title("Seçili Tarihler Arası Nem")
    ax2.grid(True)
    st.pyplot(fig2)

    st.subheader("💨 Rüzgar Hızı Grafiği")
    fig3, ax3 = plt.subplots()
    ax3.plot(filtreli_df["Tarih"], filtreli_df["Rüzgar Hızı (km/s)"], marker='^', color='green')
    ax3.set_xlabel("Tarih")
    ax3.set_ylabel("Rüzgar Hızı (km/s)")
    ax3.set_title("Seçili Tarihler Arası Rüzgar Hızı")
    ax3.grid(True)
    st.pyplot(fig3)

# 📊 Detaylı İstatistikler
st.subheader("📋 İstatistik Özeti")
col1, col2, col3 = st.columns(3)
col1.metric("Ortalama Sıcaklık", f"{df['Sıcaklık (°C)'].mean():.1f} °C")
col2.metric("Maksimum Nem", f"{df['Nem (%)'].max()} %")
col3.metric("Minimum Rüzgar", f"{df['Rüzgar Hızı (km/s)'].min()} km/s")
