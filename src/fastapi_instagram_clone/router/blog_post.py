from beartype import beartype
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/blog", tags=["blog"])


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: bool | None


@router.post("/new")
@beartype
def create_blog(*, blog: BlogModel) -> dict[str, BlogModel]:
    return {"data": blog}
