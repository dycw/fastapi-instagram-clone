from collections.abc import Generator

from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from fastapi_instagram_clone.db.database import get_db
from fastapi_instagram_clone.db.db_user import create_user
from fastapi_instagram_clone.db.models import DbUser
from fastapi_instagram_clone.db.schemas import UserBase
from fastapi_instagram_clone.db.schemas import UserDisplay


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserDisplay)
@beartype
def create_user_endpoint(
    *, request: UserBase, db: Generator[Session, None, None] = Depends(get_db)
) -> DbUser:
    return create_user(db, request)
