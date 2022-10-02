from beartype import beartype

from fastapi_instagram_clone.db.models import DbArticle
from fastapi_instagram_clone.db.schemas import ArticleBase
from fastapi_instagram_clone.types import YieldSession


@beartype
def create_article(
    request: ArticleBase, yield_sess: YieldSession, /
) -> DbArticle:
    new_article = DbArticle(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.creator_id,
    )
    sess = next(yield_sess)
    sess.add(new_article)
    sess.commit()
    sess.refresh(new_article)
    return new_article


@beartype
def get_article(yield_sess: YieldSession, id: int, /) -> DbArticle:
    sess = next(yield_sess)
    return sess.query(DbArticle).where(DbArticle.id == id).one()
