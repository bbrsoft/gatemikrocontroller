import cv2

# Buka kamera
cap = cv2.VideoCapture(0)

# Atur resolusi
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Menampilkan video live. Tekan 'q' untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Ukuran frame
    h, w, _ = frame.shape
    x1, y1 = w // 2 - 100, h // 2 - 100
    x2, y2 = w // 2 + 100, h // 2 + 100

    # Gambar kotak merah
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Tampilkan tulisan "Deteksi"
    cv2.putText(frame, "Deteksi", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Tampilkan di jendela
    cv2.imshow("Live Camera", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
