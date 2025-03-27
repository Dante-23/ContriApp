from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

from dotenv import load_dotenv
import os

load_dotenv()

# Access the DATABASE_URL environment variable
usernameEnv = os.getenv('username')
passwordEnv = os.getenv('password')
database_nameEnv = os.getenv('database_name')
urlEnv = os.getenv('url')

POSTGRESQL_DATABASE_URL = f'postgresql://{usernameEnv}:{quote_plus(passwordEnv)}@{urlEnv}:5432/{database_nameEnv}'
engine = create_engine(POSTGRESQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()