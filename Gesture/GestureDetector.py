import cv2
import mediapipe as mp
import numpy as np
import pyautogui

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize Mediapipe Hands model
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        print("✅ MediaPipe Hands model loaded successfully.")

        # Gesture-to-key mapping
        self.gesture_to_key = {
            "open": "w",
            "fist": "s",
            "left": "a",
            "right": "d"
        }

    def recognize_gesture(self, landmarks):
        """
        Simple heuristic-based gesture recognition.
        Returns one of: 'open', 'fist', 'left', 'right', or None.
        """
        # Convert landmarks to numpy array
        points = np.array([[lm.x, lm.y, lm.z] for lm in landmarks.landmark])

        # Finger tip indices (thumb, index, middle, ring, pinky)
        tips = [4, 8, 12, 16, 20]

        # Count how many fingers are open (fingertip higher than its lower joint)
        open_fingers = 0
        for tip in tips[1:]:  # skip thumb for simplicity
            if points[tip][1] < points[tip - 2][1]:
                open_fingers += 1

        # Gesture classification
        if open_fingers >= 4:
            return "open"
        elif open_fingers == 0:
            return "fist"
        else:
            wrist_x = points[0][0]
            if wrist_x < 0.4:
                return "left"
            elif wrist_x > 0.6:
                return "right"
        return None

    def detect_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            print("❌ Error: Cannot read image.")
            return

        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                gesture = self.recognize_gesture(hand_landmarks)
                if gesture:
                    print(f"🖐 Gesture detected: {gesture}")
                    cv2.putText(image, f"Gesture: {gesture.upper()}",
                                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2)

        cv2.imshow("Gesture Detection - Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def detect_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("❌ Error: Cannot open video.")
            return

        print("🎞 Press 'q' to quit video detection.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )

                    gesture = self.recognize_gesture(hand_landmarks)
                    if gesture:
                        print(f"🖐 Gesture detected: {gesture}")
                        cv2.putText(frame, f"Gesture: {gesture.upper()}",
                                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 2)

            cv2.imshow("Gesture Detection - Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def detect_webcam(self, cam_index=3):
        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            print("❌ Error: Cannot access webcam.")
            return

        print("📷 Press 'q' to quit webcam mode.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )

                    gesture = self.recognize_gesture(hand_landmarks)
                    if gesture:
                        print(f"🖐 Gesture detected: {gesture}")

                        # Display the gesture name on the frame
                        cv2.putText(frame, f"Gesture: {gesture.upper()}",
                                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 2)

                        # Simulate key press
                        key = self.gesture_to_key.get(gesture)
                        if key:
                            pyautogui.press(key)

            cv2.imshow("Gesture Control - Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
