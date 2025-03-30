from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO
import cv2
import pygame
import requests  # Untuk mengirim ke Telegram
import time  # Untuk mengontrol interval pengiriman
from ultralytics import YOLO

app = Flask(__name__)
socketio = SocketIO(app)  # Inisialisasi Flask-SocketIO

# Load Model YOLO
model = YOLO("yolov8n.pt")

# Konfigurasi awal
settings = {
    "detect_person": True,
    "detect_animal": False,
    "detect_property": False,
    "sound_enabled": True
}

# Konfigurasi Telegram
TELEGRAM_BOT_TOKEN = "7401509957:AAHcQs86n2go2A9sB-soTEbtlPPaQkGwiOE"  # Ganti dengan Token Bot Telegram
TELEGRAM_CHAT_ID = "5834504059"  # Ganti dengan ID Chat Telegram
last_sent_time = 0  # Waktu terakhir pengiriman (untuk mencegah spam)
SEND_INTERVAL = 10  # Kirim ke Telegram maksimal setiap 10 detik

pygame.mixer.init()
warning_sound = "warning.mp3"
pygame.mixer.music.load(warning_sound)

cap = cv2.VideoCapture(0)  # Buka kamera
sound_playing = False  # Flag untuk mengontrol suara


def send_telegram_photo(image):
    """Kirim gambar ke Telegram"""
    global last_sent_time

    if time.time() - last_sent_time < SEND_INTERVAL:
        return  # Jangan kirim terlalu sering

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    files = {"photo": ("warning.jpg", image, "image/jpeg")}
    data = {"chat_id": TELEGRAM_CHAT_ID, "caption": "⚠️ WARNING! Person detected in restricted area!"}

    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("📤 Foto dikirim ke Telegram!")
            last_sent_time = time.time()
        else:
            print("❌ Gagal mengirim foto:", response.text)
    except Exception as e:
        print("❌ Error mengirim foto:", str(e))


def generate_frames():
    global sound_playing

    while True:
        success, frame = cap.read()
        if not success:
            break

        h, w, _ = frame.shape  # Dapatkan ukuran frame

        # Tentukan area tengah sebagai zona peringatan
        center_x, center_y = w // 2, h // 2
        box_size = 200  # Ukuran kotak deteksi (bisa diubah)
        x1, y1 = center_x - box_size, center_y - box_size
        x2, y2 = center_x + box_size, center_y + box_size

        # Gambar kotak zona peringatan di tengah frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Kotak merah

        results = model(frame)
        warning = False

        for r in results:
            for box in r.boxes:
                bx1, by1, bx2, by2 = map(int, box.xyxy[0])  # Koordinat deteksi
                label = model.names[int(box.cls[0])]

                # Deteksi objek sesuai pengaturan
                if (label == "person" and settings["detect_person"]) or \
                   (label in ["dog", "cat"] and settings["detect_animal"]) or \
                   (label == "properti" and settings["detect_property"]):

                    cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (bx1, by1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Cek apakah objek ada dalam area tengah
                    if bx1 >= x1 and by1 >= y1 and bx2 <= x2 and by2 <= y2:
                        warning = True  # Jika ada di dalam area, aktifkan warning

        # Tampilkan teks "WARNING!" jika ada objek dalam area
        if warning:
            cv2.putText(frame, "WARNING! PERSON DETECTED!", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

        # Kirim status peringatan ke frontend
        socketio.emit('warning_status', {'warning': warning})

        # Kontrol suara
        if warning and settings["sound_enabled"]:
            if not sound_playing:
                pygame.mixer.music.play(-1)
                sound_playing = True
        else:
            if sound_playing:
                pygame.mixer.music.stop()
                sound_playing = False

        # Jika ada warning, kirim foto ke Telegram
        if warning:
            _, img_encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])  # Kompres gambar
            send_telegram_photo(img_encoded.tobytes())

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/update_settings', methods=['POST'])
def update_settings():
    data = request.json
    settings.update(data)
    return jsonify({"status": "success", "new_settings": settings})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
