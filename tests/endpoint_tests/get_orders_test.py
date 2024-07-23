import pytest


@pytest.fixture(scope='function')
def setup_new_order(forex_api_session, load_sample_order):
    new_order = load_sample_order
    # modify test sample
    new_order["stocks"] = "EURUSD"
    new_order["quantity"] = 10
    print(f"Sending request: {new_order}")
    new_order_request = forex_api_session.post_orders(order_request=new_order)
    assert new_order_request.status_code == 201, (f"Failed sending new order request: "
                                                  f"{new_order_request.status_code, new_order_request.content}")

    print(f"Got API response for new order post during setup: {new_order_request.json()}")

    order_stock, order_quantity, order_id, order_status = (new_order_request.json()["stocks"],
                                                           new_order_request.json()["quantity"],
                                                           new_order_request.json()["id"],
                                                           new_order_request.json()["status"])

    return order_stock, order_quantity, order_id, order_status


@pytest.mark.smoke
def test_get_all_orders(forex_api_session, setup_new_order):
    order_stock, order_quantity, order_id, order_status = setup_new_order
    api_response = forex_api_session.get_orders()
    assert api_response.status_code == 200, (f"Failed to retrieve orders: "
                                             f"{api_response.status_code, api_response.content}")

    print(f"Get all orders response: {api_response.json()}")

    assert order_id in [item["id"] for item in api_response.json()], (f"New order with id {order_id} "
                                                                      f"missing from api response")
    errors = []
    # iterate through response elements and store all errors instead of failing at first assert
    for item in api_response.json():
        if item["id"] == order_id:
            if item["stocks"] != order_stock:
                errors.append(f"Wrong stock in api response. Expected {order_stock} but got {item['stocks']}")
            if item["quantity"] != order_quantity:
                errors.append(
                    f"Wrong order quantity in api response. Expected {order_quantity} but got {item['quantity']}")
            if item["status"] not in (order_status, "EXECUTED"):
                errors.append(
                    f"Wrong status in api response. Expected {order_status} or EXECUTED but got {item['status']}")

    # check no errors encountered
    assert len(errors) == 0, f"Found errors: {errors}"


@pytest.mark.smoke
def test_get_order_by_id(forex_api_session, setup_new_order):
    order_stock, order_quantity, order_id, order_status = setup_new_order
    api_response = forex_api_session.get_order_by_id(order_id)
    assert api_response.status_code == 200, (f"Failed to retrieve order by id: "
                                             f"{api_response.status_code, api_response.content}")

    # save json response
    order_data = api_response.json()
    errors = []

    # # iterate through response elements and store all errors instead of failing at first assert
    if order_data["id"] != order_id:
        errors.append(f"Order ID mismatch. Expected {order_id} but got {order_data['id']}")
    if order_data["stocks"] != order_stock:
        errors.append(f"Stock mismatch. Expected {order_stock} but got {order_data['stocks']}")
    if order_data["quantity"] != order_quantity:
        errors.append(f"Quantity mismatch. Expected {order_quantity} but got {order_data['quantity']}")
    if order_data["status"] != order_status:
        errors.append(f"Status mismatch. Expected {order_status} but got {order_data['status']}")

    # check no errors encountered
    assert len(errors) == 0, f"Found errors: {errors}"


@pytest.mark.negative
def test_get_order_bad_id(forex_api_session, setup_new_order):
    import uuid
    bad_uuid = uuid.uuid4()
    api_response = forex_api_session.get_order_by_id(bad_uuid)
    assert api_response.status_code == 404, f"Got api response: {api_response.status_code} for order id: {bad_uuid}"
    assert api_response.json()["detail"] == "Order not found"
