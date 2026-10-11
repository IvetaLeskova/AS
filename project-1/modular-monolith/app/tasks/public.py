# Public interface of the Tasks module (no direct database access from Reporting).
from sqlalchemy.orm import Session
from . import repository

def summarize_tasks(db: Session) -> dict:
    tasks = repository.get_tasks(db)
    return {
        'total': len(tasks),
        'todo': sum(t.status.value == 'TODO' for t in tasks),
        'done': sum(t.status.value == 'DONE' for t in tasks),
    }
