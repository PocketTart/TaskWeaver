from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from scheduler.poller import (
    check_due_workflows
)
from scheduler.worker import (
    start_worker
)
scheduler = BackgroundScheduler()


def start_scheduler():

    if not scheduler.running:
        start_worker()

        scheduler.add_job(
            check_due_workflows,
            "interval",
            minutes=5
        )
        
        scheduler.start()

        print(
            "Scheduler started"
        )