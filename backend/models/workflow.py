from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime
)

from core.database import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    name = Column(String(255), nullable=False)

    prompt = Column(Text, nullable=False)

    workflow_json = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )