from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime
)

from core.database import Base


class WorkflowSchedule(Base):
    __tablename__ = "workflow_schedules"

    id = Column(Integer, primary_key=True, index=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id"),
        nullable=False
    )

    schedule_type = Column(
        String(50),
        nullable=False
    )

    run_time = Column(
        String(10)
    )

    day_of_week = Column(
        String(20)
    )

    is_active = Column(
        Boolean,
        default=True
    )

    next_run_at = Column(DateTime)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )