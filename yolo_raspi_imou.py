from ultralytics import YOLO
import cv2
import pygame
import time
import requests
import os

# ===== TELEGRAM SETUP =====
TELEGRAM_BOT_TOKEN = "8015834378:AAFLaVw2i4fiO1HClJN17z-mZRJkfq75Zdk"
TELEGRAM_CHAT_ID = "7081662147"

def kirim_telegram_video(path_video):
    """Fungsi untuk kirim video ke Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    with open(path_video, 'rb') as f:
        files = {'video': f}
        data = {'chat_id': TELEGRAM_CHAT_ID}
        try:
            response = requests.post(url, files=files, data=data)
            if response.ok:
                print("📤 Video berhasil dikirim ke Telegram.")
            else:
                print("❌ Gagal mengirim video:", response.text)
        except Exception as e:
            print("❌ Error kirim video:", e)

def kirim_telegram_foto(path_foto):
    """Fungsi untuk kirim foto ke Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(path_foto, 'rb') as f:
        files = {'photo': f}
        data = {'chat_id': TELEGRAM_CHAT_ID}
        try:
            response = requests.post(url, files=files, data=data)
            if response.ok:
                print("📸 Foto berhasil dikirim ke Telegram.")
            else:
                print("❌ Gagal mengirim foto:", response.text)
        except Exception as e:
            print("❌ Error kirim foto:", e)


# Load Model YOLO
model = YOLO("yolov8n.pt")

# Buka Kamera
cap = cv2.VideoCapture("rtsp://admin:L255EE02@192.168.0.108:554/cam/realmonitor?channel=1&subtype=0")

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

# Nama file video yang akan direkam
video_filename = "deteksi_video.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame_height, frame_width = frame.shape[:2]  # balik karena (height, width)
out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))


# Flag untuk mulai rekaman
start_time = None
recording = False
person_in_warning_zone = False  # Flag khusus untuk person

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
                if label == "person" and x1 < box_x2 and x2 > box_x1 and y1 < box_y2 and y2 > box_y1:
                    person_in_warning_zone = True

    # Gambar kotak merah di tengah layar
    cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (0, 0, 255), 2)

    if person_in_warning_zone:
        cv2.putText(frame, "WARNING!", (frame_width // 3, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        if not recording:
            print("🚨 PERSON terdeteksi di area peringatan! Mulai merekam dan kirim foto...")
            recording = True
            start_time = time.time()
            pygame.mixer.music.play(-1)  # Suara alarm

            warning_image_path = "warning_capture.jpg"
            cv2.imwrite(warning_image_path, frame)

            kirim_telegram_foto(warning_image_path, caption="🚨 Deteksi orang masuk area larangan!")


    # Jika ada objek yang masuk ke dalam kotak, tampilkan peringatan dan mainkan suara
    if warning:
        cv2.putText(frame, "WARNING!", (frame_width // 3, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        if not recording:
            print("🚨 Objek terdeteksi di area peringatan! Mulai merekam dan kirim foto...")
            recording = True
            start_time = time.time()
            pygame.mixer.music.play(-1)  # Putar suara terus-menerus
    
            # Simpan frame sebagai gambar
            warning_image_path = "warning_capture.jpg"
            cv2.imwrite(warning_image_path, frame)
    
            # Kirim foto ke Telegram
            kirim_telegram_foto(warning_image_path)


    if recording:
        out.write(frame)  # Rekam frame ke file video
        if time.time() - start_time >= 50:  # Rekam selama 5 detik
            print("⏱️ Rekaman selesai 10 detik.")
            break

    cv2.imshow("Cam Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup dan kirim video ke Telegram
cap.release()
out.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()

if recording:
    kirim_telegram_video(video_filename)  # Kirim video ke Telegram
    #os.remove(video_filename)  # Hapus video setelah dikirim
    time.sleep(50)
pygame.mixer.quit()
