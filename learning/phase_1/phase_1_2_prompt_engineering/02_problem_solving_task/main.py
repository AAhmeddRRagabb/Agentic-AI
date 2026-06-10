# ------------------
# Main Driver
# ------------------
import os


from helpers.logging import write_in_file
from helpers.logging import (
    TEXT_TITLE,
    TEXT_ERROR
)


import helpers.functional as F

from helpers.config import get_settings
from helpers.config import GROQ_QWEN_32b, GROQ_LLAMA_8b
from helpers.config import PROVIDER_GROQ

from core.problem_solving_pipeline import calc_model_score_with_prompt



DATA_PATH = "/mnt/d/Focus/_____Active_______/__Agentic_AI/Agentic_AI/learning/phase_1/phase_1_2_prompt_engineering/02_problem_solving_task/data"



if __name__ == "__main__":
    F.print_title("Starting the APP")
    
    F.print_subtitle("Setup the System")
    settings       = get_settings()
    groq_api_Key   = settings.GROQ_API_KEY
    gooqle_api_Key = settings.GOOGLE_API_KEY
    try:
        file_path = os.path.join(DATA_PATH, "problem_solving_examples.json")
        sentiment_analysis_data = F.load_json(file_path)
    except FileNotFoundError:
        print("File Not Found")
        print(f"File Path: {file_path}")
        exit()

    try:
        output_file_path = os.path.join(DATA_PATH, "output_file.txt")
        output_file = open(output_file_path, "w", encoding = "utf-8")
    except FileNotFoundError as e:
        print("File Not Found")
        print(f"File Path: {file_path}")
        exit()
        
    F.print_subtitle("See the results in data/output_file.txt")

    
    write_in_file(output_file, "Starting the APP", TEXT_TITLE)
    write_in_file(output_file, "")

    
    # llama 8b
    # temperatures = [0, 0.2, 0.3]
    temperatures = [0]
    # max_tokens_s   = [256, 512]
    max_tokens_s   = [256]
    results = []
    problem_versions = ["v1", "v2", 'one_shot']
    try:
        for prompt_version in problem_versions:
            for temperature in temperatures:
                for max_tokens in max_tokens_s:
                    kwargs = {
                        "temperature": temperature,
                        "max_tokens" : max_tokens
                    }
                    results.append(
                        calc_model_score_with_prompt(
                            provider       = PROVIDER_GROQ,
                            api_key        = groq_api_Key,
                            model_name     = GROQ_LLAMA_8b,
                            test_samples   = sentiment_analysis_data,
                            prompt_version = prompt_version,
                            file_to_log    = output_file,
                            **kwargs
                        )
                    )
    except Exception as e:
        write_in_file(output_file, f"Error: {e}", type = TEXT_ERROR)

    print(100 * '-')
    try:
        for prompt_version in problem_versions:
            for temperature in temperatures:
                for max_tokens in max_tokens_s:
                    kwargs = {
                        "temperature": temperature,
                        "max_tokens" : max_tokens
                    }
                    results.append(
                        calc_model_score_with_prompt(
                            provider       = PROVIDER_GROQ,
                            api_key        = groq_api_Key,
                            model_name     = GROQ_QWEN_32b,
                            test_samples   = sentiment_analysis_data,
                            prompt_version = prompt_version,
                            file_to_log    = output_file,
                            **kwargs
                        )
                    )
    except Exception as e:
        write_in_file(output_file, f"Error: {e}", type = TEXT_ERROR)

   

    print("Results:")
    print()
    for idx, result in enumerate(results, start = 1):
        print(f">> Test #{idx}")
        F.print_dict(result, n_identation = 0)

        print()
        print("---")
        print()


    
    
