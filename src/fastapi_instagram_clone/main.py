from enum import auto

from beartype import beartype
from fastapi import FastAPI
from fastapi import Response
from fastapi import status
from utilities.enum import StrEnum


app = FastAPI()


@app.get("/hello")
@beartype
def index() -> dict[str, str]:
    return {"message": "Hello world!"}


@app.get("/blog/all", tags=["blog"])
@beartype
def get_all_blogs(
    *, page: int = 1, page_size: int | None = None
) -> dict[str, str]:
    return {"message": f"All {page_size} blogs on page {page}"}


@app.get("/blog/{id}/comments/{comment_id}", tags=["blog", "comment"])
@beartype
def get_blog_comments(
    *, id: int, comment_id: int, valid: bool = True, username: str | None = None
) -> dict[str, str]:
    return {"message": f"{id=}, {comment_id=}, {valid=}, {username=}"}


class BlogType(StrEnum):
    short = auto()
    story = auto()
    howto = auto()


@app.get("/blog/type/{type}", tags=["blog"])
@beartype
def get_blog_type(*, type: BlogType) -> dict[str, str]:
    return {"message": f"Blog with {type=}"}


@app.get("/blog/{id}", tags=["blog"])
@beartype
def get_blog(*, id: int, response: Response) -> dict[str, str]:
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Blog with {id=} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Blog with {id=}"}
