from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime
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

class ReplayHistoryModel(Base):
    __tablename__ = "replay_history"
    
    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(Integer, nullable=False)

    replay_method = Column(String, nullable=False)

    replay_url = Column(Text, nullable=False)

    status_code = Column(Integer, nullable=False)

    response_length = Column(Integer, default=False)

    reflection_detected = Column(Boolean, default=False)

    diff_status_changed =  Column(Boolean, default=False)

    diff_body_changed = Column(Boolean, default=False)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    content_type = Column(String, nullable=True)

    redirect_location = Column(Text, nullable=True)

    response_preview = Column(Text, nullable=True)

    response_time = Column(String, nullable=True)
