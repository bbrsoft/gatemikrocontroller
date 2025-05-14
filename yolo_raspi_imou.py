from ultralytics import YOLO
import cv2
import pygame

# Load Model YOLO
model = YOLO("yolov8n.pt")

# Buka Kamera
cap = cv2.VideoCapture(1)
# cap = cv2.VideoCapture("rtsp://admin:L255EE02@192.168.0.108:554/cam/realmonitor?channel=1&subtype=0")

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

# Fungsi untuk menghitung jarak objek ke kamera
def calculate_distance(focal_length, real_height, image_height):
    """Menghitung jarak objek berdasarkan tinggi di gambar"""
    distance = (focal_length * real_height) / image_height
    return distance

# Fungsi untuk menghitung tinggi objek berdasarkan jarak
def calculate_real_height(focal_length, real_distance, image_height):
    """Menghitung tinggi objek berdasarkan jarak dan tinggi objek di gambar"""
    real_height = (image_height * real_distance) / focal_length
    return real_height

# Tentukan panjang fokal dan tinggi objek nyata
focal_length = 500  # Panjang fokal dalam piksel, sesuaikan dengan kamera
real_height = 170  # Tinggi objek nyata dalam cm (misalnya manusia)

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


            # Menghitung tinggi objek dalam gambar (dalam piksel)
            image_height = y2 - y1
            
            # Menghitung jarak objek ke kamera
            distance = calculate_distance(focal_length, real_height, image_height)
            
            # Menampilkan jarak objek pada frame
            cv2.putText(frame, f"Jarak: {distance:.2f} cm", (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            # Menghitung perkiraan tinggi objek berdasarkan jarak
            estimated_height = calculate_real_height(focal_length, distance, image_height)
            
            # Menampilkan perkiraan tinggi objek di dunia nyata
            cv2.putText(frame, f"Tinggi: {estimated_height:.2f} cm", (x1, y2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    # Gambar kotak merah di tengah layar
    cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (0, 0, 255), 2)

    # Jika ada objek yang masuk ke dalam kotak, tampilkan peringatan dan mainkan suara
    if warning:
        cv2.putText(frame, "WARNING!", (frame_width // 3, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        if not sound_playing:
            pygame.mixer.music.play(-1)  # Putar suara terus-menerus
            sound_playing = True
    else:
        if sound_playing:
            pygame.mixer.music.stop()  # Hentikan suara
            sound_playing = False

    cv2.imshow("Cam Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
