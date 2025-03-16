import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Sample gestures for sign language (Replace with actual dataset)
SIGN_GESTURES = {
    "hello": np.array([0.5, 0.3, 0.2, 0.7, 0.1]),  
    "thank": np.array([0.6, 0.2, 0.3, 0.8, 0.15]),
    "you": np.array([0.4, 0.25, 0.5, 0.6, 0.2]),
}

def generate_sign_gesture(text):
    """Generates sign language gestures from text."""
    cap = cv2.VideoCapture(0)  # Open webcam
    hands = mp.solutions.hands.Hands()
    words = text.split()
    
    for word in words:
        print(f"🎥 Generating sign for: {word}")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

            cv2.putText(frame, f"Sign: {word}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow("Sign Language Generator", frame)

            if cv2.waitKey(300) & 0xFF == ord("q"):
                break  # Move to the next word

    cap.release()
    cv2.destroyAllWindows()
    return f"Generated sign sequence for: {text}"

@app.route("/generate_sign", methods=["POST"])
def generate_sign():
    data = request.get_json()
    transcript = data.get("transcript")

    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400

    response = g
