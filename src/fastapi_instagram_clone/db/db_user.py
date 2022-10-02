from typing import Literal

from beartype import beartype

from fastapi_instagram_clone.db.hash import Hash
from fastapi_instagram_clone.db.models import DbUser
from fastapi_instagram_clone.db.schemas import UserBase
from fastapi_instagram_clone.types import YieldSession


@beartype
def create_user(request: UserBase, yield_sess: YieldSession, /) -> DbUser:
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash().bcrypt(request.password),
    )
    with yield_sess as sess:
        sess.add(new_user)
        sess.commit()
        sess.refresh(new_user)
    return new_user


@beartype
def get_all_users(yield_sess: YieldSession, /) -> list[DbUser]:
    with yield_sess as sess:
        return sess.query(DbUser).all()


@beartype
def get_user(yield_sess: YieldSession, id: int, /) -> DbUser:
    with yield_sess as sess:
        user = sess.query(DbUser).where(DbUser.id == id).first()
    if user is None:
        raise ValueError
    return user


@beartype
def update_user(
    yield_sess: YieldSession, id: int, request: UserBase, /
) -> Literal["ok"]:
    with yield_sess as sess:
        user = sess.query(DbUser).where(DbUser.id == id)
        if user is None:
            raise ValueError
        _ = user.update(
            {
                DbUser.username: request.username,
                DbUser.email: request.email,
                DbUser.password: Hash().bcrypt(request.password),
            }
        )
        sess.commit()
    return "ok"


@beartype
def delete_user(yield_sess: YieldSession, id: int, /) -> Literal["ok"]:
    with yield_sess as sess:
        user = sess.query(DbUser).where(DbUser.id == id).first()
        if user is None:
            raise ValueError
        sess.delete(user)
        sess.commit()
    return "ok"
