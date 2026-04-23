import cv2
from ultralytics import YOLO
import pydirectinput
import time

model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)

cv2.namedWindow("AI Presentation Controller", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AI Presentation Controller", cv2.WND_PROP_TOPMOST, 1)

son_hareket_zamani = time.time()
bekleme_suresi = 1.5 
durum_mesaji = "HAZIR (Sistemi Acmak Icin Elini Kaldir)"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Ayna Görüntü
    frame = cv2.flip(frame, 1)
    
    results = model(frame, verbose=False)

    for result in results:
        annotated_frame = result.plot()
        
        if result.keypoints is not None and len(result.keypoints) > 0:
            keypoints = result.keypoints.xy[0]
            
            if len(keypoints) > 10:
                sag_omuz = keypoints[6]
                sag_bilek = keypoints[10]

                if sag_omuz[1] != 0 and sag_bilek[1] != 0:
                    # Eli omuz hizasının yukarısına kaldırdığında sistem aktifleşir
                    if sag_bilek[1] < sag_omuz[1]:
                        dx = sag_bilek[0] - sag_omuz[0]
                        
                        # Ekranda referans çizgisi ve noktalar
                        so_x, so_y = int(sag_omuz[0]), int(sag_omuz[1])
                        sb_x, sb_y = int(sag_bilek[0]), int(sag_bilek[1])
                        cv2.circle(annotated_frame, (so_x, so_y), 50, (255, 0, 0), 2)
                        cv2.line(annotated_frame, (so_x, so_y), (sb_x, sb_y), (0, 255, 255), 2)

                        su_an = time.time()
                        if su_an - son_hareket_zamani > bekleme_suresi:
                            durum_mesaji = "KOMUT BEKLENIYOR..."
                            if dx > 80: # El sağa gitti
                                pydirectinput.press('right')
                                durum_mesaji = "-> SONRAKI SLAYT"
                                son_hareket_zamani = su_an
                            elif dx < -80: # El sola gitti
                                pydirectinput.press('left')
                                durum_mesaji = "<- ONCEKI SLAYT"
                                son_hareket_zamani = su_an
                    else:
                        durum_mesaji = "ELINI KALDIR"

        # HUD Arayüzü
        cv2.rectangle(annotated_frame, (0, 0), (600, 60), (0, 0, 0), -1)
        cv2.putText(annotated_frame, durum_mesaji, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("AI Presentation Controller", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()