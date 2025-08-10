from ahk_cursor.c_api import GetProcessByName
from ahk_cursor.logger import logger


def check_running(executable_name="BGI.exe"):
    ret = GetProcessByName(executable_name)
    if not ret:
        logger.info(f"{executable_name} not running")
        return -1
    else:
        logger.info(f"{executable_name} running")
        return ret
