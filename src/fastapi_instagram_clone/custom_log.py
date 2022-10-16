from typing import Any
from typing import cast

from beartype import beartype
from fastapi import Request


@beartype
def log(
    *,
    tag: str = "MyApp",
    message: str = "no message",
    request: Request = cast(Any, None),
) -> None:
    with open("log.txt", mode="a+") as fh:
        _ = fh.write(f"{tag}: {message}\n")
        if request is not None:
            _ = fh.write(f"\t{request.url}\n")
