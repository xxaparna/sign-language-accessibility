from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from pydantic import BaseModel
import subprocess
import logging

app = FastAPI(title="Sign Language Video Accessibility API")

# ✅ Enable CORS (Important for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Include routes from routes.py
app.include_router(router)

class VideoRequest(BaseModel):
    video_url: str

@app.post("/translate/")
async def translate_video(request: VideoRequest):
    video_url = request.video_url

    try:
        logger.info(f"📌 Processing video: {video_url}")

        # ✅ Run translation script safely with error handling
        result = subprocess.run(
            ["python", "generate_translation.py", video_url],
            capture_output=True,
            text=True
        )

        logger.info(f"📌 STDOUT: {result.stdout}")
        logger.error(f"⚠️ STDERR: {result.stderr}")  # Print script errors if any

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Translation script error: {result.stderr}")

        translation_output = result.stdout.strip()
        return {"message": "Translation successful", "translation": translation_output}

    except Exception as e:
        logger.exception("🚨 Unexpected error occurred")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/")
def home():
    return {"message": "✅ Sign Language API is running!"}

# ✅ Run FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
