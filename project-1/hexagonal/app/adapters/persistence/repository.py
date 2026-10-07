from sqlalchemy.orm import Session

from app.application.ports import TaskRepository
from app.domain.models import Task, TaskStatus

from .models import TaskORM


class SQLAlchemyTaskRepository(TaskRepository):

    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, orm_task: TaskORM) -> Task:
        return Task(
            id=orm_task.id,
            title=orm_task.title,
            description=orm_task.description,
            status=orm_task.status,
            created_at=orm_task.created_at,
            updated_at=orm_task.updated_at
        )

    def create(
        self,
        title: str,
        description: str | None
    ) -> Task:
        task = TaskORM(
            title=title,
            description=description
        )

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return self._to_domain(task)

    def get_all(self) -> list[Task]:
        tasks = self.db.query(TaskORM).all()

        return [
            self._to_domain(task)
            for task in tasks
        ]

    def get_by_id(self, task_id: str) -> Task | None:
        task = (
            self.db.query(TaskORM)
            .filter(TaskORM.id == task_id)
            .first()
        )

        if task is None:
            return None

        return self._to_domain(task)

    def update(
        self,
        task_id: str,
        title: str | None,
        description: str | None
    ) -> Task:
        task = (
            self.db.query(TaskORM)
            .filter(TaskORM.id == task_id)
            .first()
        )

        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        self.db.commit()
        self.db.refresh(task)

        return self._to_domain(task)

    def update_status(
        self,
        task_id: str,
        status: TaskStatus
    ) -> Task:
        task = (
            self.db.query(TaskORM)
            .filter(TaskORM.id == task_id)
            .first()
        )

        task.status = status

        self.db.commit()
        self.db.refresh(task)

        return self._to_domain(task)

    def delete(self, task_id: str) -> None:
        task = (
            self.db.query(TaskORM)
            .filter(TaskORM.id == task_id)
            .first()
        )

        self.db.delete(task)
        self.db.commit()

    def get_summary(self) -> dict:
        total = self.db.query(TaskORM).count()

        todo = (
            self.db.query(TaskORM)
            .filter(TaskORM.status == TaskStatus.TODO)
            .count()
        )

        done = (
            self.db.query(TaskORM)
            .filter(TaskORM.status == TaskStatus.DONE)
            .count()
        )

        return {
            "total": total,
            "todo": todo,
            "done": done
        }
