from beartype import beartype
from fastapi import FastAPI

from fastapi_instagram_clone.router import blog_get


app = FastAPI()
app.include_router(blog_get.router)


@app.get("/hello")
@beartype
def index() -> dict[str, str]:
    return {"message": "Hello world!"}
