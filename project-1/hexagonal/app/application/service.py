from app.application.ports import TaskRepository
from app.domain.exceptions import TaskNotFoundError
from app.domain.models import TaskStatus


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(
        self,
        title: str,
        description: str | None = None
    ):
        return self.repository.create(
            title,
            description
        )

    def get_tasks(self):
        return self.repository.get_all()

    def get_task(self, task_id: str):
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError(task_id)

        return task

    def update_task(
        self,
        task_id: str,
        title: str | None,
        description: str | None
    ):
        self.get_task(task_id)

        return self.repository.update(
            task_id,
            title,
            description
        )

    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus
    ):
        self.get_task(task_id)

        return self.repository.update_status(
            task_id,
            status
        )

    def delete_task(self, task_id: str):
        self.get_task(task_id)

        self.repository.delete(task_id)

    def get_summary(self):
        return self.repository.get_summary()
