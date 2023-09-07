import cv2
import mediapipe as mp
import numpy as np
import math

# RotationalIndexer

# rahul text
class RotationalIndexer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)  # set video width
        self.cap.set(4, 480)  # set video height
        self.previous_distance = None
        self.circle_open = False
        self.count = 0
        self.array_count = 4
        self.saved_angle = 0

    def rotate(self):
        ret, image = self.cap.read()
        if not ret:
            return None, None

        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and find hand landmarks
        results = self.hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip = np.array([hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
                                            hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y])
                thumb_tip = np.array([hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x,
                                    hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y])

                distance = np.linalg.norm(index_finger_tip - thumb_tip)

                if self.previous_distance is not None and self.previous_distance > 0.02 and distance < 0.08:
                    self.circle_open = not self.circle_open

                num_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

                current_angle = math.degrees(math.atan2(index_finger_tip[1] - thumb_tip[1], index_finger_tip[0] - thumb_tip[0]))
                current_angle = abs(current_angle) % 180

                print("array count", self.array_count)
                print("current angle", current_angle)
                print("saved angle", self.saved_angle)
                print("count", self.count)

                if self.count == 0:
                    self.saved_angle = 0
                    self.array_count = 4
                    self.count += 1
                else:
                    if ((current_angle - self.saved_angle) < 0.5) and self.array_count != 9:
                    # if abs(current_angle > self.saved_angle) and self.array_count != 9:
                        self.array_count += 1
                        self.saved_angle = current_angle
                    elif ((current_angle - self.saved_angle) > 0.5) and self.array_count != 0:
                    # elif abs(current_angle < self.saved_angle) and self.array_count != 0:
                        self.array_count -= 1
                        self.saved_angle = current_angle

                self.previous_distance = distance
            print("1st text", num_array[self.array_count])
            return num_array[self.array_count], image  # Return both index and image

        else:
            return None, None

    def run(self):
        while self.cap.isOpened():
            
            ret, image = self.cap.read()
            if not ret:
                continue

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #cv2.imshow('Hand Landmarks', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break


        self.cap.release()
        cv2.destroyAllWindows()
