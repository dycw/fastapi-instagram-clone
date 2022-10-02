from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.exc import NoResultFound

from fastapi_instagram_clone.auth.oauth2 import create_access_token
from fastapi_instagram_clone.auth.oauth2 import token_url
from fastapi_instagram_clone.db.database import yield_sess
from fastapi_instagram_clone.db.hash import Hash
from fastapi_instagram_clone.db.models import DbUser
from fastapi_instagram_clone.types import YieldSession


router = APIRouter(tags=["authentication"])


@router.post(f"/{token_url}")
@beartype
def get_token(
    *,
    request: OAuth2PasswordRequestForm = Depends(),
    yield_sess: YieldSession = Depends(yield_sess),
) -> dict[str, str]:
    sess = next(yield_sess)
    username = request.username
    try:
        user = sess.query(DbUser).where(DbUser.username == username).one()
    except (NoResultFound, MultipleResultsFound):
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
