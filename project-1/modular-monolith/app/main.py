from fastapi import FastAPI

from app.database import Base, engine
from app.reporting.routes import router as reporting_router
from app.tasks import models
from app.tasks.routes import router as tasks_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    version="1.0.0"
)

# Register summary before /{task_id}
app.include_router(reporting_router)
app.include_router(tasks_router)


@app.get("/")
def root():
    return {
        "message": "Task Manager API is running"
    }
