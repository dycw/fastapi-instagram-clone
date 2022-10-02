from typing import Any

from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from fastapi_instagram_clone.auth.oauth2 import get_current_user
from fastapi_instagram_clone.db import db_article
from fastapi_instagram_clone.db.database import session
from fastapi_instagram_clone.db.models import DbArticle
from fastapi_instagram_clone.db.models import DbUser
from fastapi_instagram_clone.db.schemas import ArticleBase
from fastapi_instagram_clone.db.schemas import ArticleDisplay


router = APIRouter(prefix="/article", tags=["article"])


@router.post("/", response_model=ArticleDisplay)
@beartype
def create_article(
    *,
    request: ArticleBase,
    session: Session = Depends(session),
    _: DbUser = Depends(get_current_user),
) -> DbArticle:
    return db_article.create_article(request, session)


@router.get("/{id}")
@beartype
def get_article(
    *,
    session: Session = Depends(session),
    id: int,
    current_user: DbUser = Depends(get_current_user),
) -> dict[str, Any]:
    return {
        "data": db_article.get_article(session, id),
        "current_user": current_user,
    }
