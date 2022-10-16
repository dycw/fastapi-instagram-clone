import datetime as dt

from pydantic import BaseModel


class PostBase(BaseModel):
    image_url: str
    title: str
    context: str
    creator: str


class PostDisplay(BaseModel):
    id: int
    image_url: str
    title: str
    context: str
    creator: str
    timestamp: dt.datetime

    class Config:
        orm_mode = True
