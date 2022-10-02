from typing import Literal

from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from fastapi_instagram_clone.auth.oauth2 import get_current_user
from fastapi_instagram_clone.db import db_user
from fastapi_instagram_clone.db.database import session
from fastapi_instagram_clone.db.models import DbUser
from fastapi_instagram_clone.db.schemas import UserBase
from fastapi_instagram_clone.db.schemas import UserDisplay


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserDisplay)
@beartype
def create_user(
    *, request: UserBase, session: Session = Depends(session)
) -> DbUser:
    return db_user.create_user(request, session)


@router.get("/", response_model=list[UserDisplay])
@beartype
def get_all_users(
    *,
    session: Session = Depends(session),
    _: DbUser = Depends(get_current_user),
) -> list[DbUser]:
    return db_user.get_all_users(session)


@router.get("/{id}", response_model=UserDisplay)
@beartype
def get_user(
    *,
    session: Session = Depends(session),
    id: int,
    _: DbUser = Depends(get_current_user),
) -> DbUser:
    return db_user.get_user(session, id)


@router.post("/{id}/update")
@beartype
def update_user(
    *,
    session: Session = Depends(session),
    id: int,
    request: UserBase,
    _: DbUser = Depends(get_current_user),
) -> Literal["ok"]:
    return db_user.update_user(session, id, request)


@router.get("/{id}/delete")
@beartype
def delete_user(
    *,
    session: Session = Depends(session),
    id: int,
    _: DbUser = Depends(get_current_user),
) -> Literal["ok"]:
    return db_user.delete_user(session, id)
