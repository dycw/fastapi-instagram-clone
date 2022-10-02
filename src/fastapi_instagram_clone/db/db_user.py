from collections.abc import Generator

from beartype import beartype
from sqlalchemy.orm import Session

from fastapi_instagram_clone.db.hash import Hash
from fastapi_instagram_clone.db.models import DbUser
from fastapi_instagram_clone.db.schemas import UserBase


@beartype
def create_user(
    db: Generator[Session, None, None], request: UserBase, /
) -> DbUser:
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash().bcrypt(request.password),
    )
    db2 = next(db)
    db2.add(new_user)
    db2.commit()
    db2.refresh(new_user)
    return new_user
