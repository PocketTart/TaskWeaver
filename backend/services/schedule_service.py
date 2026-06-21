from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from models.workflow_schedule import (
    WorkflowSchedule
)


class ScheduleService:

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

    def get_due_schedules(
        self,
        db: Session
    ):

        return db.query(
            WorkflowSchedule
        ).filter(
            WorkflowSchedule.is_active == True,
            WorkflowSchedule.next_run_at <= datetime.utcnow()
        ).all()

    def update_next_run(
        self,
        schedule: WorkflowSchedule,
        db: Session
    ):

        schedule.next_run_at = (
            self.calculate_next_run(
                schedule.schedule_type,
                schedule.run_time,
                schedule.day_of_week
            )
        )

        db.commit()

    def pause_schedule(
        self,
        schedule: WorkflowSchedule,
        db: Session
    ):

        schedule.is_active = False

        db.commit()

    def resume_schedule(
        self,
        schedule: WorkflowSchedule,
        db: Session
    ):

        schedule.is_active = True

        db.commit()