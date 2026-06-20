from pydantic import BaseModel, ConfigDict

class SQLQueryGenerationSchema(BaseModel):
    model_config = ConfigDict(
        strict              = True,
        extra               = "forbid",
        validate_assignment = True
    )

    query: str | None
    required_query_type: str 
    tables_used: list[str] | None

    

