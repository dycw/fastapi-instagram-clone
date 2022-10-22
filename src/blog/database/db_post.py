import datetime as dt

from beartype import beartype
from sqlalchemy.orm import Session

from blog.database.models import DbPost
from blog.routers.schemas import PostBase


@beartype
def create(db: Session, request: PostBase, /) -> DbPost:
    new_post = DbPost(
        image_url=request.image_url,
        title=request.title,
        content=request.content,
        creator=request.creator,
        timestamp=dt.datetime.now(),
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
