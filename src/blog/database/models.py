from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from blog.database.database import Base


class DbPost(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    title = Column(String)
    context = Column(String)
    creator = Column(String)
    timestamp = Column(DateTime)
