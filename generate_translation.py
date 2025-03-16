import sys
import subprocess
import os

def run_stt_model(video_url):
    """
    Runs the STT model to extract audio from the video and convert it to text.
    Saves the output in 'transcription.txt'.
    """
    stt_command = ["python", "stt_model.py", video_url]
    result = subprocess.run(stt_command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error in STT Model: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    print(f"STT Output: {result.stdout}")

def run_tts_model():
    """
    Runs the TTS model using 'transcription.txt' to generate sign language video.
    """
    if not os.path.exists("transcription.txt"):
        print("Error: transcription.txt not found.", file=sys.stderr)
        sys.exit(1)
    
    tts_command = ["python", "tts_model.py"]
    result = subprocess.run(tts_command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error in TTS Model: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    return result.stdout.strip()

def generate_translation(video_url):
    print(f"Processing video: {video_url}")
    run_stt_model(video_url)
    sign_language_video = run_tts_model()
    return sign_language_video

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No video URL provided.", file=sys.stderr)
        sys.exit(1)
    
    video_url = sys.argv[1]
    output_video = generate_translation(video_url)
    print(f"Generated Sign Language Video: {output_video}")
