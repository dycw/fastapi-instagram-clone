from typing import Any

from beartype import beartype
from fastapi import APIRouter
from fastapi import Cookie
from fastapi import Form
from fastapi import Header
from fastapi import Response
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse


router = APIRouter(prefix="/product", tags=["product"])


products = ["watch", "camera", "phone"]


@router.post("/new")
def create_product(*, name: str = Form(...)) -> list[str]:
    products.append(name)
    return products


@router.get("/all")
@beartype
def get_all_products() -> Response:
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie("test_cookie", value="test_cookie_value")
    return response


@router.get("/withheader")
@beartype
def get_products(
    *,
    response: Response,
    custom_header: list[str] | None = Header(None),
    test_cookie: str | None = Cookie(None),
) -> dict[str, Any]:
    if custom_header is not None:
        response.headers["custom_response_header"] = ", ".join(custom_header)
    return {
        "data": products,
        "custom_header": custom_header,
        "my_cookie": test_cookie,
    }


@router.get(
    "/{id}",
    responses={
        status.HTTP_200_OK: {
            "content": {"text/html": {"<div>Product</div>"}},
            "description": "Returns the HTML for an object",
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {"text/plain": {"Product not available"}},
            "description": "A cleartext error message",
        },
    },
)
@beartype
def get_product(*, id: int) -> PlainTextResponse | HTMLResponse:
    if id >= len(products):
        out = "Product not available"
        return PlainTextResponse(
            out, status_code=status.HTTP_404_NOT_FOUND, media_type="text/plain"
        )
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
                .product {{
                    width: 500px;
                    height: 30px;
                    border: 2px inset green;
                    background-color: lightblue;
                    text-align: center;
                    }}
                </style>
            </head>
        <div class="product">{product}</div>
        """
        return HTMLResponse(out, media_type="text/html")
