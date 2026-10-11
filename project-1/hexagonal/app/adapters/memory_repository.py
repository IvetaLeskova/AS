class InMemoryTaskRepository:
    def __init__(self): self.tasks = {}
    def add(self,task): self.tasks[task.id]=task;return task
    def list(self): return list(self.tasks.values())
    def get(self,task_id): return self.tasks.get(task_id)
    def save(self,task): self.tasks[task.id]=task;return task
    def delete(self,task_id): self.tasks.pop(task_id,None)
