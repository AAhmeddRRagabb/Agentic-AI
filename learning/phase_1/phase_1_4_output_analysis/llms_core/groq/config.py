# ---------------------
# Groq CFG
# ---------------------

JSON_SCHEMA_RESPONSE_FORMAT = "json_schema"
JSON_OBJECT_RESPONSE_FORMAT = "json_object"

SCHEMA_TYPES = set([
    JSON_SCHEMA_RESPONSE_FORMAT,
    JSON_OBJECT_RESPONSE_FORMAT,
])


PROVIDER_GROQ = "groq"
PROVIDER_GROQ         = "groq"
GROQ_LLAMA_8b         = "llama-3.1-8b-instant"
GROQ_LLAMA_70b        = "llama-3.3-70b-versatile"
GROQ_QWEN_32b         = "qwen/qwen3-32b"
GROQ_GPT_120b         = "openai/gpt-oss-120b"
GROQ_GPT_20b          = "openai/gpt-oss-20b"
GROQ_LLAMA_SCOUT      = "meta-llama/llama-4-scout-17b-16e-instruct"

PROVIDER_GOOGLE_GENAI = "google_genai"
GEMINI_FLASH_LITE     = "gemini-2.5-flash-lite"
GEMINI_FLASH          = "gemini-2.5-flash"