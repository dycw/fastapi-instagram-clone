from beartype import beartype
from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from fastapi_instagram_clone.auth import authentication
from fastapi_instagram_clone.db import models
from fastapi_instagram_clone.db.database import ENGINE
from fastapi_instagram_clone.db.database import Base
from fastapi_instagram_clone.exceptions import StoryException
from fastapi_instagram_clone.router import article
from fastapi_instagram_clone.router import blog_get
from fastapi_instagram_clone.router import blog_post
from fastapi_instagram_clone.router import file
from fastapi_instagram_clone.router import product
from fastapi_instagram_clone.router import user


app = FastAPI()
for router in [
    article.router,
    authentication.router,
    blog_get.router,
    blog_post.router,
    file.router,
    product.router,
    user.router,
]:
    app.include_router(router)


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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
