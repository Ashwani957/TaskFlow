"""
Diagnostic script to test DB connection and session creation.
"""
from src.utils.db import get_db, LocalSession
from src.tasks.models import TaskModel
from sqlalchemy.orm import Session

def test_db():
    print("Testing LocalSession...")
    session = LocalSession()
    if session is None:
        print("ERROR: LocalSession() returned None")
        return
    print(f"SUCCESS: Session created: {session}")
    
    try:
        print("Testing query...")
        count = session.query(TaskModel).count()
        print(f"SUCCESS: Found {count} tasks")
    except Exception as e:
        print(f"ERROR: Query failed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    test_db()
