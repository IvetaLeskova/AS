from fastapi import FastAPI

from . import models
from .database import Base, engine
from .routes import router


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