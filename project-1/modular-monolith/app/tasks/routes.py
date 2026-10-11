from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from . import schemas, service
from ..shared.database import get_db


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    return service.create_task(db, task_data)


@router.get(
    "",
    response_model=list[schemas.TaskResponse]
)
def get_tasks(
    db: Session = Depends(get_db)
):
    return service.get_tasks(db)


@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    return service.get_task(db, task_id)


@router.patch(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: str,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    return service.update_task(
        db,
        task_id,
        task_data
    )


@router.patch(
    "/{task_id}/status",
    response_model=schemas.TaskResponse
)
def update_task_status(
    task_id: str,
    status_data: schemas.TaskStatusUpdate,
    db: Session = Depends(get_db)
):
    return service.update_task_status(
        db,
        task_id,
        status_data
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    service.delete_task(db, task_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
