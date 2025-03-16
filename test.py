import os
import moviepy.editor as mp
import speech_recognition as sr

# Define file paths
video_path = r"D:\fullstack projects\sign_language_extension\sign_language_data\models\sample_video.mp4"
audio_output_path = r"D:\fullstack projects\sign_language_extension\sign_language_data\models\extracted_audio.wav_backup.wav"

def extract_audio_from_video(video_path, audio_output_path):
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_output_path)
        print(f"Audio extracted and saved at: {audio_output_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            transcription = recognizer.recognize_google(audio_data)
            print("Transcription: ", transcription)
            return transcription
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    return None

# Run the extraction and transcription
extract_audio_from_video(video_path, audio_output_path)
transcription_result = transcribe_audio(audio_output_path)

if transcription_result:
    # Save the transcription to a text file
    transcription_path = r"D:\fullstack projects\sign_language_extension\sign_language_data\models\transcription.txt"
    with open(transcription_path, "w", encoding="utf-8") as f:
        f.write(transcription_result)
    print(f"Transcription saved at: {transcription_path}")
