# Structured Output and Schema Enforcement

This project demonstrates how provider-level structured output, Pydantic validation, and fallback parsing strategies can make LLM responses safer and more reliable.

The app tests multiple Groq models on a natural-language-to-SQL generation task. Each model receives a natural language query and must return a structured response that matches a strict schema.

The task is designed to measure structured output reliability, not SQL execution correctness.

The app evaluates three Groq models:

- `llama-3.1-8b-instant`
- `llama-3.3-70b-versatile`
- `meta-llama/llama-4-scout-17b-16e-instruct`

The goal is to compare how different response-format modes and validation layers affect:

- JSON validity
- schema correctness
- required field enforcement
- type enforcement
- enum enforcement
- extra-field rejection
- malformed output handling
- fallback parsing reliability

---

## Objective

Evaluate whether LLM responses can be safely converted into validated structured objects before being used by an application.

The tested structured output strategies are:

1. JSON Schema response format
2. JSON Object response format
3. Pydantic validation
4. Text-noise removal fallback
5. Validation-error logging

---

## Task Description

Given a natural language query, the model should generate a SQL query and return a valid structured object containing:

| Field | Meaning |
|---|---|
| `query` | The generated SQL query |
| `query_type` | The type of SQL query generated |
| `tables_used` | A list of table names used in the generated query |

Example natural language query:

```text
Show each customer with the total number of orders they have placed.
```

Expected structured output:

```json
{
  "query": "SELECT customers.id, customers.name, COUNT(orders.id) AS total_orders FROM customers LEFT JOIN orders ON customers.id = orders.customer_id GROUP BY customers.id, customers.name",
  "query_type": "JOIN",
  "tables_used": ["customers", "orders"]
}
```

---

## Dataset

The dataset contains 20 natural language SQL-generation queries.

Each sample has the following structure:

```json
{
  "complexity": "medium",
  "query": "Show each customer with the total number of orders they have placed."
}
```

The queries include different complexity levels:

| Complexity | Description |
|---|---|
| `low` | Simple selection, filtering, and counting |
| `medium` | Joins, grouping, ordering, and aggregation |
| `high` | Subqueries, ranking, comparison against averages, and more advanced SQL logic |

Example queries include:

- Show all customers.
- Get the total number of users.
- Find the top 5 products by total sales quantity.
- Show the total revenue for each month in 2025.
- Find customers whose total spending is higher than the average total spending of all customers.
- Calculate the month-over-month revenue growth percentage for each month.
- Rank customers by total spending within each country.

---

## Schema Used

The app validates every model response using a Pydantic schema.

```python
from pydantic import BaseModel, ConfigDict
from typing import Literal


class SQLQueryGenerationSchema(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        strict=True,
        populate_by_name=True,
        extra="forbid"
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
```

The schema enforces:

| Constraint | Meaning |
|---|---|
| Required fields | The model must return `query`, `query_type`, and `tables_used` |
| Field types | `query` must be a string, `query_type` must be an allowed literal value, and `tables_used` must be a list of strings |
| Enum validation | `query_type` must be one of the predefined SQL query types |
| Extra-field rejection | `extra="forbid"` prevents the model from returning unexpected fields |
| Strict validation | Pydantic validates the response before the app treats it as usable |

---

## Response Formats Used

The app selects a response format based on the model being tested.

### 1. JSON Schema Response Format

For models that support structured schema mode, the app uses:

```python
{
    "type": "json_schema",
    "json_schema": {
        "name": "sql_query_generation",
        "strict": true,
        "schema": SQLQueryGenerationSchema.model_json_schema()
    }
}
```

This mode attempts to force the model to follow the supplied JSON schema directly.

---

### 2. Best-Effort JSON Schema Format

For models that support schema guidance but may not fully enforce strict output, the app uses:

```python
{
    "type": "json_schema",
    "json_schema": {
        "name": "sql_query_generation",
        "strict": false,
        "schema": SQLQueryGenerationSchema.model_json_schema()
    }
}
```

This mode still provides the schema to the provider, but validation is still required after receiving the response.

---

### 3. JSON Object Response Format

For models that do not use the stricter schema mode, the app falls back to:

```python
{
    "type": "json_object"
}
```

This mode encourages the model to return valid JSON, while Pydantic still performs the real schema validation inside the app.

---

## Prompts Used

### 1. JSON Schema Prompt

This prompt is used when the API response format already provides the schema.

```text
You are a SQL expert. We are building an automation system that should take a user query that is in a natural language description and convert it into SQL queries.
You are employed to perform this task. Generate a structured SQL query for the given natural language query.

---

Example:
Natural Language Query: Find all users that have not opened the application in the last 30 days.

SQL Query: Select * FROM users WHERE was_active_since > 30

---

Natural Language Query:
```

---

### 2. JSON Object Prompt

This prompt is used when the API response format is `json_object`, so the expected JSON structure is included inside the prompt itself.

