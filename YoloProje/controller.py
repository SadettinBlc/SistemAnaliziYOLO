import cv2
from ultralytics import YOLO
import pydirectinput
import time
import keyboard

model = YOLO('yolov8n-pose.pt') 
cap = cv2.VideoCapture(0)

cv2.namedWindow("Elden Ring Vucut Kontrolcusu", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Elden Ring Vucut Kontrolcusu", cv2.WND_PROP_TOPMOST, 1)

aktif_kafa_tus = None
sag_el_hazir = True
sol_el_hazir = True

pydirectinput.FAILSAFE = True
baslangic_zamani = time.time()
sistem_duraklatildi = False  # YENİ: Debriyaj değişkenimiz

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # ==========================================
    # GLOBAL TUŞ DİNLEYİCİ (F12)
    # ==========================================
    if keyboard.is_pressed('f12'):
        sistem_duraklatildi = not sistem_duraklatildi
        
        # Eğer sistem durdurulduysa ve karakter o an yürüyorsa, takılı kalmasın diye tuşu bırak
        if sistem_duraklatildi and aktif_kafa_tus is not None:
            pydirectinput.keyUp(aktif_kafa_tus)
            aktif_kafa_tus = None
            
        time.sleep(0.3) # Tuşa basılı tutma ihtimaline karşı ufak bir gecikme (Debounce)

    results = model(frame, verbose=False)

    for result in results:
        annotated_frame = result.plot()
        
        # Eğer sistem duraklatıldıysa ekrana kocaman uyarı bas ve hareketleri işleme
        if sistem_duraklatildi:
            cv2.rectangle(annotated_frame, (0, 0), (640, 100), (0, 0, 0), -1)
            cv2.putText(annotated_frame, "SISTEM BEKLEMEDE", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            cv2.putText(annotated_frame, "Devam etmek icin F12'ye bas", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
        # Sistem aktifse normal Elden Ring kodlarını çalıştır
        else:
            if result.keypoints is not None and len(result.keypoints) > 0:
                keypoints = result.keypoints.xy[0] 
                
                if len(keypoints) > 10: 
                    nose = keypoints[0]
                    l_shoulder = keypoints[5]
                    r_shoulder = keypoints[6]
                    l_wrist = keypoints[9]
                    r_wrist = keypoints[10] 

                    gecen_sure = time.time() - baslangic_zamani
                    sistem_aktif = gecen_sure >= 3
                    
                    sag_el_metin = "SAG EL: MERKEZ (Hazir)"
                    sol_el_metin = "SOL EL: MERKEZ (Hazir)"
                    yeni_kafa_tus = None

                    # 1. SAĞ EL (SALDIRI MOTORU)
                    if r_wrist[1] != 0 and r_shoulder[1] != 0:
                        rs_x, rs_y = int(r_shoulder[0]), int(r_shoulder[1])
                        rw_x, rw_y = int(r_wrist[0]), int(r_wrist[1])
                        cv2.circle(annotated_frame, (rs_x, rs_y), 90, (0, 0, 255), 2)
                        hx, hy = rw_x - rs_x, rw_y - rs_y
                        
                        if abs(hx) > 90 or abs(hy) > 90:
                            if sag_el_hazir:
                                if abs(hx) > abs(hy):
                                    if hx < 0: 
                                        if sistem_aktif: 
                                            pydirectinput.mouseDown(button='left')
                                            time.sleep(0.05) 
                                            pydirectinput.mouseUp(button='left')
                                        sag_el_metin = "SAG EL: HAFIF SALDIRI (Sol Tik) -> MERKEZE DON!"
                                    else: 
                                        if sistem_aktif: pydirectinput.press('g')
                                        sag_el_metin = "SAG EL: AGIR SALDIRI (G Tusu) -> MERKEZE DON!"
                                else:
                                    if hy < 0: 
                                        if sistem_aktif: 
                                            pydirectinput.mouseDown(button='right')
                                            time.sleep(0.05)
                                            pydirectinput.mouseUp(button='right')
                                        sag_el_metin = "SAG EL: SOL EL SILAHI (Sag Tik) -> MERKEZE DON!"
                                    else: 
                                        if sistem_aktif: pydirectinput.press('f')
                                        sag_el_metin = "SAG EL: ASHES OF WAR (F) -> MERKEZE DON!"
                                sag_el_hazir = False
                            else:
                                sag_el_metin = "SAG EL: KILITLI -> MERKEZE DON!"
                        else:
                            sag_el_hazir = True

                    # 2. SOL EL (DESTEK MOTORU)
                    if l_wrist[1] != 0 and l_shoulder[1] != 0:
                        ls_x, ls_y = int(l_shoulder[0]), int(l_shoulder[1])
                        lw_x, lw_y = int(l_wrist[0]), int(l_wrist[1])
                        cv2.circle(annotated_frame, (ls_x, ls_y), 90, (255, 0, 255), 2)
                        lx, ly = lw_x - ls_x, lw_y - ls_y
                        
                        if abs(lx) > 90 or abs(ly) > 90:
                            if sol_el_hazir:
                                if abs(lx) > abs(ly):
                                    if lx > 0: 
                                        if sistem_aktif: pydirectinput.press('r')
                                        sol_el_metin = "SOL EL: ESTUS (R) -> MERKEZE DON!"
                                    else: 
                                        if sistem_aktif: pydirectinput.press('q')
                                        sol_el_metin = "SOL EL: KILITLEN (Q) -> MERKEZE DON!"
                                else:
                                    if ly < 0: 
                                        if sistem_aktif: pydirectinput.press('space')
                                        sol_el_metin = "SOL EL: ZIPLA (Space) -> MERKEZE DON!"
                                    else: 
                                        if sistem_aktif: pydirectinput.press('shift')
                                        sol_el_metin = "SOL EL: TAKLA (Shift) -> MERKEZE DON!"
                                sol_el_hazir = False
                            else:
                                sol_el_metin = "SOL EL: KILITLI -> MERKEZE DON!"
                        else:
                            sol_el_hazir = True

                    # 3. KAFA (YÜRÜME JOYSTICK'İ)
                    kafa_metin = "KAFA: MERKEZ (Duruyor)"
                    if nose[1] != 0 and l_shoulder[1] != 0 and r_shoulder[1] != 0:
                        nx, ny = int(nose[0]), int(nose[1])
                        omuz_merkez_x = int((l_shoulder[0] + r_shoulder[0]) / 2)
                        omuz_merkez_y = int((l_shoulder[1] + r_shoulder[1]) / 2)
                        joy_merkez_x = omuz_merkez_x
                        joy_merkez_y = omuz_merkez_y - 180 
                        
                        cv2.circle(annotated_frame, (joy_merkez_x, joy_merkez_y), 70, (255, 0, 0), 2)
                        cv2.circle(annotated_frame, (nx, ny), 5, (0, 255, 255), -1)

                        dx = nx - joy_merkez_x
                        dy = ny - joy_merkez_y
                        
                        if abs(dx) > 70 or abs(dy) > 70:
                            if abs(dy) > abs(dx):
                                if dy < 0: 
                                    yeni_kafa_tus = 'w'
                                    kafa_metin = "KAFA: ILERI (W)"
                                else: 
                                    yeni_kafa_tus = 's'
                                    kafa_metin = "KAFA: GERI (S)"
                            else:
                                if dx < 0: 
                                    yeni_kafa_tus = 'd'
                                    kafa_metin = "KAFA: SAG (D)"
                                else: 
                                    yeni_kafa_tus = 'a'
                                    kafa_metin = "KAFA: SOL (A)"

                    if sistem_aktif:
                        if yeni_kafa_tus != aktif_kafa_tus:
                            if aktif_kafa_tus is not None:
                                pydirectinput.keyUp(aktif_kafa_tus)
                            if yeni_kafa_tus is not None:
                                pydirectinput.keyDown(yeni_kafa_tus)
                            aktif_kafa_tus = yeni_kafa_tus

                    # HUD ARAYÜZÜ
                    cv2.putText(annotated_frame, kafa_metin, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    cv2.putText(annotated_frame, sag_el_metin, (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(annotated_frame, sol_el_metin, (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

                    if not sistem_aktif:
                        cv2.putText(annotated_frame, f"SISTEM AKTIFLESIYOR: {3 - int(gecen_sure)}", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5)
                    else:
                        cv2.putText(annotated_frame, "SISTEM AKTIF", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Elden Ring Vucut Kontrolcusu", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

if aktif_kafa_tus is not None:
    pydirectinput.keyUp(aktif_kafa_tus)
cap.release()
cv2.destroyAllWindows()