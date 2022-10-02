from beartype import beartype
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from fastapi_instagram_clone.db.common import (
    handle_no_result_or_multiple_results,
)
from fastapi_instagram_clone.db.models import DbArticle
from fastapi_instagram_clone.db.schemas import ArticleBase
from fastapi_instagram_clone.exceptions import StoryException


@beartype
def create_article(request: ArticleBase, session: Session, /) -> DbArticle:
    if (content := request.content).startswith("Once upon a time"):
        raise StoryException("No stories please")
    new_article = DbArticle(
        title=request.title,
        content=content,
        published=request.published,
        user_id=request.creator_id,
    )
    session.add(new_article)
    session.commit()
    session.refresh(new_article)
    return new_article


@beartype
def get_article(session: Session, id: int, /) -> DbArticle:
    try:
        return session.query(DbArticle).where(DbArticle.id == id).one()
    except (NoResultFound, MultipleResultsFound) as error:
        return handle_no_result_or_multiple_results(error, "article", id)
