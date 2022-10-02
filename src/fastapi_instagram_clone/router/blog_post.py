from typing import Any

from beartype import beartype
from fastapi import APIRouter
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
    return {"id": id, "data": blog, "version": version}
