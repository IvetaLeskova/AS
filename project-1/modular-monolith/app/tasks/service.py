from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import repository, schemas


def create_task(db: Session, task_data: schemas.TaskCreate):
    return repository.create_task(db, task_data)


def get_tasks(db: Session):
    return repository.get_tasks(db)


def get_task(db: Session, task_id: str):
    task = repository.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


def update_task(
    db: Session,
    task_id: str,
    task_data: schemas.TaskUpdate
):
    task = get_task(db, task_id)

    return repository.update_task(
        db,
        task,
        task_data
    )


def update_task_status(
    db: Session,
    task_id: str,
    status_data: schemas.TaskStatusUpdate
):
    task = get_task(db, task_id)

    return repository.update_task_status(
        db,
        task,
        status_data.status
    )


def delete_task(db: Session, task_id: str):
    task = get_task(db, task_id)

    repository.delete_task(db, task)


