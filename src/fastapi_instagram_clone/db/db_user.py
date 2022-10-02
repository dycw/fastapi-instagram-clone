from typing import Literal

from beartype import beartype
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from fastapi_instagram_clone.db.common import (
    handle_no_result_or_multiple_results,
)
from fastapi_instagram_clone.db.hash import Hash
from fastapi_instagram_clone.db.models import DbUser
from fastapi_instagram_clone.db.schemas import UserBase


@beartype
def create_user(request: UserBase, session: Session, /) -> DbUser:
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash().bcrypt(request.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@beartype
def get_all_users(session: Session, /) -> list[DbUser]:
    return session.query(DbUser).all()


@beartype
def get_user(session: Session, id: int, /) -> DbUser:
    try:
        return session.query(DbUser).where(DbUser.id == id).one()
    except (NoResultFound, MultipleResultsFound) as error:
        return handle_no_result_or_multiple_results(error, "user", "id", id)


@beartype
def get_user_by_username(session: Session, username: str, /) -> DbUser:
    try:
        return session.query(DbUser).where(DbUser.username == username).one()
    except (NoResultFound, MultipleResultsFound) as error:
        return handle_no_result_or_multiple_results(
            error, "user", "username", username
        )


@beartype
def update_user(
    session: Session, id: int, request: UserBase, /
) -> Literal["ok"]:
    try:
        user = session.query(DbUser).where(DbUser.id == id).one()
    except (NoResultFound, MultipleResultsFound) as error:
        return handle_no_result_or_multiple_results(error, "user", "id", id)
    _ = user.update(
        {
            DbUser.username: request.username,
            DbUser.email: request.email,
            DbUser.password: Hash().bcrypt(request.password),
        }
    )
    session.commit()
    return "ok"


@beartype
def delete_user(session: Session, id: int, /) -> Literal["ok"]:
    try:
        user = session.query(DbUser).where(DbUser.id == id).one()
    except (NoResultFound, MultipleResultsFound) as error:
        return handle_no_result_or_multiple_results(error, "user", "id", id)
    session.delete(user)
    session.commit()
    return "ok"
