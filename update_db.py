from sqlalchemy import create_engine, text
from src.utils.settings import settings

engine = create_engine(url=settings.DB_CONNECTION)

def run_migration(sql):
    with engine.connect() as conn:
        try:
            conn.execute(text(sql))
            conn.commit()
            print(f"SUCCESS: {sql}")
        except Exception as e:
            print(f"SKIPPED/FAILED: {sql} -> {e}")

# Add new columns to the chat_history table
print("Starting database migration...")
run_migration("ALTER TABLE chat_history ADD COLUMN session_id VARCHAR")
run_migration("ALTER TABLE chat_history ADD COLUMN session_title VARCHAR")
print("Migration check complete.")
