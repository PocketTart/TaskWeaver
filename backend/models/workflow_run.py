from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Float
)

from core.database import Base


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id"),
        nullable=False
    )

    status = Column(
        String(50),
        default="pending"
    )

    started_at = Column(DateTime)

    completed_at = Column(DateTime)

    duration = Column(Float)

    result_json = Column(Text)

    error_message = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )