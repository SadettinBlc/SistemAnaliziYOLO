import customtkinter as ctk
import subprocess

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("500x590") # 5 butona tam sığacak boyut
app.title("Visionary Control Center")

CREATE_NO_WINDOW = 0x08000000 

def baslat_postur():
    subprocess.Popen(["pythonw", "posture.py"], creationflags=CREATE_NO_WINDOW)

def baslat_oyun():
    subprocess.Popen(["pythonw", "controller.py"], creationflags=CREATE_NO_WINDOW)

def baslat_antrenor():
    subprocess.Popen(["pythonw", "trainer.py"], creationflags=CREATE_NO_WINDOW)

def baslat_sunum():
    subprocess.Popen(["pythonw", "presenter.py"], creationflags=CREATE_NO_WINDOW)

def baslat_medya():
    subprocess.Popen(["pythonw", "media.py"], creationflags=CREATE_NO_WINDOW)

# --- EKRAN TASARIMI ---
label_baslik = ctk.CTkLabel(app, text="Sistem Seçimi", font=("Helvetica", 28, "bold"))
label_baslik.pack(pady=(30, 20)) 

btn_postur = ctk.CTkButton(app, text="🩺 Posture Assistant", width=250, height=45, 
                           font=("Helvetica", 16, "bold"), fg_color="#2b7a0b", hover_color="#1f5a08",
                           command=baslat_postur)
btn_postur.pack(pady=8)

btn_oyun = ctk.CTkButton(app, text="⚔️ Elden Ring Controller", width=250, height=45, 
                         font=("Helvetica", 16, "bold"), fg_color="#b80000", hover_color="#8a0000",
                         command=baslat_oyun)
btn_oyun.pack(pady=8)

btn_antrenor = ctk.CTkButton(app, text="💪 AI Fitness Trainer", width=250, height=45, 
                         font=("Helvetica", 16, "bold"), fg_color="#d97706", hover_color="#b45309",
                         command=baslat_antrenor)
btn_antrenor.pack(pady=8)

btn_sunum = ctk.CTkButton(app, text="📊 Presentation Controller", width=250, height=45, 
                         font=("Helvetica", 16, "bold"), fg_color="#6d28d9", hover_color="#4c1d95",
                         command=baslat_sunum)
btn_sunum.pack(pady=8)

# YENİ BUTON (Mavi Renkli Medya Kontrolcüsü)
btn_medya = ctk.CTkButton(app, text="🎵 Media Controller", width=250, height=45, 
                         font=("Helvetica", 16, "bold"), fg_color="#0284c7", hover_color="#0369a1",
                         command=baslat_medya)
btn_medya.pack(pady=8)

label_bilgi = ctk.CTkLabel(app, text="Geliştirici : S.A.D.O", font=("Helvetica", 12), text_color="gray")
label_bilgi.pack(side="bottom", pady=15)

app.mainloop()