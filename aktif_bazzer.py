import RPi.GPIO as GPIO
import time

BUZZER_PIN = 17  # Gunakan GPIO17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Nyalakan buzzer selama 1 detik
GPIO.output(BUZZER_PIN, GPIO.HIGH)
time.sleep(1)
GPIO.output(BUZZER_PIN, GPIO.LOW)

GPIO.cleanup()
