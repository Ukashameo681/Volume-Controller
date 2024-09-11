import cv2
import math
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize hand detector with a confidence of 0.7
detector = htm.handDetector(detectionCon=0.7)

# Initial rectangle properties (x, y, width, height)
rect_x, rect_y, rect_width, rect_height = 10, 10, 100, 100

# Set default color for the rectangle
rectangle_color = (255, 0, 255)

# Start video capture loop
while True:
    success, img = cap.read()  # Capture frame from webcam
    if not success:
        break

    # Detect hands in the image
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    # Check if any hands are detected
    if len(lmList) != 0:
        # Get the positions of index finger (point 8) and middle finger (point 12)
        index_x, index_y = lmList[8][1], lmList[8][2]
        middle_x, middle_y = lmList[12][1], lmList[12][2]

        # Calculate the center of the line between index and middle fingers
        center_x, center_y = (index_x + middle_x) // 2, (index_y + middle_y) // 2

        # Draw the index and middle fingers
        cv2.circle(img, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (middle_x, middle_y), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (index_x, index_y), (middle_x, middle_y), (255, 0, 255), 3)
        cv2.circle(img, (center_x, center_y), 15, (255, 0, 255), cv2.FILLED)

        # Calculate the distance between index and middle fingers
        finger_distance = math.hypot(middle_x - index_x, middle_y - index_y)

        # Move the rectangle if the fingers are close together and within the rectangle area
        if finger_distance < 50:
            if rect_x <= index_x <= rect_x + rect_width and rect_y <= index_y <= rect_y + rect_height:
                rectangle_color = (0, 255, 0)  # Change color to green when the rectangle is grabbed
                rect_x, rect_y = center_x - rect_width // 2, center_y - rect_height // 2
            else:
                rectangle_color = (255, 0, 255)  # Reset color to default

    # Draw the rectangle
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), rectangle_color, cv2.FILLED)

    # Display the video feed in a resized window
    cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Hand Tracking", 800, 600)
    cv2.imshow("Hand Tracking", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
