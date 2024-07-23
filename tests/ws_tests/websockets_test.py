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
            # place order with a valid currency pair
            order_data = {"stocks": "EURUSD", "quantity": 10}
            order_response = await place_order(client, base_url, order_data)
            print(f"Order response after placing: {order_response}")

            order_id = order_response.get('id')
            print(f"Order ID: {order_id}")
            assert order_id is not None, "Order ID should not be None"

            # check the PENDING status from the REST API response
            assert order_response['status'] == 'PENDING', "Initial status is not PENDING"

            # sub to the specific order ID
            subscribe_message = json.dumps({"action": "subscribe", "order_id": order_id})
            await websocket.send(subscribe_message)
            print(f"Subscribed to order ID: {order_id}")

            # check the "EXECUTED" status is received
            executed_message = await asyncio.wait_for(websocket.recv(), timeout=12)
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
            # place order with a valid currency pair
            order_data = {"stocks": "EURUSD", "quantity": 10}
            order_response = await place_order(client, base_url, order_data)
            print(f"Order response after placing: {order_response}")

            order_id = order_response.get('id')
            print(f"Order ID: {order_id}")
            assert order_id is not None, "Order ID should not be None"

            # check the PENDING status from the REST API response
            assert order_response['status'] == 'PENDING', "Initial status is not PENDING"

            # sub to the specific order ID
            subscribe_message = json.dumps({"action": "subscribe", "order_id": order_id})
            await websocket.send(subscribe_message)
            print(f"Subscribed to order ID: {order_id}")

            # cancel the order
            cancel_response = await client.delete(f"{base_url}/orders/{order_id}")
            cancel_text = await cancel_response.text()
            print(f"Cancel response: {cancel_text}")
            assert cancel_response.status == 204, f"Failed to cancel order: {cancel_text}"

            # wait for CANCELLED status
            cancelled_message = await asyncio.wait_for(websocket.recv(), timeout=15)
            cancelled_data = json.loads(cancelled_message)
            print(f"Cancelled message: {cancelled_data}")

            assert cancelled_data["data"]["id"] == order_id
            assert cancelled_data["data"]["status"] == "CANCELED"

            # ensure no more messages are received within a reasonable time frame
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(websocket.recv(), timeout=12)

            await websocket.close()


@pytest.mark.ws
@pytest.mark.asyncio
async def test_multiple_users_notified(forex_api_session):
    base_url = forex_api_session.base_url
    uri = f"ws://{base_url.split('//')[1]}/ws"

    async with aiohttp.ClientSession() as client:
        async with connect(uri) as websocket1, connect(uri) as websocket2:
            order_data = {"stocks": "EURUSD", "quantity": 10}
            order_response = await place_order(client, base_url, order_data)
            print(f"Order response after placing: {order_response}")

            order_id = order_response.get('id')
            print(f"Order ID: {order_id}")
            assert order_id is not None, "Order ID should not be None"

            assert order_response['status'] == 'PENDING', "Initial status is not PENDING"

            subscribe_message = json.dumps({"action": "subscribe", "order_id": order_id})
            await websocket1.send(subscribe_message)
            await websocket2.send(subscribe_message)
            print(f"Subscribed to order ID: {order_id} with both WebSocket clients")

            executed_message1 = await asyncio.wait_for(websocket1.recv(), timeout=12)
            executed_data1 = json.loads(executed_message1)
            print(f"Executed message from websocket1: {executed_data1}")

            executed_message2 = await asyncio.wait_for(websocket2.recv(), timeout=12)
            executed_data2 = json.loads(executed_message2)
            print(f"Executed message from websocket2: {executed_data2}")

            assert executed_data1["data"]["id"] == order_id
            assert executed_data1["data"]["status"] == "EXECUTED"

            assert executed_data2["data"]["id"] == order_id
            assert executed_data2["data"]["status"] == "EXECUTED"

            await websocket1.close()
            await websocket2.close()
