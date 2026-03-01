import pytest
import asyncio
from src.core.event_bus import EventBus


@pytest.mark.asyncio
async def test_event_bus_pub_sub():
    """Tests the asynchronous publishing and subscription process via EventBus."""
    bus = EventBus()
    received_data = []

    async def mock_callback(data):
        received_data.append(data)

    bus.subscribe("TEST_EVENT", mock_callback)

    # Start the listener in the background
    listener_task = asyncio.create_task(bus.start_listening())

    # Publish an event
    await bus.publish("TEST_EVENT", {"msg": "hello"})

    # Wait briefly for processing
    await asyncio.sleep(0.1)

    assert len(received_data) == 1
    assert received_data[0]["msg"] == "hello"

    listener_task.cancel()
