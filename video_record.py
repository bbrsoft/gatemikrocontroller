import subprocess

print("Mulai rekam selama 10 detik...")

subprocess.run([
    "libcamera-vid",
    "-t", "10000",                     # durasi 10 detik
    "--framerate", "15",              # fps lebih rendah = lebih terang di gelap
    "--brightness", "0.5",            # nilai antara -1.0 ke 1.0
    "--contrast", "1.0",              # tingkatkan kontras
    "--gain", "8",                    # tingkatkan gain (untuk cahaya rendah)
    "--sharpness", "1.5",             # bantu lebih tajam
    "--awb", "off",                   # matikan auto white balance
    "--awbgains", "2.0,2.0",          # buat lebih terang
    "-o", "video_nightmode.h264"
])

# subprocess.run([
#     "libcamera-vid",
#     "-t", "10000",              # durasi 10 detik
#     "-o", "video_debian.h264"   # nama file output
# ])

print("Rekaman selesai!")
