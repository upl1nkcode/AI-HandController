import cv2
import mediapipe as mp

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        # Create the Mediapipe Hands model once
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        print("✅ MediaPipe Hands model loaded successfully.")

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

            cv2.imshow("Gesture Detection - Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def detect_webcam(self, cam_index=0):
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

            cv2.imshow("Gesture Detection - Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
