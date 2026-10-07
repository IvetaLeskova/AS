from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db

from . import service


class TaskSummary(BaseModel):
    total: int
    todo: int
    done: int


router = APIRouter(
    prefix="/tasks",
    tags=["Reporting"]
)


@router.get(
    "/summary",
    response_model=TaskSummary
)
def get_task_summary(
    db: Session = Depends(get_db)
):
    return service.get_task_summary(db)
