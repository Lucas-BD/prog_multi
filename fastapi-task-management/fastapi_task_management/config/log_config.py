import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from fastapi_task_management.config.settings import PROJECT_ROOT

def setup_logging():
    log_format = "%(asctime)s [%(threadName)s] [fastapi_task_management] %(levelname)s %(name)s.%(funcName)s - %(message)s"
    logger = logging.getLogger("fastapi")
    logger.setLevel(logging.INFO)
    log_directory = f'{PROJECT_ROOT}/logs'

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(fmt=log_format))

    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(f'{log_directory}/fastapi.log', 
                                            when='midnight',
                                            interval=1,
                                            backupCount=30,
                                            encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(fmt=log_format))
    logger.addHandler(file_handler)
    return logger