"""
Check current columns in user_tasks table.
"""
from sqlalchemy import create_engine, inspect
from src.utils.settings import settings

engine = create_engine(url=settings.DB_CONNECTION)
inspector = inspect(engine)

columns = [c['name'] for c in inspector.get_columns('user_tasks')]
print(f"COLUMNS: {columns}")
