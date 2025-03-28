#!/usr/bin/env python3
"""
SportsIQ Application Runner
This script launches the SportsIQ application and handles initialization.
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

# Add the current directory to the path so we can import sportsiq modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sportsiq.utils import setup_logging, get_logger
from sportsiq.utils.env_utils import load_env_variables
from sportsiq.utils.db_utils import check_database_connection

# Set up logging
logger = setup_logging()

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import streamlit
        import pandas
        import numpy
        import plotly
        logger.info("All core dependencies are installed.")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.info("Please run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check if the environment is properly set up."""
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_file):
        logger.warning(".env file not found. Creating a default .env file.")
        create_default_env_file(env_file)
    
    # Load environment variables
    load_env_variables()
    
    # Test database connection
    db_status = check_database_connection()
    if not db_status:
        logger.warning("Database connection failed. Application will continue but some features may not work.")
    else:
        logger.info("Database connection successful.")
    
    return True

def create_default_env_file(env_file_path):
    """Create a default .env file if one doesn't exist."""
    default_env = """# SportsIQ Environment Configuration
# Database settings
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sportsiq
DB_USER=postgres
DB_PASSWORD=password

# API settings
NBA_API_KEY=your_api_key_here
API_TIMEOUT=30

# Application settings
DEBUG=True
LOG_LEVEL=INFO
CACHE_DIRECTORY=./cache
"""
    
    with open(env_file_path, 'w') as f:
        f.write(default_env)
    
    logger.info(f"Created default .env file at: {env_file_path}")
    logger.info("Please update it with your actual configuration.")

def create_cache_directories():
    """Create cache directories if they don't exist."""
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        logger.info(f"Created cache directory at: {cache_dir}")
    
    # Create subdirectories for different types of cached data
    subdirs = ["api", "data", "models", "visualizations"]
    for subdir in subdirs:
        subdir_path = os.path.join(cache_dir, subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)
            logger.info(f"Created cache subdirectory: {subdir_path}")

def run_app(port=8501, debug=False):
    """Run the Streamlit application."""
    # Get the app.py file path
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    
    # Set the command to run Streamlit
    cmd = [
        "streamlit", "run", app_path,
        "--server.port", str(port)
    ]
    
    if debug:
        cmd.append("--logger.level=debug")
    
    logger.info(f"Starting SportsIQ application on port {port}")
    logger.info(f"Command: {' '.join(cmd)}")
    
    try:
        # Run the command
        subprocess.run(cmd)
    except KeyboardInterrupt:
        logger.info("Application stopped by user.")
    except Exception as e:
        logger.error(f"Error running Streamlit application: {e}")
        sys.exit(1)

def main():
    """Main function to run the application."""
    parser = argparse.ArgumentParser(description="Run the SportsIQ application")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the application on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    args = parser.parse_args()
    
    logger.info("Initializing SportsIQ application...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create cache directories
    create_cache_directories()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run the application
    run_app(port=args.port, debug=args.debug)

if __name__ == "__main__":
    main() 