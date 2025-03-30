from ultralytics import YOLO
import cv2
import pygame

# Load Model YOLO
model = YOLO("yolov8n.pt")

# Buka Kamera
cap = cv2.VideoCapture(0)

# Inisialisasi suara
pygame.mixer.init()
warning_sound = "warning.mp3"  # Ganti dengan file suara Anda
pygame.mixer.music.load(warning_sound)

# Ambil dimensi frame pertama untuk menentukan kotak tengah
ret, frame = cap.read()
frame_height, frame_width, _ = frame.shape

# Ukuran dan posisi kotak merah di tengah layar
box_width = frame_width // 3
box_height = frame_height // 3
center_x = frame_width // 2
center_y = frame_height // 2
box_x1 = center_x - (box_width // 2)
box_y1 = center_y - (box_height // 2)
box_x2 = center_x + (box_width // 2)
box_y2 = center_y + (box_height // 2)

sound_playing = False  # Flag untuk mengecek apakah suara sedang dimainkan

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model(frame)  
    warning = False  # Flag jika ada objek masuk ke dalam kotak

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Koordinat kotak deteksi
            label = model.names[int(box.cls[0])]
            
            # Jika objek adalah manusia atau hewan
            if label in ["person", "dog", "cat", "properti"]:  
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Jika objek masuk ke dalam kotak merah
                if x1 < box_x2 and x2 > box_x1 and y1 < box_y2 and y2 > box_y1:
                    warning = True  

    # Gambar kotak merah di tengah layar
    cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (0, 0, 255), 2)

    # Jika ada objek yang masuk ke dalam kotak, tampilkan peringatan dan mainkan suara
    if warning:
        cv2.putText(frame, "WARNING!", (frame_width//3, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        if not sound_playing:
            pygame.mixer.music.play(-1)  # Putar suara terus-menerus
            sound_playing = True
    else:
        if sound_playing:
            pygame.mixer.music.stop()  # Hentikan suara
            sound_playing = False

    cv2.imshow("CAm Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
