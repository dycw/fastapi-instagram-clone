from beartype import beartype
from fastapi import APIRouter
from fastapi import Response
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse


router = APIRouter(prefix="/product", tags=["product"])


products = ["watch", "camera", "phone"]


@router.get("/all")
@beartype
def get_all_products() -> Response:
    data = " ".join(products)
    return Response(content=data, media_type="text/plain")


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
