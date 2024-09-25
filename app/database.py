from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import SQLALCHEMY_DATABASE_URL
from .models import Base  # Ensure models are imported

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)  # This line creates the tables if they don't exist


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
