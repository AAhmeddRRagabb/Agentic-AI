import json
import re
from io import TextIOWrapper

from helpers.logging import write_in_file, TEXT_ERROR, TEXT_LIST, TEXT_NORMAL, TEXT_SUBTITLE
import helpers.functional as F
from prompts import get_prompt


from .generation import generate



def parse_think_tag(model_output: str) -> str:
    return re.sub(
        pattern = r"<think>.*?</think>",
        repl = "",
        string = model_output,
        flags = re.DOTALL
    )


def calc_model_scores(actual_sample: dict[str, int | str], model_pred: dict[str, int | str], file_to_log: TextIOWrapper) -> None:
    """
    Returns:
        tuple[float, float] -> answer score & unit score
    """
    true_ans = int(actual_sample["expected_answer"])
    true_unit = str(actual_sample["unit"]).lower()

    try:
        pred_ans = int(model_pred["answer"])
    except (TypeError, ValueError) as e:
        write_in_file(file_to_log, "Model returned non-number answer", TEXT_ERROR)
        return 0, 0

    try:
        pred_unit = str(model_pred["unit"]).lower()
    except (TypeError, ValueError) as e:
        write_in_file(file_to_log, "Model returned invalid unit", TEXT_ERROR)
        return 0, 0
    

    answer_score = 1.0 if true_ans == pred_ans else 0.0
    unit_score = 1.0 if true_unit == pred_unit else 0.0

    return (answer_score, unit_score)


def print_model_output_and_actual_sample(actual_sample: dict[str, int | str], model_pred: dict[str, int | str], file_to_log: TextIOWrapper) -> None:
    problem = actual_sample["problem"]
    true_ans = actual_sample["expected_answer"]
    true_unit = actual_sample["unit"]

    pred_ans = model_pred["answer"]
    pred_unit = model_pred["unit"]
    model_reasoning_steps = model_pred["solving_steps"]


    write_in_file(
        file_to_log,
        f">> Problem:\n{problem}\n",
        type = TEXT_NORMAL
    )


    write_in_file(
        file_to_log,
        f">> Model Reasoning Steps:",
        type = TEXT_NORMAL
    )

    write_in_file(
        file_to_log,
        model_reasoning_steps,
        type = TEXT_LIST,
        n_identation = 1 
    )
    
    write_in_file(file_to_log, "")
    write_in_file(file_to_log, f">> Final Actual Result: {true_ans} {true_unit}", type = TEXT_NORMAL)
    write_in_file(file_to_log, f">> Final Model Result : {pred_ans} {pred_unit}", type = TEXT_NORMAL)



def write_sep(file_to_log):
    write_in_file(file_to_log, "")
    write_in_file(file_to_log, "")
    write_in_file(file_to_log, "-----", TEXT_NORMAL)
    write_in_file(file_to_log, "")
    write_in_file(file_to_log, "")


def calc_model_score_with_prompt(
    provider       : str,
    api_key        : str,
    model_name     : str,
    test_samples   : list[dict[str, int | str]],
    prompt_version : dict[str, str],
    file_to_log    : TextIOWrapper,
    **kwargs
) -> dict[str, str | float]:
    """
    Test the given model with prompt
    
    Returns:
        score: float
    """
    
    answer_score = 0.0
    unit_score = 0.0
    json_schema_score = 0.0
    n_times_think_appears = 0

    write_in_file(
        file_to_log, 
        text = f"Testing Combination: {model_name} | Prompt: {prompt_version} | CFG: {kwargs}",
        type = TEXT_SUBTITLE
    )

    for idx, sample in enumerate(test_samples, start = 1):
        write_in_file(
            file_to_log,
            f">> Sample #{idx}",
            type = TEXT_NORMAL
        )

        problem = sample.get("problem")
        prompt_name, prompt_text = get_prompt(problem, prompt_version)


        write_in_file(
            file_to_log,
            f">> Prompt Used:\n{prompt_text}\n",
            type = TEXT_NORMAL
        )


        # prediction
        model_pred = generate(
            provider      = provider,
            api_key       = api_key,
            model_name    = model_name,
            system_prompt = prompt_text,
            query         = problem,
            **kwargs
        ).strip()



        write_in_file(
            file_to_log,
            f">> Pure Model Output:\n{model_pred}\n",
            type = TEXT_NORMAL
        )


        # parse model op
        if "<think>" in model_pred:
            model_pred = parse_think_tag(model_pred)
            n_times_think_appears += 1

        try:
            parsed_model_output = json.loads(model_pred)
        except json.JSONDecodeError as e:
            write_in_file(file_to_log, "Model Did not return Json", TEXT_ERROR)
            write_in_file(file_to_log, f"Model Output:\n{model_pred}\n", TEXT_NORMAL)

            continue


        required_keys = {"answer", "unit", "solving_steps"}
        if required_keys.issubset(parsed_model_output):
            json_schema_score += 1

            print_model_output_and_actual_sample(sample, parsed_model_output, file_to_log)
            ans_score, u_score = calc_model_scores(sample, parsed_model_output, file_to_log)

            answer_score += ans_score
            unit_score += u_score
        
        else:
            write_in_file(file_to_log, ">> Model Returned Wrong Keys\n", TEXT_NORMAL)
            write_in_file(file_to_log, f">> Model Output:\n{parsed_model_output}", TEXT_NORMAL)

        write_sep(file_to_log)


    final_answer_score = round(answer_score / len(test_samples), 3)
    final_unit_score = round(unit_score / len(test_samples), 3)
    final_schema_score = round(json_schema_score / len(test_samples), 3)

    results = {
        "model_name"           : model_name,
        "prompt"               : prompt_name,
        "temperature"          : kwargs['temperature'],
        "max_tokens"           : kwargs['max_tokens'],
        "final_answer_score"   : final_answer_score,
        "final_unit_score"     : final_unit_score,
        "final_schema_score"   : final_schema_score,
        "n_times_think_appears": n_times_think_appears
    }


    return results
