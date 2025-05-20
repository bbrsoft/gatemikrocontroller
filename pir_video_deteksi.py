from gpiozero import MotionSensor, Buzzer
import time
import requests
import subprocess

# ====== SETUP BOT TELEGRAM ======
TELEGRAM_BOT_TOKEN = "8015834378:AAFLaVw2i4fiO1HClJN17z-mZRJkfq75Zdk"
TELEGRAM_CHAT_ID = "7081662147"

# ====== SETUP PIR SENSOR ======
pir = MotionSensor(13)  # GPIO 13 = BOARD pin 33
buzzer = Buzzer(18)  
print("📡 Menunggu gerakan dari PIR sensor...")

# Fungsi kirim pesan ke Telegram
def kirim_telegram_pesan(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': pesan}
    try:
        requests.post(url, data=data)
        print("✅ Pesan terkirim ke Telegram.")
    except Exception as e:
        print("❌ Gagal kirim pesan:", e)

# Fungsi cek apakah yolo_raspi_imou.py sudah berjalan
def is_yolo_running():
    result = subprocess.run(["pgrep", "-f", "yolo_raspi_imou.py"], stdout=subprocess.PIPE)
    return bool(result.stdout)

try:
    while True:
        pir.wait_for_motion()
        print("🚨 Gerakan terdeteksi!")
        # Aktifkan buzzer selama 2 detik
        buzzer.on()
        time.sleep(2)
        buzzer.off()
        
        kirim_telegram_pesan("🚨 Gerakan terdeteksi! Memulai deteksi kamera...")

        if not is_yolo_running():
            # Jalankan YOLO dari virtual environment
            subprocess.Popen(["/home/pi/gatemicro/env/bin/python", "/home/pi/gatemicro/yolo_raspi_imou.py"])
            print("▶️ YOLO dijalankan.")
        else:
            print("⏳ YOLO masih berjalan, tidak dijalankan ulang.")

        time.sleep(10)  # Jeda agar tidak spam deteksi
except KeyboardInterrupt:
    print("⛔ Program dihentikan oleh user.")
