import pytest
from api.AppAPI import ForexAPI
import os
import json

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def forex_api_session():
    print(f"USING BASE URL: {BASE_URL}")
    api_client = ForexAPI(base_url=BASE_URL)
    return api_client


@pytest.fixture(scope='function')
def load_sample_order():
    # load the test sample and pass it to test functions
    json_file_path = 'test_data/new_order_sample.json'
    with open(json_file_path, 'r') as file:
        sample_order = json.load(file)
    return sample_order
