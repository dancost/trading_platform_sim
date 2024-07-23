import asyncio
import json
import pytest
import aiohttp
from websockets import connect
from statistics import mean, stdev
import time


# place order helper
async def place_order(client, base_url, order_data):
    response = await client.post(f"{base_url}/orders", json=order_data)
    response_json = await response.json()
    return response_json


@pytest.mark.performance
@pytest.mark.asyncio
async def test_performance(forex_api_session):
    base_url = forex_api_session.base_url
    uri = f"ws://{base_url.split('//')[1]}/ws"
    order_data = {"stocks": "EURUSD", "quantity": 10}

    async with aiohttp.ClientSession() as client:
        # open ws connection
        async with connect(uri, ping_interval=None) as websocket:
            # Place 100 orders simultaneously
            tasks = [place_order(client, base_url, order_data) for _ in range(100)]
            start_time = time.time()
            responses = await asyncio.gather(*tasks)
            end_time = time.time()
            print(f"Time to place 100 orders: {end_time - start_time:.2f} seconds")

            # check response and collect order IDs
            order_ids = []
            for response in responses:
                assert 'id' in response, f"Response missing 'id': {response}"
                order_ids.append(response['id'])

            print(f"Placed 100 orders successfully.")

            # subscribe to specific order IDs
            for order_id in order_ids:
                subscribe_message = json.dumps({"action": "subscribe", "order_id": order_id})
                await websocket.send(subscribe_message)

            # read ws messages
            executed_timestamps = {}
            for _ in range(100):  # Expect only the EXECUTED messages
                message = await asyncio.wait_for(websocket.recv(), timeout=20)
                message_data = json.loads(message)
                order_id = message_data['data']['id']
                if message_data['data']['status'] == 'EXECUTED':
                    executed_timestamps[order_id] = time.time()
                    print(f"Executed message for order {order_id}: {message_data}")

            # compute delays
            execution_delays = []
            for order_id in order_ids:
                if order_id in executed_timestamps:
                    delay = executed_timestamps[order_id] - start_time
                    execution_delays.append(delay)
                else:
                    print(f"Missing timestamps for order {order_id}")

            if execution_delays:
                avg_delay = mean(execution_delays)
                stddev_delay = stdev(execution_delays)
                print(f"Average Order Execution Delay: {avg_delay:.2f} seconds")
                print(f"Standard Deviation of Delay: {stddev_delay:.2f} seconds")
            else:
                print("No execution delays were recorded.")
            print(f"Total Time: {end_time - start_time:.2f} seconds")