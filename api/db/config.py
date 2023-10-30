from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from common.settings.config import app_settings


def generate_db_url():
    url = f"postgresql://{app_settings.postgres_user}:{app_settings.postgres_password}@{app_settings.db_host}:{app_settings.postgres_port}/{app_settings.postgres_db}"
    # url = "sqlite:///fastapi.db"
    return url
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
