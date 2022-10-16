from shutil import copyfileobj
from typing import Any

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from pytesseract import image_to_string


app = FastAPI()


@app.post("/ocr")
# @beartype
def ocr(image: UploadFile = File(...)) -> Any:
    file_path = "txtFile"
    with open(file_path, mode="w+b") as buffer:
        copyfileobj(image.file, buffer)
    return image_to_string(file_path, lang="eng")
