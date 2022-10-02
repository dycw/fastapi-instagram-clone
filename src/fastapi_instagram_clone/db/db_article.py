from beartype import beartype
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.exc import NoResultFound

from fastapi_instagram_clone.db.common import (
    handle_no_result_or_multiple_results,
)
from fastapi_instagram_clone.db.models import DbArticle
from fastapi_instagram_clone.db.schemas import ArticleBase
from fastapi_instagram_clone.exceptions import StoryException
from fastapi_instagram_clone.types import YieldSession


@beartype
def create_article(
    request: ArticleBase, yield_sess: YieldSession, /
) -> DbArticle:
    if (content := request.content).startswith("Once upon a time"):
        raise StoryException("No stories please")
    new_article = DbArticle(
        title=request.title,
        content=content,
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
    try:
        return sess.query(DbArticle).where(DbArticle.id == id).one()
    except (NoResultFound, MultipleResultsFound) as error:
        return handle_no_result_or_multiple_results(error, "article", id)
