from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


#create db engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

#create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base class for models
Base = declarative_base()

#dependency to get db sess
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()