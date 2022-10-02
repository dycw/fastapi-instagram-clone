from typing import NoReturn

from beartype import beartype
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.exc import NoResultFound


@beartype
def handle_no_result_or_multiple_results(
    error: NoResultFound | MultipleResultsFound,
    desc1: str,
    desc2: str,
    value: int | str,
    /,
) -> NoReturn:
    full_desc = f"{desc2}={value}"
    if isinstance(error, NoResultFound):
        detail = f"No {desc1} with {full_desc} not found"
    else:
        detail = f"Multiple {desc1}s with {full_desc} found"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
