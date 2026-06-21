from datetime import datetime, timedelta

from core.database import SessionLocal

from models.workflow_schedule import WorkflowSchedule

from scheduler.queue import execution_queue


def calculate_next_run(schedule):

    now = datetime.utcnow()

    hour, minute = map(
        int,
        schedule.run_time.split(":")
    )

    if schedule.schedule_type == "daily":

        next_run = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        if next_run <= now:
            next_run += timedelta(days=1)

        return next_run

    if schedule.schedule_type == "weekly":

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
            schedule.day_of_week.lower()
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

    return None


def check_due_workflows():

    db = SessionLocal()

    try:

        schedules = db.query(
            WorkflowSchedule
        ).filter(
            WorkflowSchedule.is_active == True,
            WorkflowSchedule.next_run_at <= datetime.utcnow()
        ).all()

        print(
            f"Found {len(schedules)} due schedules"
        )

        for schedule in schedules:

            execution_queue.put(
                schedule.workflow_id
            )

            print(
                f"Queued workflow {schedule.workflow_id}"
            )

            # move schedule forward immediately
            schedule.next_run_at = (
                calculate_next_run(
                    schedule
                )
            )

        db.commit()

    finally:

        db.close()