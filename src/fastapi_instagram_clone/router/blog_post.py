from typing import Any
from typing import Optional

from beartype import beartype
from fastapi import APIRouter
from fastapi import Body
from fastapi import Path
from fastapi import Query
from pydantic import BaseModel


router = APIRouter(prefix="/blog", tags=["blog"])


class Image(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: list[str] = []
    metadata: dict[str, str] = {"key1": "val1"}
    image: Optional[Image] = None


@router.post("/new/{id}")
@beartype
def create_blog(
    *, blog: BlogModel, id: int, version: int = 1
) -> dict[str, Any]:
    return {"data": blog, "id": id, "version": version}


@router.post("/new/{id}/comment/{comment_id}")
@beartype
def create_comment(
    *,
    blog: BlogModel,
    id: int,
    comment_title: int = Query(
        None,
        title="Title of the comment",
        description="Some description for comment_id",
        alias="commentTitle",
        deprecated=True,
    ),
    content: str = Body(..., min_length=10, max_length=50, regex=r"^[a-z\s]*$"),
    v: Optional[list[str]] = Query(["1.0", "1.1", "1.2"]),
    comment_id: int = Path(None, gt=5, le=10),
) -> dict[str, Any]:
    return {
        "blog": blog,
        "id": id,
        "comment_title": comment_title,
        "content": content,
        "version": v,
        "comment_id": comment_id,
    }


@beartype
def required_functionality() -> dict[str, str]:
    return {"message": "Learning FastAPI is important"}
