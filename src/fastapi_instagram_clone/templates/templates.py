from beartype import beartype
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Request
from fastapi import Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi_instagram_clone.custom_log import log
from fastapi_instagram_clone.db.schemas import ProductBase


router = APIRouter(prefix="/templates", tags=["templates"])


templates = Jinja2Templates("templates")


@router.post("/products/{id}", response_class=HTMLResponse)
@beartype
def get_product(
    *, request: Request, id: int, product: ProductBase, bt: BackgroundTasks
) -> Response:
    bt.add_task(log_template_call, f"Template read for product with {id=}")
    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "id": id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
        },
    )


@beartype
def log_template_call(message: str, /) -> None:
    log(tag="MyAPI", message=message)
