import asyncio
import random
import time

from prefect.client.orchestration import get_client
from prometheus_client import Counter, Summary, start_http_server

from prefect_prom_exporter.flow_runs import read_flow_runs

c = Counter("my_failures", "Description of counter")


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary(
    "request_processing_seconds", "Time spent processing request"
)


# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)


async def main():
    async with get_client() as client:
        return await read_flow_runs(client=client)


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        c.inc()  # Increment by 1
        c.inc(1.6)  # Increment by given value
        process_request(random.random())

        asyncio.run(main())
