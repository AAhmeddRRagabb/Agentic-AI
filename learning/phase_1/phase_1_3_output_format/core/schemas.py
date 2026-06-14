# -----------------------------------
# Response Format Json Schema
# -----------------------------------

from pydantic import BaseModel, ConfigDict
from typing import Literal

class SQLQueryGenerationSchema(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        strict = True,
        populate_by_name = True,
        extra = "forbid"
    )

    query: str

    query_type: Literal[
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE",
        "AGGREGATE",
        "JOIN",
        "SUBQUERY",
        "OTHER"
    ]

    tables_used: list[str]