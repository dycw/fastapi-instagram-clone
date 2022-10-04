from asyncio import sleep
from typing import Any
from typing import Literal
from typing import Optional
from typing import Union

from beartype import beartype
from fastapi import APIRouter
from fastapi import Cookie
from fastapi import Form
from fastapi import Header
from fastapi import Response
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse

from fastapi_instagram_clone.custom_log import log


router = APIRouter(prefix="/product", tags=["product"])


products = ["watch", "camera", "phone"]


@beartype
async def time_consuming_functionality() -> Literal["ok"]:
    await sleep(5)
    return "ok"


@router.post("/new")
@beartype
def create_product(*, name: str = Form(...)) -> list[str]:
    products.append(name)
    return products


@router.get("/all")
@beartype
async def get_all_products() -> Response:
    log(tag="MyAPI", message="Call to get all products")
    _ = await time_consuming_functionality()
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie("test_cookie", value="test_cookie_value")
    return response


@router.get("/withheader")
@beartype
def get_products(
    *,
    response: Response,
    custom_header: Optional[list[str]] = Header(None),
    test_cookie: Optional[str] = Cookie(None),
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
def get_product(*, id: int) -> Union[PlainTextResponse, HTMLResponse]:
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
