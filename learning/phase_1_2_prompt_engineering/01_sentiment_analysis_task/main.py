# ------------------
# Main Driver
# ------------------
import os

from helpers.config import get_settings
from helpers.config import GROQ_LLAMA_8b
from helpers.config import PROVIDER_GROQ

import helpers.functional as F

from core.generation import generate
from prompts         import SENTIMENT_ANALYSIS_PROMPTS




def calc_model_score_with_prompt(
    provider       : str,
    api_key        : str,
    model_name     : str,
    test_samples   : dict[str, int | str],
    prompt         : dict[str, str],
    **kwargs
) -> dict[str, str | float]:
    """
    Test the given model with prompt
    
    Returns:
        score: float
    """
    prompt_name, prompt_text = prompt
    score = 0.0

    F.print_subtitle(f"Testing Model: {model_name} | Prompt: {prompt_name} | CFG: {kwargs}")
    for idx, sample in enumerate(test_samples, start = 1):
        print(f">> Sample #{idx}")

        review = sample.get("review")
        true_sentiment = sample.get("sentiment")

        # prediction
        pred_sentiment = generate(
            provider      = provider,
            api_key       = api_key,
            model_name    = model_name,
            system_prompt = prompt_text,
            user_input    = review,
            **kwargs
        ).lower().strip()

        if true_sentiment == pred_sentiment:
            score += 1



        print(f"\t>> Review:\n{review}\n")
        print(f"\t>> Actual Sentiment   : {true_sentiment}")
        print(f"\t>> Predicted Sentiment: {pred_sentiment}")

        print()
        print()
        print("---")
        print()
        print()

    final_score = round(score / len(test_samples), 3)
    F.print_success_message(f"Combination Score => Model: {model_name} | Prompt: {prompt_name} | Score: {final_score} | CFG: {kwargs}")
    print()
    print()

    return {
        "model_name" : model_name,
        "prompt"     : prompt_name,
        "score"      : final_score,
        "temperature": kwargs['temperature'],
        "max_tokens" : kwargs['max_tokens'],
    }


    

DATA_PATH = "/mnt/d/Focus/_____Active_______/__Agentic_AI/Agentic_AI/learning/phase_1_2_prompt_engineering/01_sentiment_analysis_task/data"


if __name__ == "__main__":
    F.print_title("Starting the APP")
    
    F.print_subtitle("Setup the System")
    settings       = get_settings()
    groq_api_Key   = settings.GROQ_API_KEY
    gooqle_api_Key = settings.GOOGLE_API_KEY
    try:
        file_path = os.path.join(DATA_PATH, "movie_sentiment_samples.json")
        sentiment_analysis_data = F.load_json(file_path)
    except FileNotFoundError:
        print("File Not Found")
        exit()

    
    print()
    print()

    
    # llama 8b
    temperatures = [0, 0.2]
    max_tokens_s   = [1, 512]
    scores = []
    try:
        for prompt in SENTIMENT_ANALYSIS_PROMPTS:
            for temperature in temperatures:
                for max_tokens in max_tokens_s:
                    kwargs = {
                        "temperature": temperature,
                        "max_tokens" : max_tokens
                    }
                    scores.append(
                        calc_model_score_with_prompt(
                            provider     = PROVIDER_GROQ,
                            api_key      = groq_api_Key,
                            model_name   = GROQ_LLAMA_8b,
                            test_samples = sentiment_analysis_data,
                            prompt       = prompt,
                            **kwargs
                        )
                    )
    except Exception as e:
        F.print_error(e, "Error from LLAMA_8B")

    print(100 * '-')

   


    print()
    print()
    print("Score:")
    print()
    for idx, score in enumerate(scores, start = 1):
        print(f">> Test #{idx}")
        print(f"\t- Model        => {score['model_name']}")
        print(f"\t- Prompt       => {score['prompt']}")
        print(f"\t- Temperature  => {score['temperature']}")
        print(f"\t- Max Tokens   => {score['max_tokens']}")
        print(f"\t- Score        => {score['score']}")

        print()
        print("---")
        print()


    
    
