from collections.abc import Awaitable
from collections.abc import Callable
from time import time

from beartype import beartype
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi import WebSocket
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from fastapi_instagram_clone.auth import authentication
from fastapi_instagram_clone.client import html
from fastapi_instagram_clone.db import models
from fastapi_instagram_clone.db.database import ENGINE
from fastapi_instagram_clone.db.database import Base
from fastapi_instagram_clone.exceptions import StoryException
from fastapi_instagram_clone.router import article
from fastapi_instagram_clone.router import blog_get
from fastapi_instagram_clone.router import blog_post
from fastapi_instagram_clone.router import dependencies
from fastapi_instagram_clone.router import file
from fastapi_instagram_clone.router import product
from fastapi_instagram_clone.router import user
from fastapi_instagram_clone.templates import templates


app = FastAPI()
for router in [
    article.router,
    authentication.router,
    blog_get.router,
    blog_post.router,
    dependencies.router,
    file.router,
    product.router,
    templates.router,
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


@app.get("/")
@beartype
async def get() -> HTMLResponse:
    return HTMLResponse(html)


clients: list[WebSocket] = []


@app.websocket("/chat")
@beartype
async def websocket_endpoint(*, websocket: WebSocket) -> HTMLResponse:
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


_ = models  # for the models
with ENGINE.begin() as conn:
    Base.metadata.create_all(conn)


@app.middleware("http")  # type: ignore
@beartype
async def add_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_time = time()
    response = await call_next(request)
    duration = time() - start_time
    response.headers["duration"] = str(duration)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.mount("/files", StaticFiles(directory="files"), name="files")
app.mount(
    "/templates/static",
    StaticFiles(directory="templates/static"),
    name="static",
)
