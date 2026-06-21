from pydantic import BaseModel
from typing import List, Optional


class WorkflowRequest(BaseModel):
    prompt: str


class WorkflowStep(BaseModel):
    action: str
    url: Optional[str] = None
    query: Optional[str] = None
    target: Optional[str] = None


class WorkflowResponse(BaseModel):
    workflow_name: str
    execution_type: str
    schedule: Optional[dict] = None
    steps: List[WorkflowStep]