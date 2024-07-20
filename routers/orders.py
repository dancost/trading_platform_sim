import uuid
from fastapi import APIRouter, HTTPException, status
from models.schemas import OrderOutput, OrderInput
from typing import List

router = APIRouter()

orders_db = []


def validate_order(order: dict):
    return True


@router.get("/orders", response_model=List[OrderOutput], status_code=status.HTTP_200_OK)
async def retrieve_all_orders():
    return orders_db


@router.post("/orders", response_model=OrderOutput, status_code=status.HTTP_201_CREATED)
async def place_a_new_order(order: OrderInput):
    order_data = order.dict()
    if not validate_order(order_data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order data"
        )
    order_id = str(uuid.uuid4())
    order_data["id"] = order_id
    order_data["status"] = "PENDING"
    orders_db.append(order_data)
    return OrderOutput(**order_data)  # converts order_data dict to OrderOutput object


@router.get("/orders/{orderId}", response_model=OrderOutput, status_code=status.HTTP_200_OK)
async def get_order_by_id(orderId: str):
    for order in orders_db:
        if order["id"] == orderId:
            return OrderOutput(**order)  # converts order dict to OrderOutput object
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Order not found"
    )


@router.delete("/orders/{orderId}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_an_order(orderId: str):
    for order in orders_db:
        if order["id"] == orderId and order["status"] == "PENDING":
            order["status"] = "CANCELED"
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Order not found or already executed"
    )
