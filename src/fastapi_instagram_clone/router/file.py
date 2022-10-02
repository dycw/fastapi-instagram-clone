from typing import Any

from beartype import beartype
from fastapi import APIRouter
from fastapi import File


router = APIRouter(prefix="/file", tags=["file"])


@router.post("/file")
@beartype
def get_file(*, file: bytes = File(...)) -> dict[str, Any]:
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"lines": lines}
