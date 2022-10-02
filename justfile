local:
  uvicorn --host=localhost --port=8000 --reload --app-dir=src \
    fastapi_instagram_clone.main:app
