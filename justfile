local:
  uvicorn --host=localhost --port=8000 --reload main:app

deta-new:
  deta new --python --name=fastapi-instagram-clone

deploy:
  deta deploy

# OCR

local-ocr:
  uvicorn --host=localhost --port=8000 --reload main_ocr:app

# blog

local-blog:
  uvicorn --host=localhost --port=8000 --reload --app-dir=src blog.main:app
