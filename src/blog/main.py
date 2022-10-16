from beartype import beartype
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
@beartype
def hw() -> str:
    return "Hello world!"
