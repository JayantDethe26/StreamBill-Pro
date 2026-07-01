import asyncio
from uuid import UUID
import os
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_client
from app.db.session import AsyncSessionLocal
from app.models.usage_event import UsageEvent

STREAM_NAME = "usage_events_stream"
GROUP_NAME = "usage_workers"

CONSUMER_NAME = os.getenv(
    "WORKER_NAME",
    "worker_1"
)

BATCH_SIZE = 2


async def process_events(
    db: AsyncSession,
    events
):
    usage_events = []
    stream_ids = []

    for _, stream_events in events:

        for stream_id, data in stream_events:

            stream_ids.append(stream_id)

            usage_events.append(
                UsageEvent(
                event_id=data["event_id"],
                organization_id=UUID(data["organization_id"]),
                customer_id=UUID(data["customer_id"]),
                product_id=UUID(data["product_id"]),
                quantity=int(data["quantity"]),
                event_type=data["event_type"]
            )
            )

    try:

        db.add_all(usage_events)

        await db.commit()

        for stream_id in stream_ids:

            await redis_client.xack(
                STREAM_NAME,
                GROUP_NAME,
                stream_id
            )

        print(
            f"✅ Processed {len(stream_ids)} events successfully."
        )

    except Exception as e:

        await db.rollback()

        print("❌ Failed to process batch")
        print(e)

        # Do NOT acknowledge the events.
        # Redis will redeliver them later.


async def main():

    print("🚀 Usage Event Worker Started...")

    while True:

        try:

            events = await redis_client.xreadgroup(
                groupname=GROUP_NAME,
                consumername=CONSUMER_NAME,
                streams={
                    STREAM_NAME: ">"
                },
                count=BATCH_SIZE,
                block=5000
            )

            if not events:
                continue

            async with AsyncSessionLocal() as db:

                await process_events(
                    db,
                    events
                )

        except Exception as e:

            print("❌ Worker Error")
            print(e)

            # Prevents the worker from crashing
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())