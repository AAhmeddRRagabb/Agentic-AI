# ------------------------------------------
# Implement Helpful functions
# ------------------------------------------

from typing import Any
from io import TextIOWrapper
import json
from pathlib import Path

# -------------------------------------- Logging -----------------------------------------
Message_Type = str | dict | list

def log_message(file: TextIOWrapper, message: Message_Type, n_identation: int = 0) -> None:

    identation = "\t" * n_identation

    if isinstance(message, str):
        file.write(f"{identation}{message}\n")

    elif isinstance(message, list):
        for item in message:
            if not isinstance(item, str):
                log_message(file, item, n_identation + 1)

            else:
                log_message(file, f">> {item}", n_identation)

    elif isinstance(message, dict):
        for key, val in message.items():
            if not isinstance(val, str):
                log_message(file, val, n_identation + 1)
            
            else:
                log_message(file, f">> {key} ==> {val}", n_identation)
    
    else:
        raise ValueError("Message Type is not allowed. Allowed types (str, dict, list)")



def log_title(file, title: str) -> None:
    title = f" {title} ".center(100, "=")
    log_message(file, f"{title}\n")

# --------------------------------- Files -------------------------------
def load_json_file(file_path: str | Path) -> Any:
    with open(file_path, mode = "r", encoding = "utf-8") as f:
        return json.load(f)


def reset_json_file(file_path: str | Path) -> None:
    with open(file_path, mode = "w", encoding = "utf-8") as f:
        json.dump([], f, indent = 4)


def append_json_result(file_path: str | Path, result: dict[str, Any] | list[dict[str, Any]]) -> None:
    try:
        data = load_json_file(file_path)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if not isinstance(data, list):
        data = []

    data.append(result)

    with open(file_path, mode = "w", encoding = "utf-8") as f:
        json.dump(data, f, indent = 4, ensure_ascii = False)
