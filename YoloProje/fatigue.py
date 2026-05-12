import cv2
import winsound
from ultralytics import YOLO
import time
import threading

model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)

cv2.namedWindow("AI Fatigue Alarm", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AI Fatigue Alarm", cv2.WND_PROP_TOPMOST, 1)

uyku_baslangic = None
bekleme_limiti = 3.0  # 3 saniye boyunca kafa eğik kalırsa alarm çalar
alarm_caliyor = False

def alarm_sesi():
    """Arka planda bilgisayarın beep sesini çalan fonksiyon"""
    global alarm_caliyor
    while alarm_caliyor:
        winsound.Beep(1000, 500) # (Frekans, Süre milisaniye)
        time.sleep(0.1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    
    # Varsayılan değerler
    uyuyor_mu = False
    durum_mesaji = "DURUM NORMAL - DIKKAT YERINDE"
    renk = (0, 255, 0) # Yeşil

    for result in results:
        annotated_frame = result.plot()
        
        if result.keypoints is not None and len(result.keypoints) > 0:
            keypoints = result.keypoints.xy[0]
            
            # Burun (0) ve Omuzlar (5, 6) okundu mu?
            if len(keypoints) > 6:
                burun = keypoints[0]
                sol_omuz = keypoints[5]
                sag_omuz = keypoints[6]

                if burun[1] != 0 and sol_omuz[1] != 0 and sag_omuz[1] != 0:
                    # Omuzların Y eksenindeki ortalama yüksekliğini bul
                    omuz_y_ortalama = (sol_omuz[1] + sag_omuz[1]) / 2
                    
                    # Burun ile omuz arasındaki mesafeyi ölç (Kafa ne kadar dik?)
                    # Mesafe azaldıkça kafa öne eğilmiş (uykuya dalmış) demektir.
                    mesafe = omuz_y_ortalama - burun[1]
                    
                    # Ekranda referans çizgisi
                    nx, ny = int(burun[0]), int(burun[1])
                    oy = int(omuz_y_ortalama)
                    cv2.line(annotated_frame, (nx, ny), (nx, oy), (255, 255, 0), 2)
                    cv2.putText(annotated_frame, f"Kafa Dikligi: {int(mesafe)}px", (nx + 10, ny), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                    # Eğer mesafe eşik değerinin altındaysa (Örnek: 80 piksel - test ederek ayarlayabilirsin)
                    if mesafe < 80:
                        uyuyor_mu = True
                        if uyku_baslangic is None:
                            uyku_baslangic = time.time()
                        
                        gecen_sure = time.time() - uyku_baslangic
                        
                        if gecen_sure > bekleme_limiti:
                            durum_mesaji = "TEHLIKE: UYKU TESPIT EDILDI!"
                            renk = (0, 0, 255) # Kırmızı
                            
                            # Alarm çalmıyorsa başlat
                            if not alarm_caliyor:
                                alarm_caliyor = True
                                threading.Thread(target=alarm_sesi, daemon=True).start()
                        else:
                            durum_mesaji = f"UYARI: KAFA DUSUYOR! ({int(bekleme_limiti - gecen_sure)}s)"
                            renk = (0, 165, 255) # Turuncu
                    else:
                        # Kafa tekrar kalktıysa sistemi sıfırla
                        uyuyor_mu = False
                        uyku_baslangic = None
                        alarm_caliyor = False

    # HUD Arayüzü
    cv2.rectangle(annotated_frame, (0, 0), (640, 60), renk, -1)
    cv2.putText(annotated_frame, durum_mesaji, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0) if renk != (0,0,255) else (255,255,255), 2)

    cv2.imshow("AI Fatigue Alarm", annotated_frame)
    if cv2.waitKey(1) & 0xFF == 27:
        alarm_caliyor = False # Çıkarken alarmı sustur
        break

alarm_caliyor = False
cap.release()
cv2.destroyAllWindows()