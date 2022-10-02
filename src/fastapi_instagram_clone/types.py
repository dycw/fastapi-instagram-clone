from collections.abc import Iterator

from sqlalchemy.orm import Session


YieldSession = Iterator[Session]
