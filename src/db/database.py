import os
import sqlite3
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

# Get the directory where the database should be stored
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
os.makedirs(DB_DIR, exist_ok=True)

# Create the database path
DB_PATH = os.path.join(DB_DIR, 'exercise_medicine.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"Database path: {DB_PATH}")
print(f"Database directory exists: {os.path.exists(DB_DIR)}")
print(f"Database directory is writable: {os.access(DB_DIR, os.W_OK)}")

# Create SQLAlchemy base class
Base = declarative_base()

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True  # Enable SQL logging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()