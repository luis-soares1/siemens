from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings.config import get_settings

settings = get_settings()

def generate_db_url():
    # url = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    return "sqlite:///./test.db"
    # print(url, 'URL')
    # return url

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
engine = create_engine(generate_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

