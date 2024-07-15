from typing import Any, Generator
from database.records import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

# Setup database connection
engine = create_engine("postgresql://superuser:wrong_password@localhost:5432/database")

# Create tables if not exists
Base.metadata.create_all(engine)


SessionLocal = sessionmaker(autoflush=True, bind=engine)


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
