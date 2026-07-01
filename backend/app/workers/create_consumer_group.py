from app.core.redis import redis_client

import asyncio


STREAM_NAME = "usage_events_stream"
GROUP_NAME = "usage_workers"


async def main():

    try:

        await redis_client.xgroup_create(
            name=STREAM_NAME,
            groupname=GROUP_NAME,
            id="0",
            mkstream=True
        )

        print("Consumer group created!")

    except Exception as e:

        print(e)


asyncio.run(main())