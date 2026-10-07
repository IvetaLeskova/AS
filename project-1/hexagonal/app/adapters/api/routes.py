from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.adapters.persistence.database import get_db
from app.adapters.persistence.repository import SQLAlchemyTaskRepository
from app.application.service import TaskService
from app.domain.exceptions import TaskNotFoundError

from . import schemas


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


def get_service(
    db: Session = Depends(get_db)
):
    repository = SQLAlchemyTaskRepository(db)

    return TaskService(repository)


@router.get(
    "/summary",
    response_model=schemas.TaskSummary
)
def get_summary(
    service: TaskService = Depends(get_service)
):
    return service.get_summary()


@router.post(
    "",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: schemas.TaskCreate,
    service: TaskService = Depends(get_service)
):
    return service.create_task(
        task_data.title,
        task_data.description
    )


@router.get(
    "",
    response_model=list[schemas.TaskResponse]
)
def get_tasks(
    service: TaskService = Depends(get_service)
):
    return service.get_tasks()


@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task(
    task_id: str,
    service: TaskService = Depends(get_service)
):
    try:
        return service.get_task(task_id)

    except TaskNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


@router.patch(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: str,
    task_data: schemas.TaskUpdate,
    service: TaskService = Depends(get_service)
):
    try:
        return service.update_task(
            task_id,
            task_data.title,
            task_data.description
        )

    except TaskNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


@router.patch(
    "/{task_id}/status",
    response_model=schemas.TaskResponse
)
def update_task_status(
    task_id: str,
    status_data: schemas.TaskStatusUpdate,
    service: TaskService = Depends(get_service)
):
    try:
        return service.update_task_status(
            task_id,
            status_data.status
        )

    except TaskNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: str,
    service: TaskService = Depends(get_service)
):
    try:
        service.delete_task(task_id)

    except TaskNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
