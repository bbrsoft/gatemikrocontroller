import cv2

cap = cv2.VideoCapture("rtsp://admin:L255EE02@192.168.0.108:554/cam/realmonitor?channel=1&subtype=0")

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Imou Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
