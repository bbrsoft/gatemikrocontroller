import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Kamera ditemukan di ID {i}")
        cap.release()
    else:
        print(f"TIDAK ditemukan kamera di ID {i}")
