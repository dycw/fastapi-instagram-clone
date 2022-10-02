from pathlib import Path
from shutil import copyfileobj
from typing import Any

from beartype import beartype
from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import FileResponse


router = APIRouter(prefix="/file", tags=["file"])


@router.post("/file")
@beartype
def get_file(*, file: bytes = File(...)) -> dict[str, Any]:
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"lines": lines}


@router.post("/uploadfile")
# @beartype
def get_uploadfile(*, uploadfile: UploadFile = File(...)) -> dict[str, str]:
    filename = uploadfile.filename
    path = Path("files", filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, mode="wb") as buffer:
        copyfileobj(uploadfile.file, buffer)
    return {"filename": filename, "type": uploadfile.content_type}


@router.get("/download/{name}", response_class=FileResponse)
@beartype
def download_file(*, name: str) -> Path:
    return Path("files", name)
