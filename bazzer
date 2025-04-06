import RPi.GPIO as GPIO
import time

# Atur mode penomoran pin
GPIO.setmode(GPIO.BOARD)

# Pin PIR dan Buzzer
PIR_PIN = 13     # OUT dari PIR
BUZZER_PIN = 12  # IO dari buzzer

# Setup pin
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

print("Menunggu gerakan...")

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Gerakan terdeteksi! 🔔")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(1)  # Buzzer bunyi 1 detik
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(1)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\nSelesai.")
    GPIO.cleanup()
