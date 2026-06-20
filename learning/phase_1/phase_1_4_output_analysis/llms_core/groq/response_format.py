
from typing import Any
from pydantic import BaseModel
from .config import JSON_SCHEMA_RESPONSE_FORMAT, JSON_OBJECT_RESPONSE_FORMAT

BEST_EFFORT_MODE_MODELS = [
    "openai/gpt-oss-safeguard-20b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]


STRICT_MODE_MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b"
]



def get_json_schema_format(strict: bool, schema: type[BaseModel]) -> dict[str, Any]:
    return {
        "type": JSON_SCHEMA_RESPONSE_FORMAT,
        "json_schema": {
            "name"  : "structured_response_format",
            "strict": strict,
            "schema": schema.model_json_schema()
        }
    }

def get_response_format(model_name: str, schema: type[BaseModel]) -> dict[str, Any]:
    if model_name in STRICT_MODE_MODELS:
        return get_json_schema_format(strict = True, schema = schema)
    elif model_name in BEST_EFFORT_MODE_MODELS:
        return get_json_schema_format(strict = False, schema = schema)
    else:
        return {
            "type": JSON_OBJECT_RESPONSE_FORMAT
        }
