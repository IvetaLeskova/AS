from datetime import datetime, timezone
from uuid import uuid4
from fastapi import HTTPException
from ..domain.task import Task, TaskStatus
from ..domain.ports import TaskRepository
class TaskService:
    def __init__(self, repo: TaskRepository): self.repo = repo
    def create(self, title: str, description: str | None) -> Task:
        now = datetime.now(timezone.utc)
        return self.repo.add(Task(str(uuid4()), title, description, TaskStatus.TODO, now, now))
    def list(self): return self.repo.list()
    def get(self, task_id: str):
        task = self.repo.get(task_id)
        if task is None: raise HTTPException(status_code=404, detail='Task not found')
        return task
    def update(self, task_id: str, title: str | None, description: str | None):
        task = self.get(task_id)
        if title is not None: task.title = title
        if description is not None: task.description = description
        task.updated_at = datetime.now(timezone.utc)
        return self.repo.save(task)
    def status(self, task_id: str, status: TaskStatus):
        task = self.get(task_id);task.status = status;task.updated_at = datetime.now(timezone.utc)
        return self.repo.save(task)
    def delete(self, task_id: str):
        self.get(task_id);self.repo.delete(task_id)
    def summary(self):
        tasks=self.repo.list()
        return {'total':len(tasks),'todo':sum(t.status == TaskStatus.TODO for t in tasks),'done':sum(t.status == TaskStatus.DONE for t in tasks)}
