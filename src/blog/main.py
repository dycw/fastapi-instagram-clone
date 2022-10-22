from fastapi import FastAPI

from blog.database.database import engine
from blog.database.models import Base
from blog.routers import post


app = FastAPI()
app.include_router(post.router)


Base.metadata.create_all(engine)
