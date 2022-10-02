import datetime as dt
from typing import Any
from typing import cast

from beartype import beartype
from fastapi.security import OAuth2PasswordBearer
from jose import jwt


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
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
