
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not accessible")
    exit()

print("Camera started! Press Q to exit.")

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to capture frame")
        break

    cv2.imshow("PyroTouch - Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Camera closed.")
