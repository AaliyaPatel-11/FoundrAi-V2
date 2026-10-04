import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from backend/.env if it exists
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

# AI Configuration
AI_API_KEY = os.getenv("AI_API_KEY")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.groq.com/openai/v1")
AI_MODEL = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")

# CORS Setup
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "https://foundr-ai-v2-delta.vercel.app")
