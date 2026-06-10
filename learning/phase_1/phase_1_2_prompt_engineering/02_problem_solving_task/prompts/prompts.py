# --------------------------------------------
# Test a bunch of prompts
# --------------------------------------------


def get_prompt_v1(problem: str) -> str:
    prompt = f"""
You are a problem solving assitant for simple real-word math problems.
Solve the given problem & return only a valid json schema

Required json schema:
{{
  "answer": number
  "unit": str,
  "solving_steps": list[str]
}}

Rules
- return only a valid json schema


Solve the following problem: {problem}\n\n
Solution:
"""
    return prompt


def get_prompt_v2(problem: str) -> str:
    prompt = f"""
You are a problem solving assitant for simple real-word math problems.
Solve the given problem & return only a valid json schema

Required json schema:
{{
  "answer": number,
  "unit": str,
  "solving_steps": list[str]
}}

Rules
- Return only a valid json schema.
- Do not include <think> tags in your response. Return the json schema directly.
- In units, use the word `percent` for percentages, not `%`.


Solve the following problem: {problem}\n\n
Solution:
"""
    return prompt


def get_one_shot_example_prompt(problem: str) -> str:
  prompt = f"""
You are a problem solving assitant for simple real-word math problems.
Solve the given problem & return only a valid json schema

Required json schema:
{{
  "answer": number,
  "unit": str,
  "solving_steps": list[str]
}}

Rules
- Return only a valid json schema.
- Do not include <think> tags in your response. Return the json schema directly.
- In units, use the word `percent` for percentages, not `%`.


Examples:
Solve the following problem: Sara has 30 pounds. Her brother gives her another 5 pounds. She wanted to buy a meal that costs 38 pounds. How many pounds does Sara still need?
Solution: 
{{
  "answer": 3,
  "unit": "pounds",
  "solving_steps": ["Sara first has 30 pounds.", "Her brother gives her 5, she now has 30 + 5 = 35 pounds.", "The meal costs 38, Sara needs 38 - 35 = 3 pounds."]
}}

Solve the following problem: {problem}\n\n
Solution:
"""
  return prompt

def get_prompt(problem: str, version_needed: str) -> str:
    if version_needed == "v1":
      return ("prompt_v1", get_prompt_v1(problem))
    
    if version_needed == "v2":
       return ("prompt_v2", get_prompt_v2(problem))
    
    if version_needed == "one_shot":
      return ("one_shot", get_one_shot_example_prompt(problem))

    raise ValueError(f"Prompt version: {version_needed} is not valid")
  
