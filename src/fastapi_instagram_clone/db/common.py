from typing import NoReturn

from beartype import beartype
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.exc import NoResultFound


@beartype
def handle_no_result_or_multiple_results(
    error: NoResultFound | MultipleResultsFound, desc: str, id: int, /
) -> NoReturn:
    if isinstance(error, NoResultFound):
        detail = f"No {desc} with {id=} not found"
    else:
        detail = f"Multiple {desc}s with {id=} found"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
