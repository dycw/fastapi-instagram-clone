from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends

from fastapi_instagram_clone.auth.oauth2 import oauth2_schema
from fastapi_instagram_clone.db import db_article
from fastapi_instagram_clone.db.database import yield_sess
from fastapi_instagram_clone.db.models import DbArticle
from fastapi_instagram_clone.db.schemas import ArticleBase
from fastapi_instagram_clone.db.schemas import ArticleDisplay
from fastapi_instagram_clone.types import YieldSession


router = APIRouter(prefix="/article", tags=["article"])


@router.post("/", response_model=ArticleDisplay)
@beartype
def create_article(
    *, request: ArticleBase, yield_sess: YieldSession = Depends(yield_sess)
) -> DbArticle:
    return db_article.create_article(request, yield_sess)


@router.get("/{id}", response_model=ArticleDisplay)
@beartype
def get_article(
    *,
    yield_sess: YieldSession = Depends(yield_sess),
    id: int,
    token: str = Depends(oauth2_schema),
) -> DbArticle:
    _ = token
    return db_article.get_article(yield_sess, id)
