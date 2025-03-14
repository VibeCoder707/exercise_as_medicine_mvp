import os
from sqlalchemy import inspect
from .database import engine, Base, DB_PATH

def check_database_status():
    """Check database status and print debug information"""
    print("\n=== Database Status ===")
    
    # Check database file
    print(f"\nDatabase file path: {DB_PATH}")
    print(f"Database file exists: {os.path.exists(DB_PATH)}")
    if os.path.exists(DB_PATH):
        print(f"Database file size: {os.path.getsize(DB_PATH)} bytes")
    
    # Check tables
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    print(f"\nTables in database: {table_names}")
    
    # Check table columns
    for table_name in table_names:
        print(f"\nColumns in {table_name}:")
        for column in inspector.get_columns(table_name):
            print(f"  - {column['name']}: {column['type']}")
    
    # Try a simple query
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT COUNT(*) FROM patients").scalar()
            print(f"\nNumber of patients in database: {result}")
    except Exception as e:
        print(f"\nError querying database: {str(e)}")

    print("\n=====================")