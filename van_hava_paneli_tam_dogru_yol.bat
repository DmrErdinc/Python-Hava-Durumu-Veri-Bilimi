@echo off
title  VAN HAVA DURUMU OTOMASYON PANELI 
color 0A
echo Baslatiliyor...
cd /d "C:\Users\Dmr.Erdinc\Desktop\VAN Hava durumu\defterler"
echo [1/2] E-posta sistemi calisiyor...
python mail_gonder.py

"C:\Users\Dmr.Erdinc\AppData\Roaming\Python\Python313\Scripts\streamlit.exe" run "C:\Users\Dmr.Erdinc\Desktop\VAN Hava durumu\defterler\streamlit_panel.py"
echo [2/2] Streamlit Panel Başlatılıyor..

pause

