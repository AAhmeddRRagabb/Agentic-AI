# ------------------------------------
# General CFG
# ------------------------------------

from pydantic_settings import BaseSettings, SettingsConfigDict

SENSITIVE_KEYWORDS = {
    "password",
    "password_hash",
    "credit_card",
    "credit card",
    "token",
    "secret",
    "api_key",
    "national_id",
}


DB_TABLES_EXIST = {
    "customers",
    "products",
    "orders",
    "sales",
    "categories",
    "countries"
}

DB_ALLOWED_QUERY_TYPES = {
    "select"
}


ENV_PATH = "/mnt/d/Focus/_____Active_______/__Agentic_AI/Agentic_AI/.env"
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file          = ENV_PATH,
        env_file_encoding = "utf-8"
    )

    # API key
    GROQ_API_KEY  : str
    GOOGLE_API_KEY: str

def get_settings() -> Settings:
    return Settings()


