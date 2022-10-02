from contextlib import AbstractContextManager

from beartype import beartype
from sqlalchemy.orm import Session

from fastapi_instagram_clone.db.hash import Hash
from fastapi_instagram_clone.db.models import DbUser
from fastapi_instagram_clone.db.schemas import UserBase


@beartype
def create_user(
    request: UserBase, yield_session: AbstractContextManager[Session], /
) -> DbUser:
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash().bcrypt(request.password),
    )
    with yield_session as db:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return new_user
