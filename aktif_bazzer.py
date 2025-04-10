import RPi.GPIO as GPIO
 
buzzer = 18
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
GPIO.setup(buzzer, GPIO.OUT)
 
GPIO.output(buzzer, GPIO.HIGH)
