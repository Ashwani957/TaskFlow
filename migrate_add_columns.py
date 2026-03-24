"""
Robust migration for PostgreSQL.
Adds missing columns one by one with separate transactions.
"""
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

run_migration("ALTER TABLE user_tasks ADD COLUMN priority VARCHAR DEFAULT 'medium'")
run_migration("ALTER TABLE user_tasks ADD COLUMN due_date TIMESTAMP")
run_migration("ALTER TABLE user_tasks ADD COLUMN created_at TIMESTAMP")

print("Migration complete!")
