import asyncio
import json
import pytest
import aiohttp
from websockets import connect


# place order helper
async def place_order(client, base_url, order_data):
    response = await client.post(f"{base_url}/orders", json=order_data)
    response_json = await response.json()
    print(f"Order response: {response_json}")
    return response_json


@pytest.mark.ws
@pytest.mark.asyncio
async def test_websocket_order_status(forex_api_session):
    base_url = forex_api_session.base_url
    uri = f"ws://{base_url.split('//')[1]}/ws"

    async with aiohttp.ClientSession() as client:
        async with connect(uri) as websocket:
            # place an order with a valid currency pair
            order_data = {"stocks": "EURUSD", "quantity": 10}
            order_response = await place_order(client, base_url, order_data)
            print(f"Order response after placing: {order_response}")

            order_id = order_response.get('id')
            print(f"Order ID: {order_id}")
            assert order_id is not None, "Order ID should not be None"

            # start listening ws messages
            pending_message = await websocket.recv()
            pending_data = json.loads(pending_message)
            print(f"Pending message: {pending_data}")

            assert pending_data["data"]["id"] == order_id
            assert pending_data["data"]["status"] == "PENDING"

            # wait for EXECUTED status
            executed_message = await websocket.recv()
            executed_data = json.loads(executed_message)
            print(f"Executed message: {executed_data}")

            assert executed_data["data"]["id"] == order_id
            assert executed_data["data"]["status"] == "EXECUTED"

            await websocket.close()


@pytest.mark.ws
@pytest.mark.asyncio
async def test_no_messages_after_cancelled(forex_api_session):
    base_url = forex_api_session.base_url
    uri = f"ws://{base_url.split('//')[1]}/ws"

    async with aiohttp.ClientSession() as client:
        async with connect(uri) as websocket:
            # place an order with a valid currency pair
            order_data = {"stocks": "EURUSD", "quantity": 10}
            order_response = await place_order(client, base_url, order_data)
            print(f"Order response after placing: {order_response}")

            order_id = order_response.get('id')
            print(f"Order ID: {order_id}")
            assert order_id is not None, "Order ID should not be None"

            # listen for the first message (PENDING status)
            pending_message = await websocket.recv()
            pending_data = json.loads(pending_message)
            print(f"Pending message: {pending_data}")

            assert pending_data["data"]["id"] == order_id
            assert pending_data["data"]["status"] == "PENDING"

            # cancel the order
            cancel_response = await client.delete(f"{base_url}/orders/{order_id}")
            cancel_text = await cancel_response.text()
            print(f"Cancel response: {cancel_text}")
            assert cancel_response.status == 204, f"Failed to cancel order: {cancel_text}"

            # wait for the second message (CANCELLED status)
            cancelled_message = await websocket.recv()
            cancelled_data = json.loads(cancelled_message)
            print(f"Cancelled message: {cancelled_data}")

            assert cancelled_data["data"]["id"] == order_id
            assert cancelled_data["data"]["status"] == "CANCELED"

            # ensure no further messages are received within a reasonable time frame
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(websocket.recv(), timeout=12)

            await websocket.close()
