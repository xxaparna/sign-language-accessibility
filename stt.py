import os
import subprocess
import whisper
import time
import shutil
import tempfile
import logging
from typing import Optional, Tuple

class SpeechToText:
    def __init__(self, model_size: str = "base", ffmpeg_path: Optional[str] = None, language: Optional[str] = None):
        """
        Initialize the Speech-to-Text processor with Whisper.
        
        Args:
            model_size: Size of the Whisper model ('tiny', 'base', 'small', 'medium', 'large')
            ffmpeg_path: Path to ffmpeg executable, uses system path if None
            language: Target language code (e.g., 'en' for English) to improve transcription accuracy
        """
        # Set up logging
        self.setup_logging()
        
        # Force CPU usage to avoid CUDA errors
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        
        # Ensure the whisper cache directory exists
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "whisper")
        os.makedirs(cache_dir, exist_ok=True)
        self.logger.info(f"Whisper cache directory: {cache_dir}")
        
        self.logger.info("Initializing Whisper Model...")
        try:
            # Try to load the model with explicit download location
            self.model = whisper.load_model(model_size, download_root=cache_dir)
            self.logger.info(f"Whisper Model '{model_size}' loaded successfully!")
        except Exception as e:
            self.logger.error(f"Error loading Whisper Model: {e}")
            
            # Try to download the model manually
            try:
                self.logger.info(f"Attempting to download model '{model_size}' manually...")
                model_path = os.path.join(cache_dir, f"{model_size}.pt")
                if not os.path.exists(model_path):
                    whisper._download(model_size, cache_dir, False)
                    self.logger.info(f"Model downloaded to {model_path}")
                
                # Try loading again
                self.model = whisper.load_model(model_size, download_root=cache_dir)
                self.logger.info("Model loaded successfully after manual download!")
            except Exception as download_error:
                self.logger.error(f"Manual download failed: {download_error}")
                raise

        self.ffmpeg_path = ffmpeg_path or "ffmpeg"
        self.language = language
        self.temp_files = []  # Track temporary files for cleanup
    
    def setup_logging(self):
        """Configure logging for the module."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger('SpeechToText')

    def extract_audio(self, video_path: str) -> Optional[str]:
        """
        Extracts audio from video and saves it as a temporary file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Path to the extracted audio file or None if extraction failed
        """
        if not os.path.exists(video_path):
            self.logger.error(f"Video file not found: {video_path}")
            return None
            
        temp_dir = tempfile.gettempdir()
        self.logger.info(f"Using temporary directory: {temp_dir}")
        
        filename = os.path.basename(video_path).split('.')[0]
        audio_wav_path = os.path.join(temp_dir, f"{filename}_extracted_audio.wav")
        self.temp_files.append(audio_wav_path)

        self.logger.info(f"Extracting audio from {video_path}...")
        self.logger.info(f"Output audio will be saved to: {audio_wav_path}")

        command = f'"{self.ffmpeg_path}" -i "{video_path}" -acodec pcm_s16le -ar 16000 -ac 1 "{audio_wav_path}" -y'
        
        try:
            self.logger.debug(f"Running command: {command}")
            subprocess.run(command, shell=True, check=True)
            
            if os.path.exists(audio_wav_path):
                file_size = os.path.getsize(audio_wav_path)
                self.logger.info(f"Audio extracted: {audio_wav_path} (Size: {file_size} bytes)")
                return audio_wav_path
            else:
                self.logger.error("Audio file not created despite successful command execution")
                return None
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"FFmpeg audio extraction failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during audio extraction: {e}")
            return None

    def transcribe_audio(self, audio_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Transcribes extracted audio and saves it to a temporary file.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Tuple of (path to transcription file, raw transcription text) or (None, None) on failure
        """
        self.logger.info(f"Checking file before transcription: {audio_path}")

        if not os.path.exists(audio_path):
            self.logger.error(f"Error: Audio file not found -> {audio_path}")
            return None, None
            
        # Check file size and permissions
        try:
            file_size = os.path.getsize(audio_path)
            self.logger.info(f"Audio file size: {file_size} bytes")
            
            # Check if file is readable
            with open(audio_path, 'rb') as f:
                f.read(10)  # Try to read first 10 bytes
                self.logger.info("Audio file is readable")
        except Exception as e:
            self.logger.error(f"Error accessing audio file: {e}")
            return None, None

        try:
            self.logger.info("Transcribing with Whisper...")
            
            # Check whisper cache directory
            cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "whisper")
            if os.path.exists(cache_dir):
                self.logger.info(f"Whisper cache directory exists: {cache_dir}")
                try:
                    cache_contents = os.listdir(cache_dir)
                    self.logger.info(f"Cache contents: {cache_contents}")
                except Exception as e:
                    self.logger.warning(f"Could not list cache directory contents: {e}")
            else:
                self.logger.warning(f"Whisper cache directory not found: {cache_dir}")
            
            # Configure transcription options
            options = {}
            if self.language:
                options["language"] = self.language
            
            # Add word-level timestamps for better synchronization
            options["word_timestamps"] = True
            
            # Convert backslashes to forward slashes for compatibility
            normalized_path = audio_path.replace('\\', '/')
            self.logger.info(f"Using normalized path for transcription: {normalized_path}")
            
            result = self.model.transcribe(normalized_path, **options)
            transcription = result["text"]
            
            # Create a unique filename
            filename = os.path.basename(audio_path).split('_extracted_audio')[0]
            temp_transcript_path = os.path.join(tempfile.gettempdir(), f"{filename}_transcription.txt")
            self.temp_files.append(temp_transcript_path)
            
            with open(temp_transcript_path, "w", encoding="utf-8") as f:
                f.write(transcription)
                
                # Optionally, also save word-level timestamps if available
                if "segments" in result:
                    f.write("\n\n--- Word Timestamps ---\n")
                    for segment in result["segments"]:
                        if "words" in segment:
                            for word_data in segment["words"]:
                                f.write(f"{word_data['word']}: {word_data['start']:.2f}s - {word_data['end']:.2f}s\n")

            self.logger.info(f"Transcription saved to: {temp_transcript_path}")
            return temp_transcript_path, transcription
        except Exception as e:
            self.logger.error(f"Error in transcription: {e}")
            import traceback
            self.logger.error(f"Detailed traceback: {traceback.format_exc()}")
            return None, None

    def transcribe_video(self, video_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts audio and transcribes it.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Tuple of (path to transcription file, raw transcription text) or (None, None) on failure
        """
        self.logger.info(f"Starting transcription process for: {video_path}")
        
        audio_path = self.extract_audio(video_path)
        if audio_path:
            transcript_path, transcript_text = self.transcribe_audio(audio_path)
            return transcript_path, transcript_text
        return None, None
    
    def cleanup(self):
        """Remove all temporary files created during processing."""
        for file_path in self.temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.logger.debug(f"Deleted temporary file: {file_path}")
            except Exception as e:
                self.logger.warning(f"Could not delete temporary file {file_path}: {e}")
        
        self.temp_files = []


# --- Run Script ---
if __name__ == "__main__":
    import argparse
    import sys
    
    # Default values that match your original script
    default_ffmpeg_path = r"D:\ffmpeg-2025-03-13-git-958c46800e-essentials_build\ffmpeg-2025-03-13-git-958c46800e-essentials_build\bin\ffmpeg.exe"
    default_video_path = r"D:\fullstack projects\sign_language_extension\sign_language_data\models\test_video.mp4"
    
    # Check if any command line arguments were provided
    if len(sys.argv) > 1:
        # Use argparse if arguments were provided
        parser = argparse.ArgumentParser(description="Transcribe video audio using Whisper")
        parser.add_argument("--video", required=True, help="Path to the video file")
        parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"], 
                            help="Whisper model size")
        parser.add_argument("--ffmpeg", default=None, help="Path to ffmpeg executable")
        parser.add_argument("--language", default=None, help="Target language code (e.g., 'en' for English)")
        
        args = parser.parse_args()
        video_path = args.video
        ffmpeg_path = args.ffmpeg or default_ffmpeg_path
        model_size = args.model
        language = args.language
    else:
        # Use default values if no arguments were provided (backwards compatibility)
        video_path = default_video_path
        ffmpeg_path = default_ffmpeg_path
        model_size = "base"
        language = None
        print(f"Using default video: {video_path}")
    
    try:
        stt = SpeechToText(model_size=model_size, ffmpeg_path=ffmpeg_path, language=language)
        transcript_path, transcript_text = stt.transcribe_video(video_path)

        if transcript_path:
            print(f"\n✅ Final Transcription saved at: {transcript_path}")
            print("\n--- Beginning of Transcription ---")
            print(transcript_text[:500] + "..." if len(transcript_text) > 500 else transcript_text)
            print("--- End of Transcription Preview ---\n")
        else:
            print("❌ Transcription failed.")
    finally:
        # Clean up temporary files
        if 'stt' in locals():
            stt.cleanup()