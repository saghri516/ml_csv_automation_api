import logging
import sys
from datetime import datetime
from pathlib import Path
import config

# Create logs directory if it doesn't exist
config.LOGS_DIR.mkdir(exist_ok=True)

def setup_logger(name):
    """Setup logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # File handler
    fh = logging.FileHandler(config.LOG_FILE)
    fh.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

logger = setup_logger(__name__)
