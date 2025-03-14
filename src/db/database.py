import os
import sqlite3
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

# Get absolute path for database
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))
DB_FILE = 'exercise_medicine.db'
DB_PATH = os.path.join(PROJECT_ROOT, DB_FILE)

# Create database URL - using root directory for visibility
DATABASE_URL = f"sqlite:///{DB_FILE}"

print("="*50)
print("Database Configuration")
print("="*50)
print(f"Current Directory: {CURRENT_DIR}")
print(f"Project Root: {PROJECT_ROOT}")
print(f"Database Path: {DB_PATH}")
print(f"Database URL: {DATABASE_URL}")

# Create base class for declarative models
Base = declarative_base()

# Create engine with SQLite configuration
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True  # Enable SQL logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database"""
    try:
        Base.metadata.create_all(bind=engine)
        print("\nDatabase initialized successfully")
        print(f"Looking for database at: {DB_PATH}")
        print(f"Database file exists: {os.path.exists(DB_PATH)}")
    except Exception as e:
        print(f"Error initializing database: {e}")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database on module import
init_db()