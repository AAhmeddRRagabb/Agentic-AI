
def get_json_schema_prompt(query: str) -> str:
    prompt = f"""
You are a SQL expert. We are building an automation system that should take a user query that is in a natural language description and convert it into SQL queries.
You are employed to perform this task. Generate a structured SQL query for the given natural language query.

---

Example:
Natural Language Query: Find all users that have not opened the application in the last 30 days.

SQL Query: Select * FROM users WHERE was_active_since > 30

---

Natural Language Query: {query}\n

"""
    return prompt


def get_json_object_prompt(query: str) -> str:
    prompt = f"""
You are a SQL expert. We are building an automation system that should take a user query that is in a natural language description and convert it into SQL queries.
You are employed to perform this task. Generate a structured SQL query for the given natural language query.

You should return the output in the following json schema:
{{
    "query": string represents the SQL query you have generated.
    "query_type": string represents the query type (SELECT, UPDATE, etc.)
    "tables_used": a list of the names of the tables used
}}


---

Example:
Natural Language Query: Find all users that have not opened the application in the last 30 days.

Response: 
{{
    "query": "SELECT * FROM users WHERE was_active_since > 30"m
    "query_type": "SELECT",
    "tables_used": ["users"]
}}

---

Natural Language Query: {query}\n
Response:

"""
    return prompt


def get_prompt(query: str, response_format_type: str) -> str:
    if response_format_type == "json_schema":
        return (
            "json_schema_prompt", get_json_schema_prompt(query)
        )
    else:
        return (
            "json_object_prompt", get_json_object_prompt(query)
        )