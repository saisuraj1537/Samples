import cv2
import cv2.aruco as aruco
import math

# Initialize the webcam (0 is the default camera)
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Force using v4l2

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

# Set a higher frame rate (FPS)
cap.set(cv2.CAP_PROP_FPS, 60)  # Try setting the FPS to 60 (or a value supported by your webcam)

# Define the dictionary used to detect the markers (you can choose other dictionaries too)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters_create()

# Get the frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the center of the frame
frame_center = (frame_width // 2, frame_height // 2)

# Define the known width of the ArUco marker in cm (e.g., 5 cm)
known_marker_width_cm = 17.0  # change this value to your marker's real-world width

# Estimate focal length (in pixels) based on a known distance to the marker
focal_length = 600  # This is an example, and should be calibrated for your camera

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Convert the frame to grayscale (ArUco detection works better in grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers
    corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # If markers are detected
    if len(corners) > 0:
        for corner in corners:
            # Calculate the center of the ArUco marker (mean of the four corners)
            marker_center = tuple(map(int, corner[0].mean(axis=0)))

            # Draw the detected marker
            frame = aruco.drawDetectedMarkers(frame, corners, ids)

            # Calculate the width of the marker in the image
            marker_width_in_image = int(math.sqrt((corner[0][0][0] - corner[0][1][0])**2 + 
                                                  (corner[0][0][1] - corner[0][1][1])**2))

            # Calculate the distance from the camera to the marker using the formula
            distance_cm = (known_marker_width_cm * focal_length) / marker_width_in_image

            # Calculate the displacement from the center of the frame
            delta_x = marker_center[0] - frame_center[0]
            delta_y = marker_center[1] - frame_center[1]

            # Calculate the movement distance to the center (in cm)
            move_distance_x = (delta_x / frame_width) * distance_cm
            move_distance_y = (delta_y / frame_height) * distance_cm

            # Print directions or "land" along with the distance in cm
            if abs(delta_x) < 50 and abs(delta_y) < 50:  # Marker is near the center
                print(f"Land (Distance: {distance_cm:.2f} cm), Move X: {move_distance_x:.2f} cm, Move Y: {move_distance_y:.2f} cm")
            elif delta_x > 50:
                print(f"Move Right (Distance: {distance_cm:.2f} cm), Move X: {move_distance_x:.2f} cm")
            elif delta_x < -50:
                print(f"Move Left (Distance: {distance_cm:.2f} cm), Move X: {move_distance_x:.2f} cm")
            elif delta_y > 50:
                print(f"Move Down (Distance: {distance_cm:.2f} cm), Move Y: {move_distance_y:.2f} cm")
            elif delta_y < -50:
                print(f"Move Up (Distance: {distance_cm:.2f} cm), Move Y: {move_distance_y:.2f} cm")

    # Display the resulting frame
    cv2.imshow('Webcam Feed with ArUco Detection and Direction', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()

