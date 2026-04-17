import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = "llama3-70b-8192"

    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            print("❌ GROQ_API_KEY not set")
            return False
        print("✅ GROQ API Key Loaded")
        return True