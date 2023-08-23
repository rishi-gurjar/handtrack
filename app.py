import cv2
import mediapipe as mp

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
