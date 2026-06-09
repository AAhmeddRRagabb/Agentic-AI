# ------------------
# Main Driver
# ------------------

from helpers.config import get_settings
from helpers.config import GROQ_LLAMA_8b, GEMINI_FLASH_LITE
from helpers.config import PROVIDER_GROQ, PROVIDER_GOOGLE_GENAI

import helpers.functional as F

from core.generation import generate, stream
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

    F.print_subtitle(f"Testing Model: {model_name} | Prompt: {prompt_name}")
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
        ).lower()

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
    F.print_success_message(f"Combination Score => Model: {model_name} | Prompt: {prompt_name} | Score: {final_score}")
    print()
    print()

    return {
        "model_name": model_name,
        "prompt"    : prompt_name,
        "score"     : final_score
    }


    



if __name__ == "__main__":
    F.print_title("Starting the APP")
    
    F.print_subtitle("Setup the System")
    settings       = get_settings()
    groq_api_Key   = settings.GROQ_API_KEY
    gooqle_api_Key = settings.GOOGLE_API_KEY
    try:
        sentiment_analysis_data = F.load_json("movie_sentiment_samples.json")
    except FileNotFoundError:
        print("File Not Found")
        exit()

    groq_kwargs = {
        "temperature": 0.4,
        "max_tokens" : 1,
        "top_p"      : 0.9
    }

    google_kwargs = {
        "temperature"        : 0.4,
        "max_output_tokens"  : 1,
        "top_p"              : 0.9
    }

    
    print()
    print()

    
    # llama 8b
    scores = []
    try:
        for prompt in SENTIMENT_ANALYSIS_PROMPTS:
            scores.append(
                calc_model_score_with_prompt(
                    provider     = PROVIDER_GROQ,
                    api_key      = groq_api_Key,
                    model_name   = GROQ_LLAMA_8b,
                    test_samples = sentiment_analysis_data,
                    prompt       = prompt,
                    **groq_kwargs
                )
            )
    except Exception as e:
        F.print_error(e, "Error from LLAMA_8B")

    print(100 * '-')

    # generate
    try:
        for prompt in SENTIMENT_ANALYSIS_PROMPTS:
            scores.append(
                calc_model_score_with_prompt(
                    provider     = PROVIDER_GOOGLE_GENAI,
                    api_key      = gooqle_api_Key,
                    model_name   = GEMINI_FLASH_LITE,
                    test_samples = sentiment_analysis_data,
                    prompt       = prompt,
                    **google_kwargs
                )
            )
    except Exception as e:
        F.print_error(e, "Error from Gemini")


    print()
    print()
    for score in scores:
        print(f">> Model: {score['model_name']} | Prompt: {score['prompt']} | Score: {score['score']}")


    
    
