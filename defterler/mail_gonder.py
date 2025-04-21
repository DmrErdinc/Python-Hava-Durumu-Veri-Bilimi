import smtplib
import os
from email.message import EmailMessage

# Ayarlar
GONDEREN_EMAIL = "eraydemir300@gmail.com"  # BURAYA GMAIL'İNİ YAZ
SIFRE = "ejiv vcrc vopn zlsa"                # BURAYA Gmail'den aldığın UYGULAMA ŞİFRESİNİ yaz
ALICI_EMAIL = "eraydemir300@gmail.com"       # Kime göndereceksen

# E-posta içeriği
msg = EmailMessage()
msg["Subject"] = "📄 Van Hava Durumu Raporu"
msg["From"] = GONDEREN_EMAIL
msg["To"] = ALICI_EMAIL
msg.set_content("Merhaba Güncel Van hava durumu raporu ekte yer almaktadır.İyi günler dileriz!")

# Ek dosya
dosya_yolu = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "grafikler", "Van_rapor.pdf"))
if os.path.exists(dosya_yolu):
    with open(dosya_yolu, "rb") as f:
        dosya = f.read()
        msg.add_attachment(dosya, maintype="application", subtype="pdf", filename="Van_rapor.pdf")
else:
    print("❌ PDF dosyası bulunamadı:", dosya_yolu)
    exit()

dosya_yolu = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "grafikler", "sicaklik_grafigi.png"))
if os.path.exists(dosya_yolu):
    with open(dosya_yolu, "rb") as f:
        dosya = f.read()
        msg.add_attachment(dosya, maintype="application", subtype="png", filename="sicaklik_grafigi.png")
else:
    print("❌ PDF dosyası bulunamadı:", dosya_yolu)
    exit()

# Gönder
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GONDEREN_EMAIL, SIFRE)
        smtp.send_message(msg)
    print("✅ E-posta başarıyla gönderildi!")
except Exception as e:
    print("❌ Hata oluştu:", e)
