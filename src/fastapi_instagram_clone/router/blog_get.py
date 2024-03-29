from enum import auto
from typing import Any
from typing import Optional

from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status
from strenum import StrEnum

from fastapi_instagram_clone.router.blog_post import required_functionality


router = APIRouter(prefix="/blog", tags=["blog"])


@router.get(
    "/all",
    summary="Retrieve all blogs",
    description="This API call simulates fetching all blogs.",
    response_description="The list of available blogs",
)
@beartype
def get_blogs(
    *,
    page: int = 1,
    page_size: Optional[int] = None,
    req_parameter: dict[str, str] = Depends(required_functionality),
) -> dict[str, Any]:
    return {
        "message": f"All {page_size} blogs on page {page}",
        "req": req_parameter,
    }


@router.get("/{id}/comments/{comment_id}", tags=["comment"])
@beartype
def get_comment(
    *,
    id: int,
    comment_id: int,
    valid: bool = True,
    username: Optional[str] = None,
) -> dict[str, str]:
    """Simulates retrieving a comment of a blog.

    - **id** mandatory path parameter
    - **comment_id** mandatory path parameter
    - **valid** optional query parameter
    - **username** optional query parameter
    """
    return {"message": f"{id=}, {comment_id=}, {valid=}, {username=}"}


class BlogType(StrEnum):
    short = auto()
    story = auto()
    howto = auto()


@router.get("/type/{type}")
@beartype
def get_blog_type(*, type: BlogType) -> dict[str, str]:
    return {"message": f"Blog with {type=}"}


@router.get("/{id}")
@beartype
def get_blog(*, id: int, response: Response) -> dict[str, str]:
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Blog with {id=} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Blog with {id=}"}