```text
You are a SQL expert. We are building an automation system that should take a user query that is in a natural language description and convert it into SQL queries.
You are employed to perform this task. Generate a structured SQL query for the given natural language query.

You should return the output in the following json schema:
{
    "query": string represents the SQL query you have generated.
    "query_type": string represents the query type (SELECT, UPDATE, etc.)
    "tables_used": a list of the names of the tables used
}

---

Example:
Natural Language Query: Find all users that have not opened the application in the last 30 days.

Response:
{
    "query": "SELECT * FROM users WHERE was_active_since > 30",
    "query_type": "SELECT",
    "tables_used": ["users"]
}

---

Natural Language Query:
Response:
```

---

## Parsing and Validation Pipeline

Each model response passes through the following pipeline:

```text
Raw model response
→ json.loads(...)
→ Pydantic model_validate(...)
→ valid structured object
```

If direct parsing or validation fails, the app applies a fallback cleaning strategy.

---

## Fallback Strategy

The app includes a fallback function to remove common noise from model outputs before retrying validation.

The fallback removes:

| Noise Type | Example |
|---|---|
| Thinking tags | `<think>...</think>` |
| Markdown fences | ```json and ``` |
| Extra wrapper text | Cleaned before retrying JSON parsing |

The fallback function targets tags such as:

```text
<think>
...
</think>
```

and removes them before retrying JSON parsing and Pydantic validation.

---

## Evaluation Metrics

Each model is evaluated by counting how many responses fail schema validation.

| Metric | Meaning |
|---|---|
| `N_Errors` | Number of outputs that failed JSON parsing or Pydantic validation |
| `valid_schema` | Whether the original model output was directly valid without fallback |
| `success` | Whether parsing and validation eventually succeeded |
| `model_output` | The parsed and validated SQL response |
| `error` | The parsing or validation error when validation fails |

The main success condition is:

```text
The model response must be parseable JSON and must pass SQLQueryGenerationSchema validation.
```

---

## Results

The following table shows the evaluation results using:

```text
temperature = 0
max_tokens = 512
number of samples = 20
```

| Test # | Model | Response Mode | Samples | Schema Errors |
|---:|---|---|---:|---:|
| 1 | `llama-3.1-8b-instant` | `json_object` | 20 | 0 |
| 2 | `llama-3.3-70b-versatile` | `json_object` | 20 | 0 |
| 3 | `meta-llama/llama-4-scout-17b-16e-instruct` | `json_schema` best-effort | 20 | 0 |

---

## Results Summary

| Model | Schema Errors | Validation Result | Notes |
|---|---:|---|---|
| `llama-3.1-8b-instant` | 0 | Passed | Returned valid structured outputs across all samples. |
| `llama-3.3-70b-versatile` | 0 | Passed | Returned valid structured outputs across all samples. |
| `meta-llama/llama-4-scout-17b-16e-instruct` | 0 | Passed | Successfully followed the JSON schema response format. |

---

## Key Observations

- All tested models returned outputs that passed the required schema validation.
- The app successfully combined provider-level response formatting with application-level Pydantic validation.
- `json_object` mode was enough for the Llama 3.1 8B and Llama 3.3 70B models in this experiment.
- The Scout model used the JSON schema response format and also produced valid outputs.
- Pydantic validation provides an important safety layer even when the provider supports structured output.
- `extra="forbid"` is important because it prevents the app from silently accepting unexpected fields.
- Using `Literal` for `query_type` allows the app to enforce strict enum values.
- The fallback parser is useful for production robustness, even though no schema errors occurred in this final run.

---

## Error Handling

When validation fails, the app logs:

```text
Pydantic Validation Error
```

Then it writes the detailed validation errors returned by Pydantic.

The app also logs the raw model output so the failure can be inspected later.

This allows the system to fail safely instead of crashing silently or accepting malformed data.

---

## Error Analysis Example

A common structured-output failure would be an invalid enum value.

Example invalid output:

```json
{
  "query": "SELECT * FROM users",
  "query_type": "READ",
  "tables_used": ["users"]
}
```

This fails because `READ` is not one of the allowed values:

```text
SELECT
INSERT
UPDATE
DELETE
AGGREGATE
JOIN
SUBQUERY
OTHER
```

Another possible failure is an extra unexpected field:

```json
{
  "query": "SELECT * FROM users",
  "query_type": "SELECT",
  "tables_used": ["users"],
  "confidence": "high"
}
```

This fails because the schema uses:

```python
extra="forbid"
```

So the app rejects fields that are not part of the contract.

---

## Conclusion

This experiment shows how structured output and schema enforcement can make LLM responses safer for real applications.

The system does not rely only on prompting. It combines:

- provider-level response formatting
- strict Pydantic schema validation
- enum enforcement
- extra-field rejection
- fallback parsing
- validation-error logging

All tested models completed the 20-query SQL-generation dataset with zero schema errors.

This confirms that the structured output pipeline is working correctly for the tested models and that the app can safely convert raw LLM responses into validated Python objects before using them.
