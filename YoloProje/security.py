import cv2
from ultralytics import YOLO
import time
import os
from datetime import datetime

# Fotoğrafların kaydedileceği klasörü otomatik oluştur
if not os.path.exists("Security_Logs"):
    os.makedirs("Security_Logs")

model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)

cv2.namedWindow("AI Security Guard", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AI Security Guard", cv2.WND_PROP_TOPMOST, 1)

son_kayit_zamani = 0
bekleme_suresi = 3.0  # Aynı adamın saniyede 30 fotoğrafını çekmesin diye 3 sn bekleme

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    insan_tespit_edildi = False

    for result in results:
        annotated_frame = result.plot()
        
        # Eğer bir iskelet noktası okunuyorsa, ekranda biri var demektir
        if result.keypoints is not None and len(result.keypoints) > 0:
            keypoints = result.keypoints.xy[0]
            
            # Yeterli doğrulukta eklem okunuyorsa tehlike çanları çalsın
            if len(keypoints) > 5:
                insan_tespit_edildi = True
                su_an = time.time()
                
                # 3 saniyede bir temiz (çizgisiz) kareyi log klasörüne kaydet
                if su_an - son_kayit_zamani > bekleme_suresi:
                    zaman_damgasi = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    dosya_adi = f"Security_Logs/Intruder_{zaman_damgasi}.jpg"
                    cv2.imwrite(dosya_adi, frame)
                    son_kayit_zamani = su_an

    # HUD Arayüzü (Durum Bildirimi)
    if insan_tespit_edildi:
        cv2.rectangle(annotated_frame, (0, 0), (640, 70), (0, 0, 255), -1)
        cv2.putText(annotated_frame, "TEHLIKE: INSAN TESPIT EDILDI!", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        cv2.putText(annotated_frame, "Fotograf Kaydediliyor...", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        cv2.rectangle(annotated_frame, (0, 0), (640, 70), (0, 200, 0), -1)
        cv2.putText(annotated_frame, "GUVENLI: ORTAM TEMIZ", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

    cv2.imshow("AI Security Guard", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC ile çıkış
        break

cap.release()
cv2.destroyAllWindows()