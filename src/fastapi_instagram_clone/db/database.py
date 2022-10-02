from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any
from typing import cast

from beartype import beartype
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi-practice.db"
ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
Base = cast(Any, declarative_base())


@contextmanager
@beartype
def yield_session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
