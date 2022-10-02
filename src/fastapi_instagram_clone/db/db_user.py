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
    sess = next(yield_sess)
    sess.add(new_user)
    sess.commit()
    sess.refresh(new_user)
    return new_user


@beartype
def get_all_users(yield_sess: YieldSession, /) -> list[DbUser]:
    sess = next(yield_sess)
    return sess.query(DbUser).all()


@beartype
def get_user(yield_sess: YieldSession, id: int, /) -> DbUser:
    sess = next(yield_sess)
    return sess.query(DbUser).where(DbUser.id == id).one()


@beartype
def update_user(
    yield_sess: YieldSession, id: int, request: UserBase, /
) -> Literal["ok"]:
    sess = next(yield_sess)
    user = sess.query(DbUser).where(DbUser.id == id).one()
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
    sess = next(yield_sess)
    user = sess.query(DbUser).where(DbUser.id == id).one()
    sess.delete(user)
    sess.commit()
    return "ok"
