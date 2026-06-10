# Problem Solving with Prompt Engineering

This project demonstrates how different prompt engineering techniques affect LLM responses in a real-world problem-solving task.

The app tests multiple prompts on simple reasoning-based math problems and evaluates whether the model can return the correct final answer, correct unit, and valid JSON output.

The task is designed to measure reasoning behavior, not memorization of formulas.

The app evaluates two Groq models:

- `llama-3.1-8b-instant`
- `qwen/qwen3-32b`

The goal is to compare how prompt clarity, formatting constraints, and examples affect:

- answer accuracy
- unit accuracy
- JSON schema consistency
- reasoning-step quality
- unwanted `<think>` tag behavior

---

## Objective

Evaluate the effect of different prompt styles on real-world math reasoning and structured output consistency.

The tested prompt types are:

1. Prompt V1
2. Prompt V2
3. One-Shot Prompt

---

## Task Description

Given a simple real-world math problem, the model should solve the problem and return a valid JSON object containing:

| Field | Meaning |
|---|---|
| `answer` | The final numeric answer |
| `unit` | The unit of the final answer |
| `solving_steps` | A short list of visible solving steps |

Example problem:

```text
Sara had 30 pounds. Her brother gave her another 3 pounds. After that, she bought bread for 5 pounds. How much money does Sara have now?
```

Expected output:

```json
{
  "answer": 28,
  "unit": "pounds",
  "solving_steps": [
    "Sara started with 30 pounds.",
    "Her brother gave her 3 pounds, so she had 33 pounds.",
    "She spent 5 pounds, so she has 28 pounds left."
  ]
}
```

---

## Dataset

The dataset contains 14 real-world reasoning problems.

Each sample has the following structure:

```json
{
  "problem": "A shop sells notebooks for 8 pounds each. Ali bought 3 notebooks and paid with 30 pounds. How much change should he get?",
  "expected_answer": 6,
  "unit": "pounds"
}
```

The problems include daily-life situations such as:

- buying and receiving change
- counting remaining items
- passengers entering and leaving
- battery percentage changes
- distance remaining
- total cost calculation
- dividing items equally

---

## Prompts Used

### 1. Prompt V1

```text
You are a problem solving assitant for simple real-word math problems.
Solve the given problem & return only a valid json schema

Required json schema:
{
  "answer": number
  "unit": str,
  "solving_steps": list[str]
}

Rules
- return only a valid json schema

Solve the following problem:
```

---

### 2. Prompt V2

```text
You are a problem solving assitant for simple real-word math problems.
Solve the given problem & return only a valid json schema

Required json schema:
{
  "answer": number,
  "unit": str,
  "solving_steps": list[str]
}

Rules
- Return only a valid json schema.
- Do not include <think> tags in your response. Return the json schema directly.
- In units, use the word `percent` for percentages, not `%`.

Solve the following problem:
```

---

### 3. One-Shot Prompt

```text
You are a problem solving assitant for simple real-word math problems.
Solve the given problem & return only a valid json schema

Required json schema:
{
  "answer": number,
  "unit": str,
  "solving_steps": list[str]
}

Rules
- Return only a valid json schema.
- Do not include <think> tags in your response. Return the json schema directly.
- In units, use the word `percent` for percentages, not `%`.

Examples:
Solve the following problem: Sara has 30 pounds. Her brother gives her another 5 pounds. She wanted to buy a meal that costs 38 pounds. How many pounds does Sara still need?

Solution:
{
  "answer": 3,
  "unit": "pounds",
  "solving_steps": [
    "Sara first has 30 pounds.",
    "Her brother gives her 5, she now has 30 + 5 = 35 pounds.",
    "The meal costs 38, Sara needs 38 - 35 = 3 pounds."
  ]
}

Solve the following problem:
```

---

## Evaluation Metrics

Each model/prompt combination is evaluated using three main scores.

