"""
Database utilities for the SportsIQ application.
"""
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from sportsiq.utils.env_utils import get_database_url

# Configure logger
logger = logging.getLogger(__name__)

def get_db_engine():
    """
    Create and return a SQLAlchemy database engine using the connection string from environment.
    
    Returns:
        Engine: SQLAlchemy engine instance
    """
    try:
        engine = create_engine(get_database_url())
        logger.info("Database engine created successfully")
        return engine
    except Exception as e:
        logger.error(f"Error creating database engine: {e}")
        raise

def get_db_session():
    """
    Create and return a SQLAlchemy database session.
    
    Returns:
        Session: SQLAlchemy session instance
    """
    try:
        engine = get_db_engine()
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        logger.error(f"Error creating database session: {e}")
        raise

def test_connection():
    """
    Test the database connection.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection test failed: {e}")
        return False

def execute_query(query, params=None):
    """
    Execute a SQL query and return the results.
    
    Args:
        query (str): SQL query to execute
        params (dict, optional): Parameters for the query
    
    Returns:
        list: List of rows as dictionaries
    """
    try:
        session = get_db_session()
        result = session.execute(text(query), params or {})
        rows = [dict(row._mapping) for row in result]
        session.close()
        return rows
    except SQLAlchemyError as e:
        logger.error(f"Error executing query: {e}")
        if session:
            session.close()
        raise 