from picamera2 import Picamera2
import time

picam2 = Picamera2()

# Konfigurasi video
config = picam2.create_video_configuration()
picam2.configure(config)

# Start dan rekam
picam2.start_recording("video_night.h264")
print("Recording 10 seconds...")
time.sleep(10)
picam2.stop_recording()
print("Recording selesai.")
