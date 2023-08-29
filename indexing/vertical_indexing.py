# VERTICAL INDEXING

import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize MediaPipe Hand components
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Capture video stream from webcam
cap = cv2.VideoCapture(0)

# Variables to keep track of the previous distance and circle state
previous_distance = None
circle_open = False

count = 0

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
            index_finger_tip = np.array([hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
                                         hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y])
            thumb_tip = np.array([hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
                                  hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y])

            # Calculate the Euclidean distance between the index finger tip and thumb tip
            distance = np.linalg.norm(index_finger_tip - thumb_tip)

            # Calculate the midpoint between the index finger tip and thumb tip
            midpoint = (index_finger_tip + thumb_tip) / 2

            # Convert the midpoint and radius to pixel coordinates
            circle_center = (int(midpoint[0] * image.shape[1]), int(midpoint[1] * image.shape[0]))
            circle_radius = int(distance * image.shape[1] / 2)


            # Check if the tips are touching
            if previous_distance is not None and previous_distance > 0.02 and distance < 0.08:
                # Toggle the circle state
                circle_open = not circle_open

            num_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

            avg_y = np.mean([landmark.y for landmark in hand_landmarks.landmark])

            current_y = avg_y


            if(count == 0):
                index = 4
                print(num_array[index])
                saved_y = 0
                count += 1
            else:
                if(current_y < saved_y and index != 9):
                    index += 1
                    saved_y = current_y
                elif(current_y > saved_y and index != 0):
                    index -= 1
                    saved_y = current_y

            print("Array index: ", num_array[index])

            #print("Saved y: ", saved_y)
            #print("Current y: ", current_y)
            #print("Count:", count)

            color = (255, 255, 255)

            # Draw the colored circle only if circle_open is True
            if circle_open:
                cv2.circle(image, circle_center, circle_radius, color, 20)

            # Draw the hand landmarks
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Update previous_distance for the next iteration
            previous_distance = distance

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
