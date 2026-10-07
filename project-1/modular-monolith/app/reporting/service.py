from sqlalchemy.orm import Session

from app.tasks import models


def get_task_summary(db: Session):
    total = db.query(
        models.Task
    ).count()

    todo = (
        db.query(models.Task)
        .filter(
            models.Task.status
            == models.TaskStatus.TODO
        )
        .count()
    )

    done = (
        db.query(models.Task)
        .filter(
            models.Task.status
            == models.TaskStatus.DONE
        )
        .count()
    )

    return {
        "total": total,
        "todo": todo,
        "done": done
    }
