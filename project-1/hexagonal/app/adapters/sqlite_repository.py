import os
from sqlalchemy import Column, String, Text, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from ..domain.task import Task, TaskStatus
Base = declarative_base()
class TaskRow(Base):
    __tablename__='tasks'
    id=Column(String,primary_key=True)
    title=Column(String(120),nullable=False)
    description=Column(Text,nullable=True)
    status=Column(String(10),nullable=False)
    created_at=Column(DateTime(timezone=True),nullable=False)
    updated_at=Column(DateTime(timezone=True),nullable=False)
engine=create_engine(os.getenv('TASK_DB_URL','sqlite:///./tasks.db'),connect_args={'check_same_thread':False})
SessionLocal=sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
def as_task(row):
    return Task(row.id,row.title,row.description,TaskStatus(row.status),row.created_at,row.updated_at) if row else None
class SQLiteTaskRepository:
    def add(self,task):
        with SessionLocal() as db:
            db.add(TaskRow(id=task.id,title=task.title,description=task.description,status=task.status.value,created_at=task.created_at,updated_at=task.updated_at));db.commit()
        return task
    def list(self):
        with SessionLocal() as db:return [as_task(t) for t in db.query(TaskRow).all()]
    def get(self,task_id):
        with SessionLocal() as db:return as_task(db.get(TaskRow,task_id))
    def save(self,task):
        with SessionLocal() as db:
            row=db.get(TaskRow,task.id)
            row.title,row.description,row.status,row.updated_at=task.title,task.description,task.status.value,task.updated_at
            db.commit()
        return task
    def delete(self,task_id):
        with SessionLocal() as db:
            row=db.get(TaskRow,task_id)
            if row:db.delete(row);db.commit()
