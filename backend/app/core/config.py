import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    LANGSMITH_API_KEY:  str | None = os.getenv("LANGSMITH_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    REEST_CSV_PATH: str = os.path.abspath(os.getenv("REEST_CSV_PATH", "data/reest.csv"))
    ALLOWED_FORMATS: set[str] = {"csv", "excel"}
    CORS_ORIGINS: list[str] = ["*"]
settings = Settings()
