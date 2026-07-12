import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

# 1. Dynamically find the absolute path to your root LifeOS folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

# 2. Load configurations using the exact absolute path
class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = str(ENV_FILE_PATH)
        extra = "ignore"

settings = Settings()

# 3. Initialize the database engine
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 4. Create a session factory for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get a database session for endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()