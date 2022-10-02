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
def get_all_blogs() -> dict[str, str]:
    return {"message": "All blogs provided"}


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
