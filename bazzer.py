import RPi.GPIO as GPIO
import time
import requests
import os

# ====== SETUP BOT TELEGRAM ======
TOKEN = '7401509957:AAHcQs86n2go2A9sB-soTEbtlPPaQkGwiOE'   # Ganti dengan token kamu
CHAT_ID = '5834504059'                                    # Ganti dengan chat ID kamu

# ====== SETUP PIR DAN BUZZER ======
GPIO.setmode(GPIO.BOARD)
PIR_PIN = 13
BUZZER_PIN = 12

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

print("Menunggu gerakan dari PIR sensor...")

# Fungsi untuk kirim pesan teks ke Telegram
def kirim_telegram_pesan(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': pesan
    }
    try:
        requests.post(url, data=data)
        print("✅ Pesan teks terkirim ke Telegram.")
    except Exception as e:
        print("❌ Gagal mengirim pesan:", e)

# Fungsi untuk kirim foto ke Telegram
def kirim_telegram_foto(path_foto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    files = {'photo': open(path_foto, 'rb')}
    data = {'chat_id': CHAT_ID}
    try:
        requests.post(url, files=files, data=data)
        print("📷 Gambar berhasil dikirim ke Telegram.")
    except Exception as e:
        print("❌ Gagal mengirim gambar:", e)

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("🚨 Gerakan terdeteksi!")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)

            # Ambil gambar dari kamera
            filename = "deteksi.jpg"
            os.system(f"libcamera-still -t 1000 -o {filename}")

            # Kirim ke Telegram
            kirim_telegram_pesan("🚨 Gerakan terdeteksi! Mengirim foto...")
            kirim_telegram_foto(filename)

            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(5)  # Tunggu sebelum deteksi lagi
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.5)

except KeyboardInterrupt:
    print("Program dihentikan oleh user.")
    GPIO.cleanup()
