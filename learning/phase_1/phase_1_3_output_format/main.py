
import re
import os
import json
from io import TextIOWrapper

import helpers.functional as F
import helpers.config as CFG
from helpers.logging import write_in_file, TEXT_ERROR, TEXT_LIST, TEXT_DICT, TEXT_SUBTITLE, TEXT_NORMAL


from core.groq_client       import GroqModelsAPI
from core.prompts           import get_prompt
from core.response_formats  import get_response_format
from core.schemas           import SQLQueryGenerationSchema

from pydantic import ValidationError


def print_sep(file_to_log, n_dashes: int = 3) -> None:
    write_in_file(file_to_log, "")
    write_in_file(file_to_log, "")
    write_in_file(file_to_log, "-" * n_dashes, TEXT_NORMAL)
    write_in_file(file_to_log, "")
    write_in_file(file_to_log, "")


def remove_text_noise(text: str, tags_text: list[str]) -> str:
    # tags
    for tag_text in tags_text:
        tag_text = re.escape(tag_text)
        text = re.sub(
            pattern = rf"<{tag_text}[^>]*>.*?</{tag_text}\s*>",
            repl = "",
            string = text,
            flags = re.DOTALL
        )

    # markdown
    text = re.sub(
        pattern = r"```(?:json)?",
        repl = "",
        string = text,
        flags = re.IGNORECASE
    )

    return text

def parse_model_output(model_response: str) -> dict:
    """
    Parsing the model output:
        - if the model returned the json schema correctly --> return the schema
        - if the model returned a json object correctly ----> return the object
        - if not ---> try to remove any existing noise | tags | fences | ...
        - if neither works ---> returns an error
    """

    try:
        sql_query_generation = SQLQueryGenerationSchema.model_validate(
            json.loads(model_response)
        )

    except (ValidationError, json.JSONDecodeError) as e:
        return {
            "success"     : False,
            "model_output": None,
            "error"       : e
        }
    
    sql_query_generation_parsed = sql_query_generation.model_dump()
    

    return {
        "success"     : True,
        "model_output": sql_query_generation_parsed,
        "error"       : None
    }
    
        




def run_experiment(
    file_to_log    : TextIOWrapper,
    groq_client    : GroqModelsAPI,
    query          : str,
    model_name     : str,
    tags_to_remove : list[str],
    **kwargs
) -> bool:
    """Runs an experiment & returns True if success"""

    response_format = get_response_format(model_name)
    prompt_name, prompt_text = get_prompt(query = query, response_format_type = response_format["type"])

    model_response = groq_client.generate(
        model_name      = model_name,
        user_input      = query,
        system_prompt   = prompt_text,
        response_format = response_format,
        **kwargs
    )

    parsed = parse_model_output(model_response)
    validation_err = parsed["error"]
    
    if parsed["success"]:
        results = {
            "user_query"  : query,
            "model_name"  : model_name,
            "prompt_ver"  : prompt_name,
            "results"     : parsed,
            "valid_schema": True # whether the model outputted a valid schema or not
        }

        write_in_file(
            file_to_log,
            text = results,
            type = TEXT_DICT
        )

        return True
    

    parsed = parse_model_output(remove_text_noise(model_response, tags_to_remove))
    if parsed["success"]:
        results = {
            "user_query"  : query,
            "model_name"  : model_name,
            "prompt_ver"  : prompt_name,
            "model_op"    : parsed,
            "valid_schema": False # whether the model outputted a valid schema or not
        }

        write_in_file(
            file_to_log,
            text = results,
            type = TEXT_DICT
        )

        return True



    write_in_file(
        file_to_log,
        "Pydantic Validation Error",
        TEXT_ERROR
    )

    write_in_file(
        file_to_log,
        validation_err.errors(),
        TEXT_LIST
    )

    write_in_file(
        file_to_log,
        f"\n\nModel Output: {model_response}\n",
        TEXT_NORMAL
    )

    return False
    


        
        





ASSETS_PATH = "/mnt/d/Focus/_____Active_______/__Agentic_AI/Agentic_AI/learning/phase_1/phase_1_3_output_format/assets"
if __name__ == "__main__":
    # --------------------- Init ----------------------- #
    F.print_title("Starting the APP")

    F.print_subtitle("Loading Files")
    try:
        output_file_path = os.path.join(ASSETS_PATH, "output.txt")
        output_file = open(file = output_file_path, mode = "w", encoding = "utf-8")
    except FileNotFoundError as e:
        F.print_error(e, "File Not Found")
        exit()

    try:
        data_file_path = os.path.join(ASSETS_PATH, "samples.json")
        samples = F.load_json(data_file_path)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        F.print_error(e, "File Not Found")
        exit()


    F.print_subtitle("Initiating Client & CFG")
    F.print_success_message("See the assets/output.txt for logging...")

    settings = CFG.get_settings()
    models_cfg = {
        "temperature": 0,
        "max_tokens": 512
    }
    
    groq_models_client = GroqModelsAPI(settings.GROQ_API_KEY)


    models_to_test = [
        # CFG.GROQ_GPT_20b,
        CFG.GROQ_LLAMA_8b,
        CFG.GROQ_LLAMA_70b,
        CFG.GROQ_LLAMA_SCOUT
    ]

    # ------------ Run experiments -------------- #
    model_errors = {}  # record how often a model violates the required schema
    for model in models_to_test:
        write_in_file(output_file, f"Testing {{{model}}}", TEXT_SUBTITLE)
        F.print_subtitle(f"Testing {{{model}}}")

        n_errors = 0
        for idx, sample in enumerate(samples, start = 1):
            print(f">> Sample #{idx}")
            write_in_file(output_file, f">> Sample #{idx}", TEXT_NORMAL)


            query = sample['query']
            success = run_experiment(
                file_to_log    = output_file,
                groq_client    = groq_models_client,
                query          = query,
                model_name     = model,
                tags_to_remove = ["think"]
            )

            if not success:
                n_errors += 1
        

        model_errors[model] = n_errors
        print_sep(output_file)
    # ---------------- Model results ----------- #
    print_sep(output_file, 10)


    write_in_file(output_file, "Final Results", TEXT_SUBTITLE)
    write_in_file(output_file, "Model => N_Errors", TEXT_NORMAL, 1)
    write_in_file(output_file, model_errors, TEXT_DICT, 1)



    output_file.close()