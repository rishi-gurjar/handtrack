import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hand components
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Capture video stream from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, image = cap.read()
    if not ret:
        continue

    # Convert the BGR image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and find hand landmarks
    results = hands.process(image)

    # Draw the hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of the index finger tip and thumb tip
            index_finger_tip = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
                                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y]
            thumb_tip = [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
                         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y]

            # Calculate the average y-coordinate of all the hand landmarks
            avg_y = np.mean([landmark.y for landmark in hand_landmarks.landmark])

            # Map the average y-coordinate to a color value (you can customize this mapping)
            color_value = int(avg_y * 255)
            color = (color_value, 255 - color_value, 255)

            # Calculate the Euclidean distance between the index finger tip and thumb tip
            distance = np.linalg.norm(np.array(index_finger_tip) - np.array(thumb_tip))

            # Calculate the midpoint between the index finger tip and thumb tip
            midpoint = [(index_finger_tip[0] + thumb_tip[0]) / 2, (index_finger_tip[1] + thumb_tip[1]) / 2]

            # Convert the midpoint and radius to pixel coordinates
            circle_center = (int(midpoint[0] * image.shape[1]), int(midpoint[1] * image.shape[0]))
            circle_radius = int(distance * image.shape[1] / 2)

            # Draw the colored circle with thickness 5
            cv2.circle(image, circle_center, circle_radius, color, 5)

            # Draw the hand landmarks
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Convert the image back to BGR for displaying
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Display the image
    cv2.imshow('Hand Landmarks', image)

    # Break the loop if the 'ESC' key is pressed
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()
