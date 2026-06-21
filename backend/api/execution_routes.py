from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_user

from services.execution_service import (
    ExecutionService
)

from models.workflow import Workflow
from models.workflow_run import WorkflowRun


router = APIRouter(
    prefix="/executions",
    tags=["Executions"]
)

execution_service = ExecutionService()


# RUN WORKFLOW

@router.post("/run/{workflow_id}")
async def run_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    return await execution_service.run_workflow(
        workflow_id,
        current_user.id,
        db
    )


# GET ALL EXECUTIONS OF CURRENT USER

@router.get("/history")
def get_execution_history(
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    runs = (
        db.query(
            WorkflowRun
        )
        .join(
            Workflow,
            Workflow.id ==
            WorkflowRun.workflow_id
        )
        .filter(
            Workflow.user_id ==
            current_user.id
        )
        .order_by(
            WorkflowRun.started_at.desc()
        )
        .all()
    )

    return runs


# GET EXECUTION HISTORY OF A WORKFLOW

@router.get(
    "/workflow/{workflow_id}"
)
def get_workflow_runs(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    workflow = db.query(
        Workflow
    ).filter(
        Workflow.id == workflow_id,
        Workflow.user_id ==
        current_user.id
    ).first()

    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    runs = (
        db.query(
            WorkflowRun
        )
        .filter(
            WorkflowRun.workflow_id ==
            workflow_id
        )
        .order_by(
            WorkflowRun.started_at.desc()
        )
        .all()
    )

    return runs


# GET SINGLE EXECUTION

@router.get("/{run_id}")
def get_execution(
    run_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    run = (
        db.query(
            WorkflowRun
        )
        .join(
            Workflow,
            Workflow.id ==
            WorkflowRun.workflow_id
        )
        .filter(
            WorkflowRun.id ==
            run_id,
            Workflow.user_id ==
            current_user.id
        )
        .first()
    )

    if not run:

        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    return run