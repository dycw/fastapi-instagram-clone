from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends

from fastapi_instagram_clone.db import db_user
from fastapi_instagram_clone.db.database import yield_sess
from fastapi_instagram_clone.db.models import DbUser
from fastapi_instagram_clone.db.schemas import UserBase
from fastapi_instagram_clone.db.schemas import UserDisplay
from fastapi_instagram_clone.types import YieldSession


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserDisplay)
@beartype
def create_user(
    *, request: UserBase, yield_sess: YieldSession = Depends(yield_sess)
) -> DbUser:
    return db_user.create_user(request, yield_sess)


@router.get("/", response_model=list[UserDisplay])
@beartype
def get_all_users(
    *, yield_sess: YieldSession = Depends(yield_sess)
) -> list[DbUser]:
    return db_user.get_all_users(yield_sess)


@router.get("/{id}", response_model=UserDisplay)
@beartype
def get_user(
    *, yield_sess: YieldSession = Depends(yield_sess), id: int
) -> DbUser:
    return db_user.get_user(yield_sess, id)
