from beartype import beartype
from fastapi import FastAPI


app = FastAPI()


@app.get("/hello")
@beartype
def index() -> dict[str, str]:
    return {"message": "Hello world!"}


@app.get("/blog/all")
@beartype
def get_all_blogs() -> dict[str, str]:
    return {"message": "All blogs provided"}


@app.get("/blog/{id}")
@beartype
def get_blog(*, id: int) -> dict[str, str]:
    return {"message": f"Blog with {id=}"}
