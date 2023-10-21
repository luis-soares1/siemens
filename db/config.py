from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Replace this with the env variable
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/python_db"
engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocomit=False, autoflush=False, bind=engine)
Base = declarative_base()