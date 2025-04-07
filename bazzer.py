import RPi.GPIO as GPIO
import time

# Gunakan penomoran BOARD (fisik pin)
GPIO.setmode(GPIO.BOARD)

# Pin setup
PIR_PIN = 13        # Pin fisik 13 (GPIO27 untuk PIR OUT)
BUZZER_PIN = 12     # Pin fisik 12 (GPIO18 untuk kontrol buzzer IO)

# Setup GPIO
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

print("Menunggu gerakan dari PIR sensor...")

try:
    while True:
        if GPIO.input(PIR_PIN):  # Jika gerakan terdeteksi
            print("Gerakan terdeteksi! 🔔 Buzzer bunyi...")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(1)  # Buzzer bunyi selama 1 detik
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(1)
        else:
            print("Tidak ada gerakan.")
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.5)

except KeyboardInterrupt:
    print("\nProgram dihentikan oleh user.")
    GPIO.cleanup()
