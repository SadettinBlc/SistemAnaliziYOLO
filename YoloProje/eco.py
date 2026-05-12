import cv2
from ultralytics import YOLO
import time

model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)

cv2.namedWindow("AI Eco-Manager", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AI Eco-Manager", cv2.WND_PROP_TOPMOST, 1)

son_insan_zamani = time.time()
bekleme_limiti = 5.0 # 5 saniye kimse yoksa uykuya geç

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    insan_var = False

    for result in results:
        # Eğer sistem bir iskelet veya anahtar nokta görüyorsa insan vardır
        if result.keypoints is not None and len(result.keypoints) > 0:
            if len(result.keypoints.xy[0]) > 5: 
                insan_var = True
                break

    su_an = time.time()

    if insan_var:
        son_insan_zamani = su_an
        annotated_frame = results[0].plot() 
        cv2.rectangle(annotated_frame, (0, 0), (640, 50), (0, 255, 0), -1)
        cv2.putText(annotated_frame, "PERSONEL TESPIT EDILDI - ISIKLAR ACIK", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    else:
        annotated_frame = frame.copy() 
        gecen_sure = su_an - son_insan_zamani
        
        # Odanın boş olduğu anlaşıldıysa ve 5 saniye geçtiyse ekranı karart (Tasarruf Modu)
        if gecen_sure > bekleme_limiti:
            karanlik = cv2.rectangle(annotated_frame.copy(), (0, 0), (annotated_frame.shape[1], annotated_frame.shape[0]), (0, 0, 0), -1)
            # Görüntüyü %70 oranında sanal olarak karartıyoruz
            annotated_frame = cv2.addWeighted(annotated_frame, 0.3, karanlik, 0.7, 0) 
            
            cv2.putText(annotated_frame, "ENERJI TASARRUF MODU AKTIF", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            cv2.putText(annotated_frame, "Sistem Otonom Olarak Beklemeye Alindi...", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(annotated_frame, "Uyanmak icin kadraja giriniz.", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        # Biri odadan çıktı, 5'ten geriye sayıyor
        else:
            cv2.rectangle(annotated_frame, (0, 0), (640, 50), (0, 165, 255), -1) 
            kalan_sure = int(bekleme_limiti - gecen_sure)
            cv2.putText(annotated_frame, f"ODADA KIMSE YOK! KAPANMAYA SON: {kalan_sure} sn", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.imshow("AI Eco-Manager", annotated_frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()