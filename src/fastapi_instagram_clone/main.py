from enum import auto

from beartype import beartype
from fastapi import FastAPI
from utilities.enum import StrEnum


app = FastAPI()


@app.get("/hello")
@beartype
def index() -> dict[str, str]:
    return {"message": "Hello world!"}


@app.get("/blog/all")
@beartype
def get_all_blogs(
    *, page: int = 1, page_size: int | None = None
) -> dict[str, str]:
    return {"message": f"All {page_size} blogs on page {page}"}


@app.get("/blog/{id}/comments/{comment_id}")
@beartype
def get_blog_comments(
    *, id: int, comment_id: int, valid: bool = True, username: str | None = None
) -> dict[str, str]:
    return {"message": f"{id=}, {comment_id=}, {valid=}, {username=}"}


class BlogType(StrEnum):
    short = auto()
    story = auto()
    howto = auto()


@app.get("/blog/type/{type}")
@beartype
def get_blog_type(*, type: BlogType) -> dict[str, str]:
    return {"message": f"Blog with {type=}"}


@app.get("/blog/{id}")
@beartype
def get_blog(*, id: int) -> dict[str, str]:
    return {"message": f"Blog with {id=}"}
