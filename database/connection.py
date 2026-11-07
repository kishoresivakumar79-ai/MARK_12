"""
Database Connection Manager for MARK 12
Supports both standard SQLite3 connection and SQLAlchemy sessions.
"""
import sqlite3
import os
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "mark_12.db"

def get_db_path() -> str:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return str(DB_PATH)

def get_connection() -> sqlite3.Connection:
    """Return a raw SQLite3 connection configured with row_factory as Row and WAL journal."""
    db_file = get_db_path()
    conn = sqlite3.connect(db_file, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

@contextmanager
def get_db():
    """Context manager for SQLite database sessions."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# SQLAlchemy optional compatibility layer
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base

    DATABASE_URL = f"sqlite:///{get_db_path()}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def get_sqlalchemy_session():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
except ImportError:
    Base = object
    engine = None
    SessionLocal = None
    def get_sqlalchemy_session():
        yield None
