from contextlib import AbstractContextManager

from sqlalchemy.orm import Session


YieldSession = AbstractContextManager[Session]
