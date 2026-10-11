from fastapi import FastAPI
from .tasks import models
from .shared.database import Base, engine
from .tasks.routes import router as tasks_router
from .reporting.routes import router as reporting_router
Base.metadata.create_all(bind=engine)
app = FastAPI(title='Task Manager - Modular Monolith', version='1.0')
app.include_router(reporting_router)
app.include_router(tasks_router)
@app.get('/')
def root(): return {'message': 'Task Manager API is running'}
