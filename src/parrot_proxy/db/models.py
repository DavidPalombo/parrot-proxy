from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from parrot_proxy.db.database import Base

class RequestModel(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)

    method = Column(String, nullable=False)
    path = Column(String, nullable=False)
    version = Column(String, nullable=False)

    headers = Column(Text, nullable=False)
    body = Column(Text, nullable=True)