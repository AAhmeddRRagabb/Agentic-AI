# ---------------------------------------------------------
# Different response formats according to the given model
# ---------------------------------------------------------


from .schemas import SQLQueryGenerationSchema

BEST_EFFORT_MODE_MODELS = [
    "openai/gpt-oss-safeguard-20b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]


STRICT_MODE_MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b"
]



def json_schema_format(strict: bool) -> dict[str, str]:
    return {
        "type"       : "json_schema",
        "json_schema": {
            "name"  : "sql_query_generation",
            "strict": strict,
            "schema": SQLQueryGenerationSchema.model_json_schema()
        }
    } 



def get_response_format(model_name: str) -> dict[str, str]:
    if model_name in STRICT_MODE_MODELS:
        return json_schema_format(True)
    
    elif model_name in BEST_EFFORT_MODE_MODELS:
        return json_schema_format(False)
    
    else:
        return {
            "type": "json_object"
        }
