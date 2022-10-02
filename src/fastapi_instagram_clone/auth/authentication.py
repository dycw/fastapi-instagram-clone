from typing import Any

from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_instagram_clone.auth.oauth2 import create_access_token
from fastapi_instagram_clone.auth.oauth2 import token_url
from fastapi_instagram_clone.db.database import session
from fastapi_instagram_clone.db.db_user import get_user_by_username
from fastapi_instagram_clone.db.hash import Hash


router = APIRouter(tags=["authentication"])


@router.post(f"/{token_url}")
@beartype
def get_token(
    *,
    request: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(session),
) -> dict[str, Any]:
    username = request.username
    try:
        user = get_user_by_username(session, username)
    except HTTPException:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    if not Hash().verify(user.password, request.password):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )
    access_token = create_access_token({"sub": username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": username,
    }
