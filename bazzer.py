import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

PIR_PIN = 13        # Pin PIR (fisik 13)
BUZZER_PIN = 12     # Buzzer (fisik 12 = GPIO18)

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

print("Menunggu gerakan dari PIR sensor...")

try:
    while True:
        motion = GPIO.input(PIR_PIN)
        if motion:
            print("Gerakan terdeteksi! 🔔")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(1)
        else:
            print("Tidak ada gerakan.")
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.5)

except KeyboardInterrupt:
    print("Dihentikan.")
    GPIO.cleanup()
