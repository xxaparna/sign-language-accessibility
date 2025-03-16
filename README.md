## 🚀 About the Project  
This project aims to **make video content accessible to the deaf community** by converting speech into **sign language animations**. It uses **AI-powered models** for **Speech-to-Text (STT)** and **Text-to-Sign (TTS)** translation.

## ✨ Features  
✅ Converts video speech to **text** using **Whisper STT**  
✅ Generates **sign language videos** from text  
✅ AI-powered **sign language translation**  
✅ Easy integration with browser extensions  

---

## 🛠 Tech Stack  
- **Backend:** FastAPI, Python  
- **AI Models:** Whisper STT, Custom TTS  
- **Frontend:** JavaScript (if applicable)  
- **Other Tools:** FFmpeg, OpenAI Whisper  

---
## 📂 Project Structure  
sign-language-project/ │── api/ # API endpoints (FastAPI) │── extension/ # Browser extension files (if any) │── sign_language_data/ # Dataset & models │ ├── datasets/ # Training data │ ├── models/ # Pretrained models & scripts │ ├── stt.py # Speech-to-Text script │ ├── tts.py # Text-to-Sign script │── preprocessing/ # Data preprocessing scripts │── utils/ # Utility functions │── transcription.txt # Extracted text from STT │── test_video.mp4 # Sample test video │── generate_translation.py # Main translation script │── README.md # Project documentation │── requirements.txt # Python dependencies │── venv/ # Virtual environment

## 🔥 Installation & Setup  

### 🖥 Prerequisites  
- **Python 3.9+**
- **FFmpeg installed** (Download from [FFmpeg](https://ffmpeg.org/download.html))
- **Virtual Environment** (recommended)

### 🚀 Steps to Run  
```bash
# Clone the repository
git clone https://github.com/your-username/sign-language-accessibility.git
cd sign-language-accessibility

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows

# Install dependencies
pip install -r requirements.txt

# Run the speech-to-text script
python sign_language_data/models/stt.py --video test_video.mp4

# Run the text-to-sign model
python sign_language_data/models/tts.py --input transcription.txt

# Run the main translation script
python generate_translation.py test_video.mp4
