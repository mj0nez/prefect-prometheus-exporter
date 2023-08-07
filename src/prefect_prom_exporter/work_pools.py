from typing import List

from prefect.client.orchestration import PrefectClient
from prefect.client.schemas.filters import (
    WorkPoolFilter,
    WorkPoolFilterId,
)
from prefect.client.schemas.objects import WorkPool


async def read_work_pools(client: PrefectClient) -> List[WorkPool]:
    return await client.read_work_pools()


async def read_work_pools_of_queues(client: PrefectClient, queues)-> List[WorkPool]:
    pool_ids = [q.work_pool_id for q in queues]
    wp_filter = WorkPoolFilter(id=WorkPoolFilterId(any_=pool_ids))
    return await client.read_work_pools(work_pool_filter=wp_filter)
