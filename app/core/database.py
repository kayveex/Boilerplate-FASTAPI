from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

# Setup engine
database_url = settings.DATABASE_URL

# SQLite membutuhkan flag khusus `check_same_thread: False`
connect_args = {}
if database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    database_url,
    connect_args=connect_args,
    pool_pre_ping=True,  # Otomatis tes koneksi sebelum eksekusi (penting untuk Supabase pooler/MySQL timeout)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base untuk SQLAlchemy Models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency injection untuk FastAPI route handlers"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
