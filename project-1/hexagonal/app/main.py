import os
from fastapi import FastAPI
from .adapters.api import router, get_service
from .adapters.memory_repository import InMemoryTaskRepository
from .adapters.sqlite_repository import SQLiteTaskRepository
from .application.service import TaskService
repository = InMemoryTaskRepository() if os.getenv('TASK_BACKEND') == 'memory' else SQLiteTaskRepository()
service = TaskService(repository)
app = FastAPI(title='Task Manager - Hexagonal',version='1.0')
app.dependency_overrides[get_service] = lambda: service
app.include_router(router)
@app.get('/')
def root(): return {'message':'Task Manager API is running'}
