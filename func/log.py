import sys
from enum import Enum
import inspect
from loguru import logger

class Level(Enum):
    DEBUG = "DEBUG"
    SUCCESS = "SUCCESS"
    INFO = "INFO"

def do(string: str, level = Level.INFO):

    try:
        logger.remove(0)
    except:
        pass

    file = str(inspect.stack()[1].filename)
    line = str(inspect.stack()[1].lineno)
    logger.configure(extra={"filex": file, "linex": line})


    match level.name:
        case "DEBUG":
            log_level = "DEBUG"
            log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <yellow>File {extra[filex]} line: ({extra[linex]}):</yellow> <b>{message}</b>"
            logger.add(sys.stderr, level=log_level, format=log_format, colorize=True, backtrace=True, diagnose=True)
            logger.add("app.log", level=log_level, format=log_format, colorize=True, backtrace=True, diagnose=True)
            logger.debug(string)
        case "SUCCESS":
            log_level = "INFO"
            log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <b>{message}</b>"
            logger.add(sys.stderr, level=log_level, format=log_format, colorize=True, backtrace=True, diagnose=True)
            logger.add("app.log", level=log_level, format=log_format, colorize=True, backtrace=True, diagnose=True)
            logger.success("APP core: " + string)
        case _:
            log_level = "INFO"
            log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <b>{message}</b>"
            logger.add(sys.stderr, level=log_level, format=log_format, colorize=True, backtrace=True, diagnose=True)
            logger.add("app.log", level=log_level, format=log_format, colorize=True, backtrace=True, diagnose=True)
            logger.info(string)

    logger.remove()
    # logger.success(string)
    # logger.error(string)
    # logger.debug(string)
    # logger.info(string)
    # logger.warning(string)
