from sqlalchemy.orm import Session

from . import models, schemas


def create_task(
    db: Session,
    task_data: schemas.TaskCreate
):
    task = models.Task(
        title=task_data.title,
        description=task_data.description
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(db: Session):
    return db.query(models.Task).all()


def get_task(
    db: Session,
    task_id: str
):
    return (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )


def update_task(
    db: Session,
    task: models.Task,
    task_data: schemas.TaskUpdate
):
    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    db.commit()
    db.refresh(task)

    return task


def update_task_status(
    db: Session,
    task: models.Task,
    status: models.TaskStatus
):
    task.status = status

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: models.Task
):
    db.delete(task)
    db.commit()
