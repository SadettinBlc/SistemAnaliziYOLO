import cv2
import math
from ultralytics import YOLO

# Açı hesaplama fonksiyonu (Trigonometri)
def calculate_angle(a, b, c):
    angle = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    if angle < 0:
        angle += 360
    if angle > 180:
        angle = 360 - angle
    return angle

model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)

cv2.namedWindow("AI Fitness Trainer", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AI Fitness Trainer", cv2.WND_PROP_TOPMOST, 1)

tekrar_sayisi = 0
hareket_yonu = 0 # 0: Asagida, 1: Yukarida
form_mesaji = "HAZIRLAN..."

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO'yu sessiz modda çalıştır (Konsola log basmasın)
    results = model(frame, verbose=False)

    for result in results:
        annotated_frame = result.plot()
        
        if result.keypoints is not None and len(result.keypoints) > 0:
            keypoints = result.keypoints.xy[0]
            
            if len(keypoints) > 10:
                sag_omuz = keypoints[6]
                sag_dirsek = keypoints[8]
                sag_bilek = keypoints[10]

                # Eklemlerin hepsi ekrandaysa
                if sag_omuz[1] != 0 and sag_dirsek[1] != 0 and sag_bilek[1] != 0:
                    
                    # Açıyı hesapla
                    aci = calculate_angle(sag_omuz, sag_dirsek, sag_bilek)
                    
                    # Dirsek noktasına açıyı yaz
                    cv2.putText(annotated_frame, str(int(aci)), tuple(map(int, sag_dirsek)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    # Sayac Mantigi (Bicep Curl)
                    if aci > 130: # Kol düz/aşağıda
                        hareket_yonu = 0
                        form_mesaji = "YUKARI CEK!"
                    if aci < 40 and hareket_yonu == 0: # Kol tam büküldü
                        hareket_yonu = 1
                        tekrar_sayisi += 1
                        form_mesaji = "GUZEL! ASAGI SAL"
                        
        # HUD Arayüzü (Ekrana Yazdırma)
        cv2.rectangle(annotated_frame, (0, 0), (350, 120), (0, 0, 0), -1) # Arka plan kutusu
        cv2.putText(annotated_frame, f"TEKRAR (REP): {tekrar_sayisi}", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.putText(annotated_frame, form_mesaji, (10, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("AI Fitness Trainer", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27: # ESC ile çıkış
        break

cap.release()
cv2.destroyAllWindows()