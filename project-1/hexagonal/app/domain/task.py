from dataclasses import dataclass
from datetime import datetime
from enum import Enum
class TaskStatus(str, Enum):
    TODO = 'TODO'
    DONE = 'DONE'
class TaskPriority(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


@dataclass
class Task:
    id: str
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    priority: TaskPriority = TaskPriority.MEDIUM
