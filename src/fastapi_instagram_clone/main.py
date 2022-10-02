from beartype import beartype
from fastapi import FastAPI

from fastapi_instagram_clone.db import models
from fastapi_instagram_clone.db.database import ENGINE
from fastapi_instagram_clone.db.database import Base
from fastapi_instagram_clone.router import blog_get
from fastapi_instagram_clone.router import blog_post
from fastapi_instagram_clone.router import user


app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)


@app.get("/hello")
@beartype
def index() -> dict[str, str]:
    return {"message": "Hello world!"}


_ = models  # for the models
with ENGINE.begin() as conn:
    Base.metadata.create_all(conn)
