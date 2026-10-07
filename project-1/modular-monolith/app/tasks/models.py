import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, String, Text
from sqlalchemy.sql import func

from app.database import Base


class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    DONE = "DONE"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    title = Column(
        String(120),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    status = Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.TODO
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
