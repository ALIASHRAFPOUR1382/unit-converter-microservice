from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Get connection information from environment variables
# Default to SQLite for local development (no PostgreSQL setup required)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./tododb.db"  # SQLite database file
)

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    # SQLite specific settings
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        echo=True
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(DATABASE_URL, echo=True)

# Create SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Create database tables
    """
    Base.metadata.create_all(bind=engine)

