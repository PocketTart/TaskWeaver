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


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)

    run_id = Column(
        Integer,
        ForeignKey("workflow_runs.id"),
        nullable=False
    )

    step_number = Column(Integer)

    action = Column(String(100))

    status = Column(String(50))

    message = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )