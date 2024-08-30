# Setup database connection and expose

from typing import Any, Generator
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from .with_enforcer import WithEnforcer


_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def setup(username: str, password: str, hostname: str, port: int, databasename: str):
    """User should setup database first"""
    global _engine, _SessionLocal

    # NOTE: postgres trust local connections, so may not need to provide password
    _engine = create_engine(
        f"postgresql://{username}:{password}@{hostname}:{port}/{databasename}"
    )
    _SessionLocal = sessionmaker(bind=_engine)


def get_session_yield() -> Generator[Session, Any, None]:
    """Used by FastAPI dependency"""
    if _SessionLocal is None:
        raise Exception("Databse has not been initialized")

    session: Session = _SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_session_with() -> Session:
    """Used by non-FastAPI user"""
    if _SessionLocal is None:
        raise Exception("Databse has not been initialized")

    session: Session = _SessionLocal()
    return WithEnforcer(session)  # type: ignore[return-type]
