import cv2

cap=cv2.VideoCapture('rtsp://admin:123456@192.168.43.120:8554/profile0')
print("Till Here")
while True:
    ret,frame=cap.read()
    print("frame read")
    cv2.imshow("Capturing",frame)
    print("Frame Printed")

    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
