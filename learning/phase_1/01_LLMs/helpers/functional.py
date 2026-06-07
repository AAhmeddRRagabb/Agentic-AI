# ---------------------------------------------
# Import general utility functions
# ---------------------------------------------

from typing import Any
import json
from pathlib import Path

import traceback


# from groq.types.c






    

# -------------------- Printing Utils --------------------------
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"



def format_error(error: Exception) -> dict:
    tb = traceback.extract_tb(error.__traceback__)

    last_frame = tb[-1] if tb else None

    return {
        "error_type"    : type(error).__name__,
        "error_message" : str(error),
        "error_file"    : str(Path(last_frame.filename).resolve()) if last_frame else None,
        "error_line"    : last_frame.lineno if last_frame else None,
        "error_function": last_frame.name if last_frame else None,
    }



def print_subtitle(subtitle: str):
    subtitle = f" {subtitle} ".center(50, "=")
    print(f"{BLUE}{subtitle}{RESET}")
    print()


def print_success_message(message: str):
    print(f"{GREEN}>> {message} <<{RESET}")


def print_error(error: Exception, message: str):
    sep = 50 * '='
    print(f"{RED}{sep}{RESET}")

    print(f"{RED}>> {message} <<{RESET}: ")
    
    err_json = format_error(error)
    print(json.dumps(err_json, indent = 2))
    
    print(f"{RED}{sep}{RESET}")


def print_title(title: str, n_sep: int =  100, sep: str = "="):
    """Printing a title in a well-formatted manner"""
    title = f" {title} ".center(n_sep, sep)
    print(title)


def print_structured_response(structured_response):
    """Printing the Agent Structured Response"""
    # print_title("Structured Response", 50)
    structured_response = structured_response.model_dump()

    for attb, value in structured_response.items():
        print()
        print(f"{attb.capitalize()}", end = "")

        if isinstance(value, list):
            print(":")
            for item in value:
                if isinstance(item, dict): 
                    for key, val in item.items():
                        print(f"\t{key} => {val}")
                else:
                    print(f"\t{item}")
                
                print()

        else:
            print(f"=> {value}")


def print_dict(dic: dict, n_identation: int):
    identation = ""
    if n_identation > 0:
        identation = "\t" * n_identation
    for k, v in dic.items():
        print(f"{identation}{k} => {v}")


def print_semi_dict(semi_dict: Any, n_identation: int):
    identation = ""
    if n_identation > 0:
        identation = "\t" * n_identation
    print()
    items = semi_dict.__dict__.items()
    for k, v in items:
        print(f"{identation}{k} => {v}")


def print_list(list_obj: list[Any], n_identation: int, item_name: str):
    identation = ""
    if n_identation > 0:
        identation = "\t" * n_identation

    for idx, val in enumerate(list_obj, start = 1):
        print(f"- {item_name} #{idx}")
        print(f"{identation}{type(val)}")
        print()    
