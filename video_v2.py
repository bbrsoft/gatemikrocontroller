import cv2
import datetime

# Buka kamera (biasanya 0 = default camera)
cap = cv2.VideoCapture(0)

# Atur resolusi
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Codec & output file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video_with_overlay.avi', fourcc, 20.0, (640, 480))

start_time = datetime.datetime.now()

print("Recording...")

while (datetime.datetime.now() - start_time).seconds < 10:
    ret, frame = cap.read()
    if not ret:
        break

    # Gambar kotak di tengah layar
    h, w, _ = frame.shape
    x1, y1 = w//2 - 100, h//2 - 100
    x2, y2 = w//2 + 100, h//2 + 100
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Kotak merah

    # Tampilkan tulisan "Deteksi"
    cv2.putText(frame, "Deteksi", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255, 255, 255), 2)

    # Simpan ke file
    out.write(frame)

    # Tampilkan preview (optional)
    cv2.imshow('Preview', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Selesai merekam.")
cap.release()
out.release()
cv2.destroyAllWindows()
