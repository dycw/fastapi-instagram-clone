from beartype import beartype
from fastapi import FastAPI

from fastapi_instagram_clone.router import blog_get
from fastapi_instagram_clone.router import blog_post


app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.get("/hello")
@beartype
def index() -> dict[str, str]:
    return {"message": "Hello world!"}
