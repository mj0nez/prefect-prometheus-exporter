from typing import List

from prefect.client.orchestration import PrefectClient
from prefect.client.schemas.filters import FlowFilter, FlowRunFilter
from prefect.client.schemas.objects import StateType
from prefect.client.schemas.sorting import FlowRunSort


async def read_flow_runs(
    client: PrefectClient, state_type: List[StateType] = []
):
    # state: List[str] = []
    # state_type: List[StateType] = [StateType.COMPLETED,]
    state_type: List[StateType] = []

    state_filter = {}

    if state_type:
        state_filter["type"] = {"any_": state_type}

    flow_runs = await client.read_flow_runs(
        flow_run_filter=FlowRunFilter(state=state_filter)
        if state_filter
        else None,
        sort=FlowRunSort.EXPECTED_START_TIME_DESC,
    )
    flows_by_id = {
        flow.id: flow
        for flow in await client.read_flows(
            flow_filter=FlowFilter(
                id={"any_": [run.flow_id for run in flow_runs]}
            )
        )
    }
    return flow_runs, flows_by_id
