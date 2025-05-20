from gpiozero import MotionSensor
from signal import pause

pir = MotionSensor(13)

pir.when_motion = lambda: print("Gerakan Terdeteksi!")
pir.when_no_motion = lambda: print("Tidak ada gerakan.")

pause()
