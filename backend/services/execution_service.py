import json

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.workflow import Workflow
from models.workflow_run import WorkflowRun

from executor.executor import (
    WorkflowExecutor
)

from browser.playwright_client import (
    PlaywrightClient
)

from agents.result_formatter.agent import (
    ResultFormatterAgent
)


class ExecutionService:

    # Used by API route
    async def run_workflow(
        self,
        workflow_id: int,
        user_id: int,
        db: Session
    ):

        workflow = db.query(
            Workflow
        ).filter(
            Workflow.id == workflow_id,
            Workflow.user_id == user_id
        ).first()

        if not workflow:

            raise HTTPException(
                status_code=404,
                detail="Workflow not found"
            )

        run = WorkflowRun(
            workflow_id=workflow.id,
            status="running",
            started_at=datetime.utcnow()
        )

        db.add(run)
        db.commit()
        db.refresh(run)

        workflow_json = json.loads(
            workflow.workflow_json
        )

        client = PlaywrightClient()

        (
            playwright,
            browser,
            page
        ) = await client.get_page()

        try:

            executor = WorkflowExecutor()

            print("WORKFLOW JSON:")
            print(workflow_json)

            results = await executor.execute(
                page,
                workflow_json,
                db,
                run.id
            )
            formatter = ResultFormatterAgent()

            formatted_result = formatter.format(
                workflow.prompt,
                workflow.name,
                json.dumps(results)
            )

            run.status = "completed"

            run.completed_at = (
                datetime.utcnow()
            )

            run.duration = (
                run.completed_at -
                run.started_at
            ).total_seconds()

            run.result_json = formatted_result

            db.commit()

            return {
                "success": True,
                "run_id": run.id,
                "workflow_id": workflow.id,
                "workflow_name": workflow.name,
                "status": run.status,
                "duration": run.duration,
                "results": formatted_result
            }

        except Exception as e:

            import traceback
            traceback.print_exc()

            run.status = "failed"

            run.completed_at = (
                datetime.utcnow()
            )

            run.duration = (
                run.completed_at -
                run.started_at
            ).total_seconds()

            run.error_message = str(e)

            db.commit()

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

        finally:

            await browser.close()
            await playwright.stop()

    # Used by scheduler worker
    async def run_scheduled_workflow(
        self,
        workflow_id: int,
        db: Session
    ):

        workflow = db.query(
            Workflow
        ).filter(
            Workflow.id == workflow_id
        ).first()

        if not workflow:

            print(
                f"Workflow {workflow_id} not found"
            )

            return

        return await self.run_workflow(
            workflow_id,
            workflow.user_id,
            db
        )