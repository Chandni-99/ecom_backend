from sqlalchemy import create_engine, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


engine=create_engine(settings.DB_URL,echo=True,pool_pre_ping=True)
SessionLocal = sessionmaker(autoflush=false, bind=engine)
Base = declarative_base()


def get_db():
    database =SessionLocal()
    try:
        yield database
    finally:
        database.close()