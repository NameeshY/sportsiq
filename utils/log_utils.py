"""
Logging utilities for the SportsIQ application.
"""
import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

from sportsiq.utils.env_utils import get_log_level, is_debug_mode

def setup_logging(app_name="sportsiq"):
    """
    Set up logging for the application.
    
    Args:
        app_name (str): Name of the application for the logger
        
    Returns:
        Logger: Configured logger instance
    """
    # Get log level from environment
    log_level = get_log_level()
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Set up the logger
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    if logger.handlers:
        logger.handlers = []
    
    # Log format
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # File handler (if not in debug mode)
    if not is_debug_mode():
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(logs_dir, f"{app_name}_{timestamp}.log")
        
        # Rotating file handler (10MB max file size, keep 5 backups)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    
    logger.info(f"Logger configured with level: {logging.getLevelName(log_level)}")
    return logger

def get_logger(module_name):
    """
    Get a logger for a specific module.
    
    Args:
        module_name (str): Name of the module
        
    Returns:
        Logger: Logger for the module
    """
    return logging.getLogger(f"sportsiq.{module_name}") 