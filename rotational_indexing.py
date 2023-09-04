import cv2
import mediapipe as mp
import numpy as np
import math

class RotationalIndexer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.previous_distance = None
        self.circle_open = False
        self.count = 0
        self.array_count = 4
        self.saved_angle = 0

    def rotate(self):
        ret, image = self.cap.read()
        if not ret:
            return None

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

                if self.count == 0:
                    self.saved_angle = 0
                    self.count += 1
                else:
                    if abs(current_angle - self.saved_angle) < 0.5 and self.array_count != 9:
                        self.array_count += 1
                        self.saved_angle = current_angle
                    elif abs(current_angle - self.saved_angle) > 0.5 and self.array_count != 0:
                        self.array_count -= 1
                        self.saved_angle = current_angle

                self.previous_distance = distance
                return num_array[self.array_count]
        else:
            return None

    def run(self):
        while self.cap.isOpened():
            index = self.rotate()
            
            ret, image = self.cap.read()
            if not ret:
                continue

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imshow('Hand Landmarks', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break


        self.cap.release()
        cv2.destroyAllWindows()