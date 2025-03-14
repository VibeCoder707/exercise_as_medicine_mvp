import os
import sqlite3
from sqlalchemy import create_engine, event, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

# Get absolute path for database
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
DB_FILE = 'exercise_medicine.db'
DB_PATH = os.path.join(PROJECT_ROOT, 'data', DB_FILE)

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Create database URL with absolute path
DATABASE_URL = f"sqlite:///{DB_PATH}"

print("="*50)
print("Database Configuration")
print("="*50)
print(f"Current Directory: {CURRENT_DIR}")
print(f"Project Root: {PROJECT_ROOT}")
print(f"Database Path: {DB_PATH}")
print(f"Database URL: {DATABASE_URL}")

# Create base class for declarative models
Base = declarative_base()

# Import models to ensure they're registered with Base
from .models import Patient, Condition, Prescription

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
        # Enable SQL logging
        engine.echo = True
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("\nDatabase initialized successfully")
        
        # Verify tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {tables}")
        
        # Print table schemas
        for table_name in tables:
            print(f"\nSchema for table {table_name}:")
            for column in inspector.get_columns(table_name):
                print(f"  - {column['name']}: {column['type']}")
        
        # Check database file
        print(f"\nDatabase location: {DB_PATH}")
        print(f"Database exists: {os.path.exists(DB_PATH)}")
        if os.path.exists(DB_PATH):
            print(f"Database size: {os.path.getsize(DB_PATH)} bytes")
            
        # Try a simple query
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
            print(f"\nTables in SQLite master: {result}")
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database on module import
init_db()
