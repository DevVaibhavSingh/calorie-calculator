from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Make sure the DATABASE_URL is using the correct PostgreSQL format
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL  # This should be a PostgreSQL URL

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
