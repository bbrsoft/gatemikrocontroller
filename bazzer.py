import RPi.GPIO as GPIO
import time
import requests


# ====== SETUP BOT TELEGRAM ======
TOKEN = '7401509957:AAHcQs86n2go2A9sB-soTEbtlPPaQkGwiOE'          # Ganti dengan token bot kamu
CHAT_ID = '5834504059'          # Ganti dengan chat ID kamu

# ====== SETUP PIR DAN BUZZER ======
GPIO.setmode(GPIO.BOARD)
PIR_PIN = 13
BUZZER_PIN = 12

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

print("Menunggu gerakan dari PIR sensor...")

# Fungsi kirim pesan ke Telegram
def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': pesan
    }
    try:
        requests.post(url, data=payload)
        print("Pesan dikirim ke Telegram.")
    except Exception as e:
        print("Gagal mengirim pesan:", e)

try:
    while True:
        motion = GPIO.input(PIR_PIN)
        if motion:
            print("Gerakan terdeteksi! 🔔")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            kirim_telegram("🚨 Gerakan terdeteksi di lokasi!")
            time.sleep(1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(1)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.2)

except KeyboardInterrupt:
    print("Program dihentikan.")
    GPIO.cleanup()
