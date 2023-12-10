import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from utils import get_env_value
import json
from typing import Any

LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
DATE_FORMAT = '%d-%m-%y %H:%M:%S'
LOG_LEVEL = logging.INFO

LOG_TO_FILE = True if os.getenv('LOG_TO_FILE') == 'true' else False

log_dir = 'logs'
log_file = 'bot_log.txt'

handlers = []

formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
if LOG_TO_FILE:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    handler = RotatingFileHandler(os.path.join(
        log_dir, log_file), maxBytes=2097152, backupCount=5)
    handler.setFormatter(formatter)
    handlers.append(handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
handlers.append(console_handler)

# Устанавливаем настройки для корневого логгера
root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)
root_logger.handlers = handlers

# Telegram bot settings
TELEGRAM_API_KEY = get_env_value('TELEGRAM_API_KEY')

# Backend root path
BACKEND_ROOT_PATH = get_env_value('BACKEND_ROOT_PATH')
BACKEND_SECRET = get_env_value('BACKEND_SECRET')