from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_user

from models.workflow import Workflow
from models.user import User
from models.workflow_schedule import WorkflowSchedule
from models.workflow_run import WorkflowRun
from models.execution_log import ExecutionLog

from schemas.workflow_schema import WorkflowRequest

from services.workflow_service import WorkflowService


router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)

workflow_service = WorkflowService()


# CREATE WORKFLOW

@router.post("/")
def create_workflow(
    request: WorkflowRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return workflow_service.create_workflow(
        prompt=request.prompt,
        user_id=current_user.id,
        db=db
    )


# GET ALL WORKFLOWS (USER ONLY)

@router.get("")
def get_workflows(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    workflows = db.query(
        Workflow
    ).filter(
        Workflow.user_id == current_user.id
    ).all()

    return workflows


# GET SINGLE WORKFLOW

@router.get("/{workflow_id}")
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    workflow = db.query(
        Workflow
    ).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == current_user.id
    ).first()

    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return workflow


# DELETE WORKFLOW

@router.delete("/{workflow_id}")
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    workflow = db.query(
        Workflow
    ).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == current_user.id
    ).first()

    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    # Fetch all runs for this workflow
    runs = db.query(
        WorkflowRun
    ).filter(
        WorkflowRun.workflow_id == workflow.id
    ).all()

    # Delete execution logs first
    for run in runs:

        db.query(
            ExecutionLog
        ).filter(
            ExecutionLog.run_id == run.id
        ).delete()

    # Delete workflow runs
    db.query(
        WorkflowRun
    ).filter(
        WorkflowRun.workflow_id == workflow.id
    ).delete()

    # Delete workflow schedules
    db.query(
        WorkflowSchedule
    ).filter(
        WorkflowSchedule.workflow_id == workflow.id
    ).delete()

    # Delete workflow
    db.delete(workflow)

    db.commit()

    return {
        "message": "Workflow deleted"
    }