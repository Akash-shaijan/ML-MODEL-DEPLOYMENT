import logging
import os
from logging.handlers import RotatingFileHandler
from app.config import settings

def setup_logger():
    
    os.makedirs("app/logs", exist_ok=True)

    logger = logging.getLogger("ml_api")  
    
    logger.setLevel(settings.LOG_LEVEL) 

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    console_handler = logging.StreamHandler()
    
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler("app/logs/app.log", maxBytes=1_000_000, backupCount=3)
    
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()

