from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# دریافت اطلاعات اتصال از متغیرهای محیطی
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/tododb"
)

# ایجاد engine
engine = create_engine(DATABASE_URL, echo=True)

# ایجاد SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class برای models
Base = declarative_base()


def get_db():
    """
    Dependency برای دریافت database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    ایجاد جداول دیتابیس
    """
    Base.metadata.create_all(bind=engine)

