import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s : %(name)s : %(levelname)s : %(message)s")

file_handler = logging.FileHandler("main_log.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(formatter)


if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def divide(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        logger.exception('Y cannot be zero')
        return 0


x, y = 10, 2
logger.info(divide(x, y))

x, y = 10, 0
logger.info(divide(x, y))

