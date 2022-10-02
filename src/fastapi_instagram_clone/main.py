from beartype import beartype
from fastapi import FastAPI


app = FastAPI()


@app.get("/hello")
@beartype
def index() -> dict[str, str]:
    return {"message": "Hello world!"}
