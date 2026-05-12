import cv2
from ultralytics import YOLO
import time
import pyautogui

model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)

cv2.namedWindow("AI Privacy Shield", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AI Privacy Shield", cv2.WND_PROP_TOPMOST, 1)

son_tetiklenme_zamani = 0
bekleme_suresi = 10.0 # Arkadaki kişi gitmeden sürekli masaüstüne dönmesin diye 10 saniye bekleme süresi (Cooldown)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    
    # Ekranda kaç kişi olduğunu sayıyoruz
    kisi_sayisi = 0
    if results[0].keypoints is not None:
        # YOLO'nun bulduğu her bir iskelet (kişi) sayısını al
        kisi_sayisi = len(results[0].keypoints.xy)

    su_an = time.time()
    durum_mesaji = "GUVENLI: SADECE SEN VARSIN"
    renk = (0, 200, 0) # Yeşil

    # Eğer kadrajda 1'den fazla insan varsa (yani arkana biri geldiyse)
    if kisi_sayisi >= 2:
        durum_mesaji = f"TEHLIKE: {kisi_sayisi} KISI TESPIT EDILDI!"
        renk = (0, 0, 255) # Kırmızı
        
        if su_an - son_tetiklenme_zamani > bekleme_suresi:
            # Otonom olarak Windows + D tuşlarına bas (Tüm pencereleri aşağı al)
            pyautogui.hotkey('win', 'd')
            son_tetiklenme_zamani = su_an

    # HUD Arayüzü
    annotated_frame = results[0].plot()
    cv2.rectangle(annotated_frame, (0, 0), (640, 60), renk, -1)
    cv2.putText(annotated_frame, durum_mesaji, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Ekranda kaç kişi olduğunu sağ üste yaz
    cv2.putText(annotated_frame, f"Kisi Sayisi: {kisi_sayisi}", (450, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("AI Privacy Shield", annotated_frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()