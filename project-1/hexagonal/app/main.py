from fastapi import FastAPI

from app.adapters.api.routes import router
from app.adapters.persistence.database import Base, engine
from app.adapters.persistence import models


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Task Manager API is running"
    }
