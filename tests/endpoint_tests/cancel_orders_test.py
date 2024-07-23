import pytest
import uuid
import time


@pytest.fixture(scope='function')
def setup_new_order(forex_api_session, load_sample_order):
    new_order = load_sample_order
    new_order["stocks"] = "EURUSD"
    new_order["quantity"] = 10
    print(f"Sending request: {new_order}")
    response = forex_api_session.post_orders(order_request=new_order)
    assert response.status_code == 201, f"Failed sending new order request: {response.status_code}"
    print(f"Got API response for new order post during setup: {response.json()}")

    order_data = response.json()
    return order_data


@pytest.mark.smoke
def test_cancel_pending_order(forex_api_session, setup_new_order):
    order_data = setup_new_order

    # check order is in pending status
    get_response = forex_api_session.get_order_by_id(order_id=order_data['id'])
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "PENDING"

    # cancel the newly created order
    delete_response = forex_api_session.delete_order_by_id(order_id=order_data['id'])
    assert delete_response.status_code == 204, f"Expected 204, got {delete_response.status_code}"

    # check order is canceled
    get_response = forex_api_session.get_order_by_id(order_id=order_data['id'])
    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    assert get_response.json()["status"] == "CANCELED"


@pytest.mark.negative
def test_cancel_nonexistent_order(forex_api_session):
    # attempt to cancel an order with a random UUID that doesn't exist
    nonexistent_order_id = str(uuid.uuid4())
    print(f"Sending cancel request for nonexistent order id: {nonexistent_order_id}")
    delete_response = forex_api_session.delete_order_by_id(order_id=nonexistent_order_id)
    assert delete_response.status_code == 404, f"Expected 404, got {delete_response.status_code}"

    error_response = delete_response.json()
    assert error_response["detail"] == "Order not found or already executed"


@pytest.mark.negative
def test_cancel_executed_order(forex_api_session, setup_new_order):
    order_data = setup_new_order

    # wait for the order to be executed
    time.sleep(10)

    # verify the order status is "EXECUTED"
    get_response = forex_api_session.get_order_by_id(order_id=order_data['id'])
    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    assert get_response.json()[
               "status"] == "EXECUTED", f"Expected status 'EXECUTED', got {get_response.json()['status']}"

    # attempt to cancel the executed order
    delete_response = forex_api_session.delete_order_by_id(order_id=order_data['id'])
    assert delete_response.status_code == 404, f"Expected 404, got {delete_response.status_code}"

    error_response = delete_response.json()
    assert error_response["detail"] == "Order not found or already executed"


@pytest.mark.negative
def test_cancel_already_canceled_order(forex_api_session, setup_new_order):
    order_data = setup_new_order

    # cancel the newly created order
    delete_response = forex_api_session.delete_order_by_id(order_id=order_data['id'])
    assert delete_response.status_code == 204, f"Expected 204, got {delete_response.status_code}"

    # attempt to cancel the already canceled order
    delete_response = forex_api_session.delete_order_by_id(order_id=order_data['id'])
    assert delete_response.status_code == 404, f"Expected 404, got {delete_response.status_code}"

    error_response = delete_response.json()
    assert error_response["detail"] == "Order not found or already executed"
