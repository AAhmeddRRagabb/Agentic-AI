# --------------------------------------------
# Test a bunch of prompts
# --------------------------------------------



GENERIC_PROMPT = """Classify the given user review:"""


STRUCTURED_PROMPT = """We are working on a movie-streaming platform, where people can comment on these movies explaining their opinion.
We need to analyze the user comments (reviews). Your role is to accomplish that task.

Classify the review: 
"""


CONSTRAINT_PROMPT = """We are working on a movie-streaming platform, where people can comment on these movies explaining their opinion.
We need to analyze the user comments (reviews). Your role is to accomplish that task.
Return only:
- positive: if the review is good.
- negative: if the review is bad.
- neutral: if neither good or bad.

Rules
- You should only return one word, either positive, negatice, or neutral depending on your analysis of the review.

Classify the review: 
"""



ONE_SHOT_EXAMPLE_PROMPT = """We are working on a movie-streaming platform, where people can comment on these movies explaining their opinion.
We need to analyze the user comments (reviews). Your role is to accomplish that task.
Return only:
- positive: if the review is good.
- ngative: if the review is bad.
- neutral: if neither good or bad.

Rules
- You should only return one word, either positive, negatice, or neutral depending on your analysis of the review.

Examples
- Classify this review: This is a very interesting movie, it shows very strong drama scenes with good action moments.
  Classification: positive 

Classify the review: 
"""

FEW_SHOT_EXAMPLES_PROMPT = """We are working on a movie-streaming platform, where people can comment on these movies explaining their opinion.
We need to analyze the user comments (reviews). Your role is to accomplish that task.
Return only:
- positive: if the review is good.
- ngative: if the review is bad.
- neutral: if neither good or bad.

Rules
- You should only return one word, either positive, negatice, or neutral depending on your analysis of the review.

Examples
- Classify this review: This is a very interesting movie, it shows very strong drama scenes with good action moments.
  Classification: positive 

- Classify this review: A very bad movie, no centralized story & very random scenes.
  Classification: negative

- Classify this review: A moderate movie. Has good scenes but could better.
  Classification: neutral

Classify the review: 
"""


SENTIMENT_ANALYSIS_PROMPTS = [
    ("generic_prompt"    , GENERIC_PROMPT),
    ("structured_prompt" , STRUCTURED_PROMPT),
    ("constraint_prompt" , CONSTRAINT_PROMPT),
    ("one_shot_example"  , ONE_SHOT_EXAMPLE_PROMPT),
    ("few_shot_examples" , FEW_SHOT_EXAMPLES_PROMPT)
]

