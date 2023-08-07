import asyncio
from typing import List

import pydantic
from prefect.client.orchestration import PrefectClient
from prefect.client.schemas.objects import WorkQueue, WorkQueueStatusDetail

"""
queues = await client.match_work_queues([work_queue_prefix])
queues = await client.read_work_queues(work_pool_name=pool)
queues = await client.read_work_queues()

"""


async def read_work_queue(client: PrefectClient, pool) -> List[WorkQueue]:
    return await client.read_work_queues(work_pool_name=pool)
    # queues = await client.read_work_queues()


async def read_work_queue_status(
    client: PrefectClient, work_queue_id
) -> WorkQueueStatusDetail:
    resp = await client._client.get(f"/work_queues/{work_queue_id}/status")
    return pydantic.parse_obj_as(WorkQueueStatusDetail, resp.json())


async def read_work_queues_status(
    client: PrefectClient, work_queues: List[str]
) -> List[WorkQueueStatusDetail]:
    return await asyncio.gather(
        *[
            read_work_queue_status(client, work_queue_id=queue)
            for queue in work_queues
        ]
    )
