# ------------------
# Logging in a file
# ------------------

from io import TextIOWrapper
from typing import Any, Literal


TEXT_TITLE    = "title"
TEXT_SUBTITLE = "subtitle"
TEXT_LIST     = "list"
TEXT_NORMAL   = "normal"
TEXT_NEWLINE  = "newline"
TEXT_ERROR    = "error"

allowed_types = [
    TEXT_TITLE,
    TEXT_SUBTITLE,
    TEXT_LIST,
    TEXT_NORMAL,
    TEXT_NEWLINE,
    TEXT_ERROR
]


def validate_text_type(type: str):
    if type not in allowed_types:
        print(f"-------> Wrong Type: {type}, will be logged as a newline <-------")
        return False
    
    return True



def write_in_file(file: TextIOWrapper, text: Any, type: str = "newline", n_identation: int = 0) -> None:

    validated_type = validate_text_type(type)
    identation = ""

    if not validated_type or type == "newline":
        file.write("\n")

    elif n_identation > 0:
        identation = "\t" * n_identation

    if type == "title":
        text = f" {text} ".center(100, "=") 
        file.write(f"{text}\n\n")
    
    elif type == "subtitle":
        text = f"====> {text} <====\n\n"
        file.write(text)


    elif type == "list":
        for item in text:
            file.write(f"{identation}- {item}\n")
        
        file.write("\n")

    elif type == "normal":
        file.write(f"{identation}{text}\n")


    elif type == "error":
        file.write("\n")
        file.write("\n")
        text = f"\t\t\t{text}"
        file.write("\n")
        file.write(f"{text}\n")
        file.write("\n")
