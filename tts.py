import os
import sys
import cv2
import imageio
import numpy as np
from pathlib import Path

class TextToSign:
    def __init__(self, transcription_file, sign_gif_folder):
        self.transcription_file = Path(transcription_file)
        self.sign_gif_folder = Path(sign_gif_folder)

        self._validate_paths()

    def _validate_paths(self):
        """Validates if the required files and directories exist."""
        if not self.transcription_file.exists():
            sys.exit(f"❌ Error: Transcription file not found -> {self.transcription_file}")

        if not self.sign_gif_folder.exists():
            sys.exit(f"❌ Error: Sign GIF folder not found -> {self.sign_gif_folder}")

    def load_transcription(self):
        """Loads and returns the transcription text."""
        try:
            text = self.transcription_file.read_text(encoding="utf-8").strip()
            if not text:
                print("⚠️ Warning: Transcription file is empty.")
            else:
                print(f"📜 Loaded Transcription: {text}")
            return text
        except Exception as e:
            sys.exit(f"❌ Error reading transcription file: {e}")

    def word_to_sign(self, word):
        """Finds the corresponding sign GIF for a word."""
        word_gif = self.sign_gif_folder / f"{word.lower()}.gif"
        return str(word_gif) if word_gif.exists() else None

    def display_sign_language(self, words):
        """Displays sign language animations for words."""
        if not words:
            print("⚠️ No words to convert.")
            return

        for word in words:
            sign_gif = self.word_to_sign(word)
            if sign_gif:
                print(f"🎥 Displaying sign for: {word}")
                self.play_gif(sign_gif)
            else:
                print(f"⚠️ No sign found for: {word}. Consider fingerspelling.")

    def play_gif(self, gif_path):
        """Plays a GIF using OpenCV."""
        try:
            gif_frames = imageio.mimread(gif_path)
            if not gif_frames:
                print(f"❌ Error: Failed to load GIF -> {gif_path}")
                return
            
            cv2.namedWindow("Sign Language Animation", cv2.WINDOW_NORMAL)
            for frame in gif_frames:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imshow("Sign Language Animation", frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    print("⏹️ Animation stopped by user.")
                    break

            cv2.destroyAllWindows()
        except Exception as e:
            print(f"❌ Error playing GIF: {e}")

    def convert_text_to_sign(self):
        """Processes transcription and displays sign animations."""
        text = self.load_transcription()
        words = text.split()

        if not words:
            print("⚠️ No words found in transcription.")
            return

        print("🔄 Converting text to sign language...")
        self.display_sign_language(words)
        print("✅ Conversion Complete!")


# --- Run Script ---
if __name__ == "__main__":
    transcription_file = r"D:\fullstack projects\sign_language_extension\sign_language_data\models\transcription.txt"
    sign_gif_folder = r"D:\fullstack projects\sign_language_extension\sign_gifs"

    tts = TextToSign(transcription_file, sign_gif_folder)
    tts.convert_text_to_sign()
