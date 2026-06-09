# Sentiment Analysis with Prompt Engineering

This project demonstrates how different prompt engineering techniques affect LLM responses in a sentiment analysis task.

The app uses the `llama-3.1-8b-instant` model from Groq to classify movie-streaming platform user reviews into one of three sentiments:

- `positive`
- `neutral`
- `negative`

The goal is to compare how prompt clarity, structure, constraints, and examples improve the consistency of model outputs.

---

## Objective

Evaluate the effect of different prompt styles on sentiment classification accuracy and output consistency.

The tested prompt types are:

1. Generic Prompt
2. Structured Prompt
3. Constraint Prompt
4. One-Shot Prompt
5. Few-Shot Prompt

---

## Task Description

Given a user review about a movie, the model should classify the sentiment as:

| Sentiment | Meaning |
|---|---|
| `positive` | The review expresses a good opinion about the movie |
| `negative` | The review expresses a bad opinion about the movie |
| `neutral` | The review is mixed, moderate, or neither clearly positive nor negative |

---

## Prompts Used

### 1. Generic Prompt
```text
Classify the given user review:
```

### Structured Output
```text
We are working on a movie-streaming platform, where people can comment on these movies explaining their opinion.
We need to analyze the user comments (reviews). Your role is to accomplish that task.

Classify the review: 
```

### Constraint Prompt
```text
We are working on a movie-streaming platform, where people can comment on these movies explaining their opinion.
We need to analyze the user comments (reviews). Your role is to accomplish that task.
Return only:
- positive: if the review is good.
- negative: if the review is bad.
- neutral: if neither good or bad.

Rules
- You should only return one word, either positive, negative, or neutral depending on your analysis of the review.

Classify the review: 
```


### One Shot Example Prompt
```text
We are working on a movie-streaming platform, where people can comment on these movies explaining their opinion.
We need to analyze the user comments (reviews). Your role is to accomplish that task.
Return only:
- positive: if the review is good.
- ngative: if the review is bad.
- neutral: if neither good or bad.

Rules
- You should only return one word, either positive, negative, or neutral depending on your analysis of the review.

Example
- Classify this review: This is a very interesting movie, it shows very strong drama scenes with good action moments.
  Classification: positive 

Classify the review: 
```


### Few Shot Examples Prompt
```text
We are working on a movie-streaming platform, where people can comment on these movies explaining their opinion.
We need to analyze the user comments (reviews). Your role is to accomplish that task.
Return only:
- positive: if the review is good.
- ngative: if the review is bad.
- neutral: if neither good or bad.

Rules
- You should only return one word, either positive, negative, or neutral depending on your analysis of the review.

Examples
- Classify this review: This is a very interesting movie, it shows very strong drama scenes with good action moments.
  Classification: positive 

- Classify this review: A very bad movie, no centralized story & very random scenes.
  Classification: negative

- Classify this review: A moderate movie. Has good scenes but could better.
  Classification: neutral

Classify the review: 
```

## Results

The following table shows the evaluation results for the `llama-3.1-8b-instant` model across different prompt types, temperatures, and maximum token limits.

| Test # | Model | Prompt | Temperature | Max Tokens | Score |
|---:|---|---|---:|---:|---:|
| 1 | `llama-3.1-8b-instant` | `generic_prompt` | 0 | 1 | 0.0 |
| 2 | `llama-3.1-8b-instant` | `generic_prompt` | 0 | 512 | 0.0 |
| 3 | `llama-3.1-8b-instant` | `generic_prompt` | 0.2 | 1 | 0.0 |
| 4 | `llama-3.1-8b-instant` | `generic_prompt` | 0.2 | 512 | 0.0 |
| 5 | `llama-3.1-8b-instant` | `structured_prompt` | 0 | 1 | 0.0 |
| 6 | `llama-3.1-8b-instant` | `structured_prompt` | 0 | 512 | 0.0 |
| 7 | `llama-3.1-8b-instant` | `structured_prompt` | 0.2 | 1 | 0.0 |
| 8 | `llama-3.1-8b-instant` | `structured_prompt` | 0.2 | 512 | 0.0 |
| 9 | `llama-3.1-8b-instant` | `constraint_prompt` | 0 | 1 | 1.0 |
| 10 | `llama-3.1-8b-instant` | `constraint_prompt` | 0 | 512 | 1.0 |
| 11 | `llama-3.1-8b-instant` | `constraint_prompt` | 0.2 | 1 | 1.0 |
| 12 | `llama-3.1-8b-instant` | `constraint_prompt` | 0.2 | 512 | 1.0 |
| 13 | `llama-3.1-8b-instant` | `one_shot_example` | 0 | 1 | 0.9 |
| 14 | `llama-3.1-8b-instant` | `one_shot_example` | 0 | 512 | 0.9 |
| 15 | `llama-3.1-8b-instant` | `one_shot_example` | 0.2 | 1 | 0.9 |
| 16 | `llama-3.1-8b-instant` | `one_shot_example` | 0.2 | 512 | 0.9 |
| 17 | `llama-3.1-8b-instant` | `few_shot_examples` | 0 | 1 | 1.0 |
| 18 | `llama-3.1-8b-instant` | `few_shot_examples` | 0 | 512 | 1.0 |
| 19 | `llama-3.1-8b-instant` | `few_shot_examples` | 0.2 | 1 | 1.0 |
| 20 | `llama-3.1-8b-instant` | `few_shot_examples` | 0.2 | 512 | 1.0 |

---

## Results Summary

| Prompt Type | Best Score | Notes |
|---|---:|---|
| `generic_prompt` | 0.0 | Failed to produce directly comparable sentiment labels. |
| `structured_prompt` | 0.0 | Added context but did not enforce a strict output format. |
| `constraint_prompt` | 1.0 | Best-performing prompt. Clear labels and strict output rules improved consistency. |
| `one_shot_example` | 0.9 | Strong performance, but one sample was misclassified. |
| `few_shot_examples` | 1.0 | Best-performing prompt. Examples helped the model follow the expected classification pattern. |

---

## Key Observations

- The `generic_prompt` and `structured_prompt` scored `0.0` because they did not strictly force the model to return one of the expected labels.
- The `constraint_prompt` achieved `1.0`, showing that clear output constraints are highly effective for classification tasks.
- The `one_shot_example` achieved `0.9`, showing that a single example improves model behavior but may still be less reliable than stronger constraints or multiple examples.
- The `few_shot_examples` achieved `1.0`, showing that multiple examples can improve output consistency and task understanding.
- Changing `temperature` from `0` to `0.2` did not affect the score in this experiment.
- Changing `max_tokens` from `1` to `512` did not affect the score for well-constrained prompts.