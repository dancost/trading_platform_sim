import pytest


@pytest.mark.smoke
@pytest.mark.parametrize("quantity", [10, 10.5])
def test_post_new_order(forex_api_session, load_sample_order, quantity):
    # update test sample with valid data
    new_order = load_sample_order
    new_order["stocks"] = "EURUSD"
    new_order["quantity"] = quantity

    # send the new order request
    print(f"Sending new order request with body: {new_order}")
    new_order_request = forex_api_session.post_orders(order_request=new_order)

    errors = []

    # check order created
    assert new_order_request.status_code == 201

    order_data = new_order_request.json()

    # iterate through response elements and store all errors instead of failing at first assert
    if order_data["stocks"] != new_order["stocks"]:
        errors.append(f"Stock mismatch. Expected {new_order['stocks']} but got {order_data['stocks']}")
    if order_data["quantity"] != new_order["quantity"]:
        errors.append(f"Quantity mismatch. Expected {new_order['quantity']} but got {order_data['quantity']}")
    if "id" not in order_data:
        errors.append("Order ID missing in response.")
    if "status" not in order_data:
        errors.append("Order status missing in response.")

    # check no errors encountered
    assert len(errors) == 0, f"Found errors: {errors}"


@pytest.mark.negative
@pytest.mark.parametrize("invalid_stocks, expected_detail", [
    ("", "Invalid currency pair symbol"),
    ("EURUSDFFA", "Invalid currency pair symbol"),
])
def test_post_new_order_invalid_symbol(forex_api_session, invalid_stocks, expected_detail):
    # create an invalid order request
    invalid_order = {
        "stocks": invalid_stocks,
        "quantity": 1
    }

    print(f"Sending order with bad symbol {invalid_order}")

    new_order_request = forex_api_session.post_orders(order_request=invalid_order)
    assert new_order_request.status_code == 400, (f"Expected status code 400 for invalid data, got: "
                                                  f"{new_order_request.status_code}")

    error_response = new_order_request.json()
    assert error_response["detail"] == expected_detail


@pytest.mark.negative
@pytest.mark.parametrize("invalid_quantity, expected_detail", [
    (0, "Order quantity must be greater than zero"),
    (-10, "Order quantity must be greater than zero"),
    ("eurusd", "Order quantity must be an integer"),
])
def test_post_new_order_invalid_quantity(forex_api_session, invalid_quantity, expected_detail):
    # the case where the quantity is a string will fail on purpose for demo reasons
    # create an invalid order request
    invalid_order = {
        "stocks": "EURUSD",
        "quantity": invalid_quantity
    }

    print(f"Sending order with bad quantity {invalid_order}")

    new_order_request = forex_api_session.post_orders(order_request=invalid_order)
    assert new_order_request.status_code == 400, (f"Expected status code 400 for invalid data, got: "
                                                  f"{new_order_request.status_code}")

    error_response = new_order_request.json()
    assert error_response["detail"] == expected_detail
