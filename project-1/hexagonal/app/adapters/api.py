from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from ..domain.task import TaskStatus, TaskPriority
from ..application.service import TaskService
router=APIRouter(prefix='/tasks',tags=['Tasks'])
class TaskCreate(BaseModel):
    title: str = Field(min_length=1,max_length=120)
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
class TaskUpdate(BaseModel):
    title: str | None = Field(None,min_length=1,max_length=120)
    description: str | None = None
    priority: TaskPriority | None = None
class StatusUpdate(BaseModel): status: TaskStatus
class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
class TaskSummary(BaseModel): total: int;todo: int;done: int
# Dependency is configured by app.main; HTTP is only an adapter.
def get_service() -> TaskService: raise RuntimeError('Service not configured')
@router.get('/summary',response_model=TaskSummary)
def summary(service:TaskService=Depends(get_service)):return service.summary()
@router.post('',response_model=TaskResponse,status_code=201)
def create(data:TaskCreate,service:TaskService=Depends(get_service)):return service.create(data.title,data.description,data.priority)
@router.get('',response_model=list[TaskResponse])
def tasks(service:TaskService=Depends(get_service)):return service.list()
@router.get('/{task_id}',response_model=TaskResponse)
def get(task_id:str,service:TaskService=Depends(get_service)):return service.get(task_id)
@router.patch('/{task_id}',response_model=TaskResponse)
def update(task_id:str,data:TaskUpdate,service:TaskService=Depends(get_service)):return service.update(task_id,data.title,data.description,data.priority)
@router.patch('/{task_id}/status',response_model=TaskResponse)
def update_status(task_id:str,data:StatusUpdate,service:TaskService=Depends(get_service)):return service.status(task_id,data.status)
@router.delete('/{task_id}',status_code=204)
def delete(task_id:str,service:TaskService=Depends(get_service)):
    service.delete(task_id)
    return Response(status_code=204)
