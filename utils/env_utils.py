"""
Environment utilities for the SportsIQ application.
"""
import os
from dotenv import load_dotenv
import logging

# Configure logger
logger = logging.getLogger(__name__)

def load_environment():
    """
    Load environment variables from .env file.
    
    Returns:
        bool: True if environment loaded successfully, False otherwise.
    """
    try:
        # Load environment variables from .env file
        load_dotenv()
        logger.info("Environment variables loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load environment variables: {e}")
        return False

def get_database_url():
    """
    Constructs and returns the database URL from environment variables.
    
    Returns:
        str: The database URL for SQLAlchemy
    """
    username = os.getenv("DB_USERNAME", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "sportsiq")
    
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"

def is_debug_mode():
    """
    Checks if the application is running in debug mode.
    
    Returns:
        bool: True if in debug mode, False otherwise
    """
    return os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

def get_log_level():
    """
    Gets the configured log level from environment.
    
    Returns:
        int: Logging level constant
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    return levels.get(log_level, logging.INFO) 