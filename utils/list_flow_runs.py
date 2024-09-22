import asyncio

from prefect import get_client
from prefect.client.schemas.sorting import FlowRunSort


async def get_flow_runs():
    async with get_client() as client:
        result = await client.read_flow_runs(limit=100, sort=FlowRunSort.END_TIME_DESC)
        for flow_run in result:
            print(flow_run.name, flow_run.flow_id, flow_run.created)


if __name__ == "__main__":
    asyncio.run(get_flow_runs())
