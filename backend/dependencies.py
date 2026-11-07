"""
FastAPI Dependencies for MARK 12
Provides dependency injection for database sessions, assistant instances, and security.
"""
from core.assistant import mark_12
from database.connection import get_db

def get_assistant():
    return mark_12

def get_db_session():
    with get_db() as conn:
        yield conn
