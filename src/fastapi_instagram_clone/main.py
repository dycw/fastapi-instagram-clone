from beartype import beartype
from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from fastapi_instagram_clone.db import models
from fastapi_instagram_clone.db.database import ENGINE
from fastapi_instagram_clone.db.database import Base
from fastapi_instagram_clone.exceptions import StoryException
from fastapi_instagram_clone.router import article
from fastapi_instagram_clone.router import blog_get
from fastapi_instagram_clone.router import blog_post
from fastapi_instagram_clone.router import product
from fastapi_instagram_clone.router import user


app = FastAPI()
app.include_router(article.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(product.router)
app.include_router(user.router)


@app.get("/hello")
@beartype
def index() -> dict[str, str]:
    return {"message": "Hello world!"}


@app.exception_handler(StoryException)  # type: ignore
@beartype
def store_exception_handler(
    _: Request, error: StoryException, /
) -> JSONResponse:
    return JSONResponse(
        {"detail": error.name}, status_code=status.HTTP_418_IM_A_TEAPOT
    )


_ = models  # for the models
with ENGINE.begin() as conn:
    Base.metadata.create_all(conn)
