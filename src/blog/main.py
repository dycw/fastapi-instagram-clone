from beartype import beartype
from fastapi import FastAPI

from blog.database.database import engine
from blog.database.models import Base


app = FastAPI()


@app.get("/")
@beartype
def hw() -> str:
    return "Hello world!"


Base.metadata.create_all(engine)