| Metric | Meaning |
|---|---|
| `final_answer_score` | Percentage of samples where the model returned the correct numeric answer |
| `final_unit_score` | Percentage of samples where the model returned the correct unit |
| `final_schema_score` | Percentage of samples where the model returned the required JSON keys |
| `n_times_think_appears` | Number of outputs that included `<think>` reasoning tags |

The required JSON keys are:

```text
answer
unit
solving_steps
```

---

## Results

The following table shows the evaluation results using:

```text
temperature = 0
max_tokens = 256
number of samples = 14
```

| Test # | Model | Prompt | Temperature | Max Tokens | Answer Score | Unit Score | Schema Score | `<think>` Appeared |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `llama-3.1-8b-instant` | `prompt_v1` | 0 | 256 | 0.857 | 0.929 | 0.929 | 0 |
| 2 | `llama-3.1-8b-instant` | `prompt_v2` | 0 | 256 | 0.857 | 0.929 | 0.929 | 0 |
| 3 | `llama-3.1-8b-instant` | `one_shot` | 0 | 256 | 0.857 | 1.000 | 1.000 | 0 |
| 4 | `qwen/qwen3-32b` | `prompt_v1` | 0 | 256 | 0.286 | 0.286 | 0.286 | 14 |
| 5 | `qwen/qwen3-32b` | `prompt_v2` | 0 | 256 | 0.429 | 0.286 | 0.429 | 14 |
| 6 | `qwen/qwen3-32b` | `one_shot` | 0 | 256 | 0.500 | 0.500 | 0.500 | 14 |

---

## Results Summary

| Model | Best Prompt | Best Answer Score | Best Unit Score | Best Schema Score | Notes |
|---|---|---:|---:|---:|---|
| `llama-3.1-8b-instant` | `one_shot` | 0.857 | 1.000 | 1.000 | Strong performance despite being a small 8B model. |
| `qwen/qwen3-32b` | `one_shot` | 0.500 | 0.500 | 0.500 | Frequently returned `<think>` tags and sometimes failed JSON parsing. |

---

## Key Observations

- `llama-3.1-8b-instant` performed surprisingly well despite its small parameter size compared with today’s larger models.
- The one-shot prompt improved unit accuracy and JSON schema consistency for the Llama model.
- The Qwen model frequently produced `<think>` tags before the JSON output, which made parsing more difficult.
- Adding explicit instructions such as “Do not include `<think>` tags” did not fully prevent Qwen from producing them.
- The Llama model did not output `<think>` tags in this experiment.
- Some model errors were not caused by lack of reasoning, but by inconsistency between the reasoning steps and final answer.

---

## Error Analysis Example

One interesting failure happened with this problem:

```text
A shop sells notebooks for 8 pounds each. Ali bought 3 notebooks and paid with 30 pounds. How much change should he get?
```


Expected reasoning:

```text
3 notebooks × 8 pounds = 24 pounds
Ali paid 30 pounds
Change = 30 - 24 = 6 pounds
```

Expected answer:

```json
{
  "answer": 6,
  "unit": "pounds"
}
```

The model produced correct reasoning steps:

```text
Ali bought 3 notebooks for 8 pounds each, so the total cost is 3 * 8 = 24 pounds.
He paid with 30 pounds, so the change is 30 - 24 = 6 pounds.
```

But the final model result was:

```text
14 pounds
```

This shows an important reasoning failure:

```text
The model can generate correct intermediate reasoning but still output an incorrect final answer.
```

So this task is useful because it does not only test whether the model can explain the solution. It also tests whether the model can keep its final answer consistent with its own reasoning.

---

## Conclusion

This experiment shows that prompt engineering can significantly affect structured problem-solving performance.

For this task, the one-shot prompt produced the best overall results, especially for JSON schema consistency and unit accuracy.

The `llama-3.1-8b-instant` model achieved strong results despite being relatively small, making it a good practical choice for simple real-world reasoning tasks.

However, the experiment also shows that correct-looking reasoning does not always guarantee a correct final answer. Therefore, automatic evaluation should compare the final numeric answer and unit against ground truth, not rely only on the model’s explanation.
