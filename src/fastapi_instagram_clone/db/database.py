from collections.abc import Iterator
from typing import Any
from typing import cast

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


def session() -> Iterator[Session]:  # cannot @beartype
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
