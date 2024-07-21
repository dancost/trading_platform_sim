import pytest
from api.AppAPI import ForexAPI
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def forex_api_session():
    print(f"USING BASE URL: {BASE_URL}")
    api_client = ForexAPI(base_url=BASE_URL)
    return api_client
