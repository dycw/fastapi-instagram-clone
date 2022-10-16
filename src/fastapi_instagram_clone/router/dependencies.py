from typing import Any

from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request


router = APIRouter(prefix="/dependencies", tags=["dependencies"])


@beartype
def convert_headers(*, request: Request, separator: str = "--") -> list[str]:
    out_headers: list[str] = []
    for key, value in request.headers.items():
        out_headers.append(f"{key} {separator} {value}")
    return out_headers


@router.get("/")
@beartype
def get_items(
    *,
    headers: list[str] = Depends(convert_headers),
    separator: str = "--",  # noqa: U100
) -> dict[str, Any]:
    return {"items": ["a", "b", "c"], "headers": headers}


@router.post("/new")
@beartype
def create_item(
    *, headers: list[str] = Depends(convert_headers)
) -> dict[str, Any]:
    return {"result": "new item created", "headers": headers}


class Account:
    @beartype
    def __init__(self, *, name: str, email: str) -> None:
        super().__init__()
        self.name = name
        self.email = email


@router.post("/user")
@beartype
def create_user(
    *, name: str, email: str, password: str, account: Account = Depends()
) -> dict[str, Any]:
    _ = (name, email, password)
    return {"name": account.name, "email": account.email}
