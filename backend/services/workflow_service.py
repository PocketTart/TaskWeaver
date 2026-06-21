import json

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from models.workflow import Workflow
from models.workflow_schedule import WorkflowSchedule

from agents.workflow_generator.agent import (
    WorkflowGeneratorAgent
)

from agents.workflow_generator.parser import (
    parse_workflow
)

from agents.workflow_validator.agent import (
    WorkflowValidatorAgent
)


class WorkflowService:

    def __init__(self):

        self.generator = WorkflowGeneratorAgent()
        self.validator = WorkflowValidatorAgent()

    # Calculate next execution time
    def calculate_next_run(
        self,
        schedule_type: str,
        run_time: str,
        day_of_week: str = None
    ):

        now = datetime.utcnow()


        hour, minute = map(
            int,
            run_time.split(":")
        )

        # Daily schedule
        if schedule_type == "daily":

            next_run = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

            if next_run <= now:
                next_run += timedelta(days=1)

            return next_run

        # Weekly schedule
        if schedule_type == "weekly":

            days = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4,
                "saturday": 5,
                "sunday": 6
            }

            target_day = days[
                day_of_week.lower()
            ]

            current_day = now.weekday()

            days_ahead = (
                target_day - current_day
            ) % 7

            next_run = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            ) + timedelta(
                days=days_ahead
            )

            if next_run <= now:
                next_run += timedelta(days=7)

            return next_run

    def create_workflow(
        self,
        prompt: str,
        user_id: int,
        db: Session
    ):

        # Generate workflow
        raw_output = self.generator.generate(
            prompt
        )

        print("\nRAW OUTPUT:")
        print(raw_output)

        # Parse workflow
        workflow_json = parse_workflow(
            raw_output
        )

        if "error" in workflow_json:

            return {
                "success": False,
                "error": workflow_json["error"],
                "raw_response": workflow_json[
                    "raw_response"
                ]
            }

        # Validate workflow
        validation = self.validator.validate(
            workflow_json
        )

        if not validation.get("valid"):

            return {
                "success": False,
                "error": validation.get(
                    "message",
                    "Validation failed"
                )
            }

        workflow_data = validation[
            "workflow"
        ]

        # Save workflow
        workflow = Workflow(
            user_id=user_id,
            name=workflow_data[
                "workflow_name"
            ],
            prompt=prompt,
            workflow_json=json.dumps(
                workflow_data
            )
        )

        db.add(workflow)
        db.commit()
        db.refresh(workflow)

        # Save schedule if needed
        if (
            workflow_data[
                "execution_type"
            ] == "scheduled"
            and "schedule" in workflow_data
        ):

            schedule_type = workflow_data[
                "schedule"
            ]["type"]

            run_time = workflow_data[
                "schedule"
            ].get("time")

            day_of_week = workflow_data[
                "schedule"
            ].get("day_of_week")

            # Calculate first execution time
            next_run_at = self.calculate_next_run(
                schedule_type,
                run_time,
                day_of_week
            )

            schedule = WorkflowSchedule(
                workflow_id=workflow.id,
                schedule_type=schedule_type,
                run_time=run_time,
                day_of_week=day_of_week,
                next_run_at=next_run_at
            )

            db.add(schedule)
            db.commit()

        return {
            "success": True,
            "workflow_id": workflow.id,
            "workflow_name": workflow.name,
            "execution_type": workflow_data[
                "execution_type"
            ]
        }