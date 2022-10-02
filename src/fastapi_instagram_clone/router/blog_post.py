from typing import Any

from beartype import beartype
from fastapi import APIRouter
from fastapi import Query
from pydantic import BaseModel


router = APIRouter(prefix="/blog", tags=["blog"])


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: bool | None


@router.post("/new/{id}")
@beartype
def create_blog(
    *, blog: BlogModel, id: int, version: int = 1
) -> dict[str, Any]:
    return {"data": blog, "id": id, "version": version}


@router.post("/new/{id}/comment")
@beartype
def create_comment(
    *,
    blog: BlogModel,
    id: int,
    comment_id: int = Query(
        None,
        title="ID of the comment",
        description="Some description for comment_id",
        alias="commentId",
        deprecated=True,
    ),
) -> dict[str, Any]:
    return {"blog": blog, "id": id, "comment_id": comment_id}
