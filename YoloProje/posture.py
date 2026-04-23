import cv2
from ultralytics import YOLO

model = YOLO('yolov8n-pose.pt') 
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)

    for result in results:
        annotated_frame = result.plot()
        
        if result.keypoints is not None and len(result.keypoints) > 0:
            keypoints = result.keypoints.xy[0] 
            
            if len(keypoints) > 10:
                left_ear_x = int(keypoints[3][0])
                left_ear_y = int(keypoints[3][1])
                left_shoulder_x = int(keypoints[5][0])
                left_shoulder_y = int(keypoints[5][1])

                if left_ear_y != 0 and left_shoulder_y != 0:
                    
                    dikey_mesafe = left_shoulder_y - left_ear_y
                    yatay_mesafe = abs(left_ear_x - left_shoulder_x)
                    
                    cv2.putText(annotated_frame, f"Dikey (Boyun): {dikey_mesafe} px", (30, 40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                    cv2.putText(annotated_frame, f"Yatay (Kambur): {yatay_mesafe} px", (30, 80), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

                    # --- SENİN İÇİN BELİRLEDİĞİMİZ KALİBRE DEĞERLERİ ---
                    boyun_hatali = dikey_mesafe < 230  # 285'ten 240'a düşerse uyar
                    sirt_hatali = yatay_mesafe > 135   # 95'ten 140'a çıkarsa uyar
                    
                    y_koordinati = 130 # Yazıları ekrana basmaya başlayacağımız yükseklik
                    
                    if boyun_hatali or sirt_hatali:
                        if boyun_hatali:
                            cv2.putText(annotated_frame, "UYARI: BOYNUN DUSTU, KAFANI KALDIR!", (30, y_koordinati), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                            y_koordinati += 40 # İkinci hata varsa yazılar üst üste binmesin diye aşağı kaydırıyoruz
                            
                        if sirt_hatali:
                            cv2.putText(annotated_frame, "UYARI: KAMBURLASTIN, SIRTINI YASLA!", (30, y_koordinati), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                    else:
                        cv2.putText(annotated_frame, "DURUS NORMAL", (30, y_koordinati), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Posture Analizi v3", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()