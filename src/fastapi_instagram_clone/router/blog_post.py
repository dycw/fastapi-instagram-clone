from beartype import beartype
from fastapi import APIRouter


router = APIRouter(prefix="/blog", tags=["blog"])


@router.post("/new")
@beartype
def create_blog() -> None:
    pass
