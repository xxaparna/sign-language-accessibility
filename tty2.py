import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf

# Load the pre-trained model (Assume it's a gesture classification model)
model = tf.keras.models.load_model("sign_language_model.h5")

# Initialize MediaPipe Hands for detecting hand gestures
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Mapping of text characters to predefined gestures (simplified)
sign_language_dict = {
    "hello": 0, "thank you": 1, "yes": 2, "no": 3, "please": 4,
    "a": 5, "b": 6, "c": 7, "d": 8, "e": 9
}

def process_text(text):
    words = text.lower().split()
    return [sign_language_dict[word] for word in words if word in sign_language_dict]

# Open Webcam for real-time demonstration
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract keypoints
            keypoints = []
            for landmark in hand_landmarks.landmark:
                keypoints.append([landmark.x, landmark.y, landmark.z])
            keypoints = np.array(keypoints).flatten()

            # Predict the sign
            prediction = model.predict(np.expand_dims(keypoints, axis=0))
            predicted_sign = np.argmax(prediction)

            # Find corresponding word
            word = list(sign_language_dict.keys())[list(sign_language_dict.values()).index(predicted_sign)]
            cv2.putText(frame, word, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Sign Language Translator", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
