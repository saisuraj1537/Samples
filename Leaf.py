import cv2
from ultralytics import YOLO

# Load the trained YOLO model
model = YOLO('/home/dronepi/detect/best.pt')

# Define leaf-related classes
leaf_classes = ["Rasna", "Neem", "Basale", "Lemon", "Tulasi"]

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use 1 or 2 if needed

# Set webcam frame size to a higher resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Change to 1280 for better quality
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Change to 720 for a larger frame

if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

print("Press 'q' to quit the webcam.")

while True:
    ret, frame = cap.read()
    
    if not ret or frame is None:
        print("Error: Failed to capture frame.")
        continue  # Skip this frame

    # Convert frame to RGB (YOLO expects RGB format)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize frame to 640x640 (optional, for YOLO)
    frame_resized = cv2.resize(frame_rgb, (640, 640))  # Resize for YOLO model input

    # Perform inference
    results = model.predict(source=frame_resized, conf=0.5, save=False, show=False)

    # Get detections
    detections = results[0].boxes
    annotated_frame = frame.copy()

    for box in detections:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
        label = box.cls[0]  # Class label (numeric)
        name = model.names[int(label)]  # Class name

        if name in leaf_classes:
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_frame, name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Display the frame in a larger window
    cv2.imshow("Webcam Detection", annotated_frame)

    # Optionally resize the window if needed
    cv2.resizeWindow("Webcam Detection", 1280, 720)  # Resize the OpenCV window for better view

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
