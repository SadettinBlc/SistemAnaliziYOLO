import cv2
from ultralytics import YOLO
import pyautogui
import time

model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)

cv2.namedWindow("AI Media Controller", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AI Media Controller", cv2.WND_PROP_TOPMOST, 1)

son_islem_zamani = time.time()
bekleme_suresi = 1.0 
durum_mesaji = "HAZIR (Hareket Bekleniyor)"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Ayna görüntüsü 
    frame = cv2.flip(frame, 1)
    
    results = model(frame, verbose=False)

    for result in results:
        annotated_frame = result.plot()
        
        if result.keypoints is not None and len(result.keypoints) > 0:
            keypoints = result.keypoints.xy[0]
            
            if len(keypoints) > 10:
                l_sho = keypoints[5]
                r_sho = keypoints[6]
                l_wri = keypoints[9]
                r_wri = keypoints[10]
                nose = keypoints[0]

                if l_sho[1] != 0 and r_sho[1] != 0 and r_wri[1] != 0 and l_wri[1] != 0:
                    su_an = time.time()
                    
                    # 1. PLAY / PAUSE: İki el de omuz hizasının üzerindeyse (Teslim olma hareketi)
                    if l_wri[1] < l_sho[1] and r_wri[1] < r_sho[1]:
                        if su_an - son_islem_zamani > bekleme_suresi:
                            pyautogui.press('playpause')
                            durum_mesaji = "PLAY / PAUSE"
                            son_islem_zamani = su_an
                            
                    # 2. SAĞ EL HAVADA (Ses Açma veya Sonraki Şarkı)
                    elif r_wri[1] < r_sho[1] and l_wri[1] > l_sho[1]: 
                        merkez_x = (l_sho[0] + r_sho[0]) / 2
                        dx = r_wri[0] - merkez_x
                        
                        # Sağ el kafanın üstüne çıkmışsa (Ses Aç)
                        if r_wri[1] < nose[1]:
                            pyautogui.press('volumeup')
                            durum_mesaji = "SES YUKSELTILIYOR"
                            time.sleep(0.05) # Sesi pürüzsüz açmak için ufak gecikme
                            
                        # Sağ el sağa doğru çok uzaklaşmışsa (Sonraki Şarkı)
                        elif dx > 150: 
                            if su_an - son_islem_zamani > bekleme_suresi:
                                pyautogui.press('nexttrack')
                                durum_mesaji = "-> SONRAKI SARKI"
                                son_islem_zamani = su_an
                                
                    # 3. SOL EL HAVADA (Ses Kısma veya Önceki Şarkı)
                    elif l_wri[1] < l_sho[1] and r_wri[1] > r_sho[1]:
                        merkez_x = (l_sho[0] + r_sho[0]) / 2
                        dx = merkez_x - l_wri[0]
                        
                        # Sol el kafanın üstüne çıkmışsa (Ses Kıs)
                        if l_wri[1] < nose[1]:
                            pyautogui.press('volumedown')
                            durum_mesaji = "SES KISILIYOR"
                            time.sleep(0.05)
                            
                        # Sol el sola doğru çok uzaklaşmışsa (Önceki Şarkı)
                        elif dx > 150:
                            if su_an - son_islem_zamani > bekleme_suresi:
                                pyautogui.press('prevtrack')
                                durum_mesaji = "<- ONCEKI SARKI"
                                son_islem_zamani = su_an
                    else:
                        durum_mesaji = "HAZIR (Hareket Bekleniyor)"

        # HUD Arayüzü
        cv2.rectangle(annotated_frame, (0, 0), (600, 60), (0, 0, 0), -1)
        cv2.putText(annotated_frame, durum_mesaji, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("AI Media Controller", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()