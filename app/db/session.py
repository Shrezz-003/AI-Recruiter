from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# This line reads the DATABASE_URL from your .env file
DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)