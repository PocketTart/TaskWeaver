import time

from fastapi import Request


async def request_timer(
    request: Request,
    call_next
):

    start_time = time.perf_counter()

    response = await call_next(
        request
    )

    process_time = (
        time.perf_counter()
        - start_time
    )

    response.headers[
        "X-Process-Time"
    ] = f"{process_time:.4f}"

    print(
        f"[{request.method}] "
        f"{request.url.path} "
        f"completed in "
        f"{process_time:.4f}s"
    )

    return response