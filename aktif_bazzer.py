import RPi.GPIO as GPIO
import time

BUZZER_PIN = 18  # GPIO18 = Pin 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

print("Buzzer ON")
GPIO.output(BUZZER_PIN, GPIO.HIGH)
time.sleep(1)

print("Buzzer OFF")
GPIO.output(BUZZER_PIN, GPIO.LOW)

GPIO.cleanup()
