import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)

cv2.namedWindow("Air Canvas", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Air Canvas", cv2.WND_PROP_TOPMOST, 1)

# Boş bir çizim tuvali (Siyah ekran) oluştur
ret, frame = cap.read()
canvas = np.zeros_like(frame)

eski_x, eski_y = 0, 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Çizim yaparken kafamız karışmasın diye görüntüyü ayna yapıyoruz
    frame = cv2.flip(frame, 1)
    results = model(frame, verbose=False)

    for result in results:
        annotated_frame = result.plot()
        
        if result.keypoints is not None and len(result.keypoints) > 0:
            keypoints = result.keypoints.xy[0]
            
            if len(keypoints) > 10:
                l_sho = keypoints[5]  # Sol Omuz
                l_wri = keypoints[9]  # Sol Bilek
                r_wri = keypoints[10] # Sağ Bilek

                if r_wri[1] != 0 and l_wri[1] != 0:
                    rx, ry = int(r_wri[0]), int(r_wri[1])
                    
                    # TEMİZLEME KOMUTU: Sol el sol omuzun üzerine çıkarsa
                    if l_wri[1] < l_sho[1]:
                        canvas = np.zeros_like(frame)
                        cv2.putText(annotated_frame, "TAHTA SILINDI!", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
                        eski_x, eski_y = 0, 0
                    
                    # ÇİZİM KOMUTU: Sağ bilek ile kesintisiz çizim
                    else:
                        if eski_x == 0 and eski_y == 0:
                            eski_x, eski_y = rx, ry
                        
                        # Önceki nokta ile yeni nokta arasına çizgi çek
                        cv2.line(canvas, (eski_x, eski_y), (rx, ry), (0, 255, 255), 8)
                        eski_x, eski_y = rx, ry
                else:
                    eski_x, eski_y = 0, 0
            else:
                eski_x, eski_y = 0, 0

    # Çizilen renkli tuvali, orijinal kamera görüntüsüyle kusursuzca birleştirme
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    
    arka_plan = cv2.bitwise_and(annotated_frame, annotated_frame, mask=mask_inv)
    on_plan = cv2.bitwise_and(canvas, canvas, mask=mask)
    son_goruntu = cv2.add(arka_plan, on_plan)

    # HUD
    cv2.putText(son_goruntu, "Sag Bilek: Cizim Yap | Sol El Havada: Tahtayi Sil", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    cv2.imshow("Air Canvas", son_goruntu)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()