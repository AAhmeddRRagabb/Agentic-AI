# -----------------------------------
# Main Driver File
# -----------------------------------
import json
from pathlib import Path

from typing import Any
from pydantic import ValidationError

from helpers.settings import get_settings
from helpers.functional import load_json_file, reset_json_file, append_json_result, log_message

from llms_core.schemas              import SQLQueryGenerationSchema
from llms_core.groq.config import (
    PROVIDER_GROQ, 
    GROQ_LLAMA_8b,
    GROQ_LLAMA_70b,
    GROQ_QWEN_32b,
    GROQ_GPT_120b
)

from llms_core.groq.response_format import get_response_format
from llms_core.groq.prompts         import get_prompt



from agents import LLMAgent



# CFG
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "assets" / "samples.json"
OUTPUT_PATH = BASE_DIR / "assets" / "output"
LOG_PATH = BASE_DIR / "assets" / "logs.txt"


MODELS_TO_TEST = [
    GROQ_LLAMA_8b,
    GROQ_QWEN_32b,
    GROQ_GPT_120b,
    GROQ_LLAMA_70b,
]



# Func
# -- running
def run_experiment(
    sample: dict[str, Any],
    agent : LLMAgent
):
    """Running the experiment & Returning results"""
    # get data
    sample_id = sample["id"]
    sample_query = sample["query"]
    sample_complexity = sample["complexity"]

    

    # invoke
    results = agent(
        query = sample_query,
        round_number = 1
    )

    if results["validated"]:
        return {
            "validated"          : True,
            "sample_id"          : sample_id,
            "sample_query"       : sample_query,
            "sample_complexity"  : sample_complexity,
            "sql_query"          : results["sql_query"],
            "required_query_type": results["required_query_type"],
            "tables_used"        : results["tables_used"]
        }
    

    return {
        "validated"          : False,
        "sample_id"          : sample_id,
        "sample_query"       : sample_query,
        "sample_complexity"  : sample_complexity,
        "violation"          : results["violation"]
    }




# -- scores
def calc_tables_used_score(true_tables_used: list[str], pred_tables_used: list[str]) -> float:
    if true_tables_used is None and pred_tables_used is None:
        return 1.0

    if true_tables_used is None or pred_tables_used is None:
        return 0.0
    
    if len(true_tables_used) == 0 and len(pred_tables_used) == 0:
        return 1.0

    if len(true_tables_used) == 0:
        return 0.0


    true_tables_used = set([table.lower() for table in true_tables_used])
    pred_tables_used = set([table.lower() for table in pred_tables_used])

    return 1.0 if pred_tables_used == true_tables_used else 0.0


def calc_query_type_score(true_query_type: str | None, pred_query_type: str | None) -> float:
    if true_query_type is None and pred_query_type is None:
        return 1.0
    
    if true_query_type is None or pred_query_type is None:
        return 0.0

    if true_query_type.lower() == pred_query_type.lower():
        return 1.0
    
    return 0.0



if __name__ == "__main__":
    system_settings = get_settings()
    print(">> see the results in assets/output")

    # load data & files
    try:
        data_samples = load_json_file(DATA_PATH)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise e
    
    try:
        log_file = open(LOG_PATH, mode = "w")
    except FileNotFoundError as e:
        raise e
    
    # init & cfg
    model_cfg = {
        'temperature': 0.0,
        "max_tokens" : 1024
    }

    # ---------------------- Main Workflow ------------------------- #
    model_scores = {}
    
    for model in MODELS_TO_TEST:
        # init
        log_message(log_file, f">>>>>>> Testing {model} <<<<<<<")
        response_format = get_response_format(model, SQLQueryGenerationSchema)
        system_prompt = get_prompt(response_format_type = response_format)
        model_scores[model] = {
            "query_type_score"   : [],
            "tables_used_score"  : [],
            "number_of_validated": []
        }

        agent = LLMAgent(
            model_provider   = PROVIDER_GROQ,
            provider_api_key = system_settings.GROQ_API_KEY,
            model_name       = model,
            system_prompt    = system_prompt,
            response_format  = response_format,
            output_schema    = SQLQueryGenerationSchema,
            log_file         = log_file,
            **model_cfg
        )


        model_name = model.replace("/", "_")
        file_path = OUTPUT_PATH / f"{model_name}.json"
        reset_json_file(file_path = file_path)

    

        # running
        for sample_idx, sample in enumerate(data_samples, start = 1):
            log_message(log_file, f">>> Sample #{sample_idx}")

            # run on a sample
            sample_outputs = run_experiment(
                sample = sample,
                agent  = agent
            )

            # evaluate
            if sample_outputs["validated"]:
                model_scores[model]["query_type_score"].append(
                    calc_query_type_score(
                        true_query_type = sample["required_query_type"],
                        pred_query_type = sample_outputs["required_query_type"]
                    )
                )

                model_scores[model]["tables_used_score"].append(
                    calc_tables_used_score(
                        true_tables_used = sample["tables_used"],
                        pred_tables_used = sample_outputs["tables_used"],
                    )
                )

                model_scores[model]['number_of_validated'].append(1.0)

            else:
                model_scores[model]["query_type_score"].append(0.0)
                model_scores[model]["tables_used_score"].append(0.0)
                model_scores[model]["number_of_validated"].append(0.0)



            # append detailed outputs in JSON
            append_json_result(file_path, sample_outputs)

            # output displayed
            if sample_outputs["validated"]:
                log_message(log_file, f">> Sql Query: {sample_outputs['sql_query']}", n_identation = 1)
                log_message(log_file, f">> NL Query : {sample_outputs['sample_query']}", n_identation = 1)

            # considered as default output
            else:
                log_message(log_file, f">> Please, write a more clear & detailed nautral language (NL) query.", n_identation = 1)


            log_message(log_file, "")
            log_message(log_file, "------")
            log_message(log_file, "")
            


        model_scores[model] = {
            "query_type_score"   : sum(model_scores[model]["query_type_score"]) / len(model_scores[model]["query_type_score"]),
            "tables_used_score"  : sum(model_scores[model]["tables_used_score"]) / len(model_scores[model]["tables_used_score"]),
            "validation_score": sum(model_scores[model]["number_of_validated"]) / len(model_scores[model]["number_of_validated"]),
        }


    log_message(log_file, "")
    log_message(log_file, "")
    log_message(log_file, "------------------")
    log_message(log_file, "")
    log_message(log_file, "")

    # ---- final evaluation results
    for model, scores in model_scores.items():
        log_message(log_file, f">>> Model: {model} <<<")

        for score_name, score_value in scores.items():
            log_message(log_file, f"\t>> {score_name} ==> {score_value}", n_identation = 1)
        
        log_message(log_file, "")
        log_message(log_file, "")

    print()
    print("Finished - Alhamdulillah")
    print()




        