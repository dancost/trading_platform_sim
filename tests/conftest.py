import pytest
from api.AppAPI import ForexAPI

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def forex_api_session():
    api_client = ForexAPI(base_url=BASE_URL)
    return api_client
