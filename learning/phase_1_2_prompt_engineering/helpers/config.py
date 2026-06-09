# ---------------------------------
# System Configurations
# ---------------------------------

from pydantic_settings import BaseSettings, SettingsConfigDict




ENV_PATH = "/mnt/d/Focus/_____Active_______/__Agentic_AI/Agentic_AI/.env"
class Settings(BaseSettings):
    """
    Application Settings - Read .env file
    """
    model_config = SettingsConfigDict(
        env_file          = ENV_PATH,
        env_file_encoding = "utf-8"
    )


    # API key
    GROQ_API_KEY  : str
    GOOGLE_API_KEY: str

def get_settings() -> Settings:
    return Settings()


# --- Model Names ---
PROVIDER_GROQ         = "groq"
GROQ_LLAMA_8b         = "llama-3.1-8b-instant"
GROQ_LLAMA_70b        = "llama-3.3-70b-versatile"
GROQ_QWEN_32b         = "qwen/qwen3-32b"
GROQ_GPT_120b         = "openai/gpt-oss-120b"
GROQ_GPT_20b          = "openai/gpt-oss-20b"

PROVIDER_GOOGLE_GENAI = "google_genai"
GEMINI_FLASH_LITE     = "gemini-2.5-flash-lite"
GEMINI_FLASH          = "gemini-2.5-flash"
