from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from blog.database import db_post
from blog.database.database import get_db
from blog.database.models import DbPost
from blog.routers.schemas import PostBase


router = APIRouter(prefix="/post", tags=["post"])


@router.post("")
@beartype
def create(*, db: Session = Depends(get_db), request: PostBase) -> DbPost:
    return db_post.create(db, request)
