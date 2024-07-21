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
        # open ws connection and set ping interval to None (only way I could stop the server from disconnecting me)
        async with connect(uri, ping_interval=None) as websocket:
            # place 100 orders simultaneously
            tasks = [place_order(client, base_url, order_data) for _ in range(100)]
            start_time = time.time()
            responses = await asyncio.gather(*tasks)
            end_time = time.time()
            print(f"Time to place 100 orders: {end_time - start_time:.2f} seconds")

            # check response
            order_ids = []
            for response in responses:
                assert 'id' in response, f"Response missing 'id': {response}"
                order_ids.append(response['id'])

            print(f"Placed 100 orders successfully.")

            # read ws messages
            pending_timestamps = {}
            executed_timestamps = {}
            for _ in range(200):  # expect 2 msg per order (pending and executed)
                message = await websocket.recv()
                message_data = json.loads(message)
                order_id = message_data['data']['id']
                if message_data['data']['status'] == 'PENDING':
                    pending_timestamps[order_id] = time.time()
                elif message_data['data']['status'] == 'EXECUTED':
                    executed_timestamps[order_id] = time.time()

            # compute delays
            execution_delays = []
            for order_id in order_ids:
                if order_id in pending_timestamps and order_id in executed_timestamps:
                    delay = executed_timestamps[order_id] - pending_timestamps[order_id]
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
