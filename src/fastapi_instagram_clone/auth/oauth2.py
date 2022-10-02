import datetime as dt
from typing import Any
from typing import cast

from beartype import beartype
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose.jwt import decode
from jose.jwt import encode
from sqlalchemy.orm import Session

from fastapi_instagram_clone.db.database import session
from fastapi_instagram_clone.db.db_user import get_user_by_username
from fastapi_instagram_clone.db.models import DbUser


token_url = "token"  # noqa: S105
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)


SECRET_KEY = (
    "6a0ea2dd4fa6c66d9bc4a6255a3ed6186a0b45b46c0ad2b9fb5bd03845208e37"  # noqa
    # openssl rand -hex 32
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@beartype
def create_access_token(
    data: dict[str, str], expires_delta: dt.timedelta = dt.timedelta(minutes=15)
) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + expires_delta
    to_encode.update({"exp": cast(Any, expire)})
    return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@beartype
def get_current_user(
    *, token: str = Depends(oauth2_scheme), session: Session = Depends(session)
) -> DbUser:
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if (username := payload.get("sub")) is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    try:
        return get_user_by_username(session, username)
    except HTTPException:
        raise credentials_exception
