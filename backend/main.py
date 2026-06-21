import asyncio

asyncio.set_event_loop_policy(
    asyncio.WindowsProactorEventLoopPolicy()
)


from fastapi import FastAPI

from core.database import Base, engine

from models.user import User
from models.workflow import Workflow
from models.workflow_run import WorkflowRun
from models.execution_log import ExecutionLog
from models.workflow_schedule import WorkflowSchedule
from api.workflow_routes import router as workflow_router
from api.auth_routes import router as auth_router
from api.execution_routes import (
    router as execution_router
)
from fastapi.middleware.cors import (
    CORSMiddleware
)


from middleware.request_timer import (
    request_timer
)
from scheduler.scheduler import start_scheduler
app = FastAPI(
    title="TaskWeaver",
    version="1.0.0"
)


app.middleware("http")(
    request_timer
)

# create tables
Base.metadata.create_all(bind=engine)

# include routes
app.include_router(auth_router)
app.include_router(workflow_router)
app.include_router(execution_router)
@app.on_event("startup")
def startup_event():
    start_scheduler()
@app.get("/")
def root():
    return {"message": "TaskWeaver API Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}