from ultralytics import YOLO
import cv2
import pygame
import time
import requests
import numpy as np

# Tentukan radius segienam


# Konfigurasi Telegram Bot
TELEGRAM_BOT_TOKEN = "7401509957:AAHcQs86n2go2A9sB-soTEbtlPPaQkGwiOE"  # Ganti dengan token bot Telegram kamu
TELEGRAM_CHAT_ID = "5834504059"      # Ganti dengan chat ID tujuan

def send_image_to_telegram(image_path):
    """
    Fungsi untuk mengirim file gambar ke Telegram.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as image_file:
        files = {"photo": image_file}
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": "Deteksi objek!"}
        response = requests.post(url, data=data, files=files)
    return response

# Inisialisasi model YOLO
model = YOLO("yolov8n.pt")

# Buka kamera
cap = cv2.VideoCapture(0)

# Set resolusi (sesuai kebutuhan, disesuaikan untuk perangkat seperti Raspberry Pi)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 340)

# Inisialisasi suara peringatan
pygame.mixer.init()
warning_sound = "warning.mp3"  # Pastikan file ini ada di direktori yang sama
pygame.mixer.music.load(warning_sound)

# Ambil frame pertama untuk menentukan posisi dan ukuran kotak tengah
ret, frame = cap.read()
if not ret:
    print("Tidak dapat membaca dari kamera.")
    exit(1)

frame_height, frame_width, _ = frame.shape

# Definisikan ukuran dan posisi kotak peringatan di tengah layar
box_width = frame_width // 3
box_height = frame_height // 3
center_x = frame_width // 2
center_y = frame_height // 2
box_x1 = center_x - (box_width // 2)
box_y1 = center_y - (box_height // 2)
box_x2 = center_x + (box_width // 2)
box_y2 = center_y + (box_height // 2)

sound_playing = False  # Flag apakah suara sudah dimainkan
last_sent_time = 0   # Inisialisasi waktu pengiriman terakhir (dalam detik)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Lakukan deteksi menggunakan YOLO
    results = model(frame)  
    warning = False  # Flag untuk mendeteksi objek dalam area kotak

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Dapatkan koordinat kotak deteksi
            label = model.names[int(box.cls[0])]
            
            # Cek label apakah yang terdeteksi adalah "person", "dog", "cat", atau "properti"
            if label in ["person", "dog", "cat", "properti"]:  
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Jika objek terdeteksi berada di dalam kotak merah (area peringatan)
                if x1 < box_x2 and x2 > box_x1 and y1 < box_y2 and y2 > box_y1:
                    warning = True  

    # Gambar kotak peringatan di tengah layar
    # Gambar segienam custom
    radius = min(box_width, box_height) // 2
    custom_points = [(100,100), (150,90), (200,110), (180,150), (120,160), (90,130)]
    pts = np.array([custom_points], np.int32)
    cv2.polylines(frame, pts, isClosed=True, color=(0, 0, 255), thickness=2)




    # Jika ada deteksi dalam area kotak, tampilkan peringatan dan mainkan suara
    if warning:
        cv2.putText(frame, "DETEKSI!", (frame_width//3, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        if not sound_playing:
            pygame.mixer.music.play(-1)  # Putar suara terus-menerus
            sound_playing = True

        # Kirim gambar ke Telegram jika satu menit telah berlalu dari pengiriman sebelumnya
        current_time = time.time()
        if current_time - last_sent_time >= 15:
            image_path = "capture.jpg"
            cv2.imwrite(image_path, frame)
            response = send_image_to_telegram(image_path)
            if response.status_code == 200:
                print("Gambar berhasil dikirim ke Telegram.")
            else:
                print("Gagal mengirim gambar ke Telegram. Status Code:", response.status_code)
            last_sent_time = current_time

    else:
        if sound_playing:
            pygame.mixer.music.stop()  # Hentikan pemutaran suara
            sound_playing = False

    cv2.imshow("Cam Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan resources
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
