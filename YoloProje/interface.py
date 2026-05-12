import customtkinter as ctk
import subprocess

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

# 10 butona tam sığması için pencereyi uzattık
app = ctk.CTk()
app.geometry("500x900") 
app.title("S.A.D.O. Control Center") # Başlığı da S.A.D.O yaptık!

CREATE_NO_WINDOW = 0x08000000 

def baslat_postur(): subprocess.Popen(["pythonw", "posture.py"], creationflags=CREATE_NO_WINDOW)
def baslat_oyun(): subprocess.Popen(["pythonw", "controller.py"], creationflags=CREATE_NO_WINDOW)
def baslat_antrenor(): subprocess.Popen(["pythonw", "trainer.py"], creationflags=CREATE_NO_WINDOW)
def baslat_sunum(): subprocess.Popen(["pythonw", "presenter.py"], creationflags=CREATE_NO_WINDOW)
def baslat_medya(): subprocess.Popen(["pythonw", "media.py"], creationflags=CREATE_NO_WINDOW)
def baslat_guvenlik(): subprocess.Popen(["pythonw", "security.py"], creationflags=CREATE_NO_WINDOW)
def baslat_cizim(): subprocess.Popen(["pythonw", "canvas.py"], creationflags=CREATE_NO_WINDOW)
def baslat_eco(): subprocess.Popen(["pythonw", "eco.py"], creationflags=CREATE_NO_WINDOW)
def baslat_yorgunluk(): subprocess.Popen(["pythonw", "fatigue.py"], creationflags=CREATE_NO_WINDOW)
def baslat_gizlilik(): subprocess.Popen(["pythonw", "privacy.py"], creationflags=CREATE_NO_WINDOW)

# --- EKRAN TASARIMI ---
label_baslik = ctk.CTkLabel(app, text="Sistem Seçimi", font=("Helvetica", 28, "bold"))
label_baslik.pack(pady=(30, 15)) 

btn_postur = ctk.CTkButton(app, text="🩺 Posture Assistant", width=250, height=45, font=("Helvetica", 16, "bold"), fg_color="#2b7a0b", hover_color="#1f5a08", command=baslat_postur)
btn_postur.pack(pady=7)

btn_oyun = ctk.CTkButton(app, text="⚔️ Elden Ring Controller", width=250, height=45, font=("Helvetica", 16, "bold"), fg_color="#b80000", hover_color="#8a0000", command=baslat_oyun)
btn_oyun.pack(pady=7)

btn_antrenor = ctk.CTkButton(app, text="💪 AI Fitness Trainer", width=250, height=45, font=("Helvetica", 16, "bold"), fg_color="#d97706", hover_color="#b45309", command=baslat_antrenor)
btn_antrenor.pack(pady=7)

btn_sunum = ctk.CTkButton(app, text="📊 Presentation Controller", width=250, height=45, font=("Helvetica", 16, "bold"), fg_color="#6d28d9", hover_color="#4c1d95", command=baslat_sunum)
btn_sunum.pack(pady=7)

btn_medya = ctk.CTkButton(app, text="🎵 Media Controller", width=250, height=45, font=("Helvetica", 16, "bold"), fg_color="#0284c7", hover_color="#0369a1", command=baslat_medya)
btn_medya.pack(pady=7)

btn_guvenlik = ctk.CTkButton(app, text="🚨 AI Security Guard", width=250, height=45, font=("Helvetica", 16, "bold"), fg_color="#991b1b", hover_color="#7f1d1d", command=baslat_guvenlik)
btn_guvenlik.pack(pady=7)

btn_cizim = ctk.CTkButton(app, text="🎨 Air Canvas", width=250, height=45, font=("Helvetica", 16, "bold"), fg_color="#0f766e", hover_color="#115e59", command=baslat_cizim)
btn_cizim.pack(pady=7)

btn_eco = ctk.CTkButton(app, text="🌱 AI Eco-Manager", width=250, height=45, font=("Helvetica", 16, "bold"), fg_color="#15803d", hover_color="#166534", command=baslat_eco)
btn_eco.pack(pady=7)

btn_yorgunluk = ctk.CTkButton(app, text="⚠️ AI Fatigue Alarm", width=250, height=45, font=("Helvetica", 16, "bold"), fg_color="#c2410c", hover_color="#9a3412", command=baslat_yorgunluk)
btn_yorgunluk.pack(pady=7)

# FİNAL İÇİN YENİ BUTON: Gizlilik Kalkanı (Lacivert / Gece Mavisi)
btn_gizlilik = ctk.CTkButton(app, text="🕵️‍♂️ AI Privacy Shield", width=250, height=45, font=("Helvetica", 16, "bold"), fg_color="#1e3a8a", hover_color="#172554", command=baslat_gizlilik)
btn_gizlilik.pack(pady=7)

# S.A.D.O İMZASI
label_bilgi = ctk.CTkLabel(app, text="Developed by S.A.D.O", font=("Helvetica", 16, "bold", "italic"), text_color="#9ca3af")
label_bilgi.pack(side="bottom", pady=20)

app.mainloop()