from abc import ABC, abstractmethod

from app.domain.models import Task, TaskStatus


class TaskRepository(ABC):

    @abstractmethod
    def create(
        self,
        title: str,
        description: str | None
    ) -> Task:
        pass

    @abstractmethod
    def get_all(self) -> list[Task]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Task | None:
        pass

    @abstractmethod
    def update(
        self,
        task_id: str,
        title: str | None,
        description: str | None
    ) -> Task:
        pass

    @abstractmethod
    def update_status(
        self,
        task_id: str,
        status: TaskStatus
    ) -> Task:
        pass

    @abstractmethod
    def delete(self, task_id: str) -> None:
        pass

    @abstractmethod
    def get_summary(self) -> dict:
        pass
