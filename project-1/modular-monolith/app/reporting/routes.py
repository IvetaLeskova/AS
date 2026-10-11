from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..shared.database import get_db
from ..tasks.public import summarize_tasks
from ..tasks.schemas import TaskSummary
router = APIRouter(prefix='/tasks', tags=['Reporting'])
@router.get('/summary', response_model=TaskSummary)
def summary(db: Session = Depends(get_db)):
    return summarize_tasks(db)
