from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone

from parrot_proxy.db.database import Base

class RequestModel(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)

    method = Column(String, nullable=False)
    path = Column(String, nullable=False)
    version = Column(String, nullable=False)

    headers = Column(Text, nullable=False)
    body = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))