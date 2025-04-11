import cv2
import pygame
import time
import requests

# Telegram
TELEGRAM_BOT_TOKEN = "7401509957:AAHcQs86n2go2A9sB-soTEbtlPPaQkGwiOE"
TELEGRAM_CHAT_ID = "5834504059"

def send_image_to_telegram(image_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as image_file:
        files = {"photo": image_file}
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": "Deteksi objek!"}
        return requests.post(url, data=data, files=files)

# Load label COCO
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Load YOLOv4-tiny model
net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

# Inisialisasi suara
pygame.mixer.init()
pygame.mixer.music.load("warning.mp3")

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

_, frame = cap.read()
frame_height, frame_width, _ = frame.shape

# Kotak Deteksi Tengah
box_w, box_h = frame_width // 3, frame_height // 3
box_x1 = (frame_width - box_w) // 2
box_y1 = (frame_height - box_h) // 2
box_x2 = box_x1 + box_w
box_y2 = box_y1 + box_h

last_sent_time = 0
sound_playing = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Buat blob dari frame
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416,416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    layer_names = net.getUnconnectedOutLayersNames()
    outputs = net.forward(layer_names)

    warning = False

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = int(scores.argmax())
            confidence = scores[class_id]
            if confidence > 0.5:
                label = classes[class_id]
                if label in ["person", "dog", "cat", "car", "motorbike"]:
                    center_x, center_y = int(detection[0]*frame_width), int(detection[1]*frame_height)
                    w, h = int(detection[2]*frame_width), int(detection[3]*frame_height)
                    x, y = int(center_x - w/2), int(center_y - h/2)

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

                    if x < box_x2 and x+w > box_x1 and y < box_y2 and y+h > box_y1:
                        warning = True

    # Gambar kotak tengah
    cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (0, 0, 255), 2)

    if warning:
        cv2.putText(frame, "DETEKSI!", (frame_width//3, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        if not sound_playing:
            pygame.mixer.music.play(-1)
            sound_playing = True

        current_time = time.time()
        if current_time - last_sent_time >= 15:
            image_path = "capture.jpg"
            cv2.imwrite(image_path, frame)
            response = send_image_to_telegram(image_path)
            if response.status_code == 200:
                print("Terkirim ke Telegram.")
            else:
                print("Gagal kirim:", response.status_code)
            last_sent_time = current_time

    else:
        if sound_playing:
            pygame.mixer.music.stop()
            sound_playing = False

    cv2.imshow("Deteksi Kamera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
