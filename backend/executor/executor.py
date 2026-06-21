from executor.action_registry import (
    ACTION_REGISTRY
)

import executor.actions.goto_action
import executor.actions.click_action
import executor.actions.fill_action
import executor.actions.wait_action
import executor.actions.extract_action
import executor.actions.save_results_action
import executor.actions.search_action

from models.execution_log import (
    ExecutionLog
)


class WorkflowExecutor:

    async def execute(
        self,
        page,
        workflow,
        db=None,
        run_id=None
    ):

        results = []

        for index, step in enumerate(
            workflow["steps"],
            start=1
        ):

            action = step["action"]

            print(
                "ACTION_REGISTRY =",
                ACTION_REGISTRY
            )

            print(
                "ACTION =",
                action
            )

            handler = ACTION_REGISTRY.get(
                action
            )

            if not handler:

                if db and run_id:

                    db.add(
                        ExecutionLog(
                            run_id=run_id,
                            step_number=index,
                            action=action,
                            status="failed",
                            message=f"Unknown action: {action}"
                        )
                    )

                    db.commit()

                raise Exception(
                    f"Unknown action: {action}"
                )

            try:

                result = await handler(
                    page,
                    step
                )

                results.append(
                    result
                )

                if db and run_id:

                    db.add(
                        ExecutionLog(
                            run_id=run_id,
                            step_number=index,
                            action=action,
                            status=result.get(
                                "status",
                                "success"
                            ),
                            message=f"{action} executed successfully"
                        )
                    )

                    db.commit()

            except Exception as e:

                if db and run_id:

                    db.add(
                        ExecutionLog(
                            run_id=run_id,
                            step_number=index,
                            action=action,
                            status="failed",
                            message=str(e)
                        )
                    )

                    db.commit()

                raise e

        return results