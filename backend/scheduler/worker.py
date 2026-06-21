import threading
import asyncio

from core.database import SessionLocal

from scheduler.queue import (
    execution_queue
)

from services.execution_service import (
    ExecutionService
)


def worker():

    print("Worker started")

    while True:

        workflow_id = execution_queue.get()

        print(
            f"Executing workflow {workflow_id}"
        )

        db = SessionLocal()

        try:

            service = ExecutionService()

            asyncio.run(
                service.run_scheduled_workflow(
                    workflow_id,
                    db
                )
            )

        except Exception as e:

            print(
                f"Worker error: {e}"
            )

        finally:

            db.close()

        execution_queue.task_done()


def start_worker():

    thread = threading.Thread(
        target=worker,
        daemon=True
    )

    thread.start()