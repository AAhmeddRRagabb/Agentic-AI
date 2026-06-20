# ------------------------------------------------------
# Alhamdulillah
# Logging Basics
# ------------------------------------------------------

# ---------------------------- Logging Levels ------------------------------------
# >> Debug   : detailed info, used for diagnosing.
# >> Info    : Confirmation that things work as expected
# >> Warning : Indication about something not expected and / or may cause problems in near future.
# >> Error   : More serious problem -> some function may not work.
# >> Critical: A more serious error -> the program itself cannot continue running.

# Logging Config:
# --> If we choose `info` as our base level --> Info & higher levels will be logged.
# --> default level is `warning`.


import logging


def add(num1: int, num2: int) -> int:
    return num1 + num2




logging.basicConfig(
    level = logging.INFO,
    filename = "logging_basics.txt",
    format = "%(asctime)s:%(levelname)s:%(message)s" # format [time:level:msg]
)



logging.info(f" 10 + 10 = {add(10, 10)}")
logging.debug(f" 10 + 10 = {add(10, 10)}") # will be ignored
logging.error(f" 10 + 10 = {add(10, 10)}")


