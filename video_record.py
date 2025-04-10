import subprocess

print("Mulai rekam selama 10 detik...")

subprocess.run([
    "libcamera-vid",
    "-t", "10000",              # durasi 10 detik
    "-o", "video_debian.h264"   # nama file output
])

print("Rekaman selesai!")
