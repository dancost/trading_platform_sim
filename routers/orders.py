import asyncio
import json
import uuid
import re
import logging
from fastapi import APIRouter, HTTPException, status, WebSocketDisconnect, WebSocket
from models.schemas import OrderOutput, OrderInput
from typing import List
from websocket_manager import ConnectionManager

logger = logging.getLogger(__name__)

router = APIRouter()
orders_db = []
websocket_manager = ConnectionManager()


def validate_order(order_input: OrderInput):
    if not re.match("^[A-Z]{3}[A-Z]{3}$", order_input.stocks):
        logger.error(f"Invalid currency pair symbol: {order_input.stocks}")
        raise HTTPException(status_code=400, detail="Invalid currency pair symbol")
    if order_input.quantity <= 0:
        logger.error(f"Order quantity must be greater than zero: {order_input.quantity}")
        raise HTTPException(status_code=400, detail="Order quantity must be greater than zero")


# auto executes pending orders after a delay
async def execute_order(order_id: str, delay: int = 10):
    await asyncio.sleep(delay)
    for order in orders_db:
        if order["id"] == order_id and order["status"] == "PENDING":
            order["status"] = "EXECUTED"
            logger.info(f"Order executed: {order_id}")
            await websocket_manager.broadcast({"action": "order_executed", "data": order}, order_id=order_id)


@router.get("/orders", response_model=List[OrderOutput], status_code=status.HTTP_200_OK)
async def retrieve_all_orders():
    logger.info("Retrieving all orders")
    return orders_db


@router.post("/orders", response_model=OrderOutput, status_code=status.HTTP_201_CREATED)
async def post_order(order_input: OrderInput):
    validate_order(order_input)
    new_order = order_input.dict()
    new_order["id"] = str(uuid.uuid4())
    new_order["status"] = "PENDING"
    orders_db.append(new_order)
    logger.info(f"New order created: {new_order['id']}")
    await websocket_manager.broadcast({"action": "new_order", "data": new_order}, order_id=new_order["id"])

    asyncio.create_task(execute_order(new_order["id"]))

    return OrderOutput(**new_order)


@router.get("/orders/{orderId}", response_model=OrderOutput, status_code=status.HTTP_200_OK)
async def get_order_by_id(orderId: str):
    for order in orders_db:
        if order["id"] == orderId:
            logger.info(f"Retrieving order by ID: {orderId}")
            return OrderOutput(**order)
    logger.error(f"Order not found: {orderId}")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Order not found"
    )


@router.delete("/orders/{orderId}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_an_order(orderId: str):
    for order in orders_db:
        if order["id"] == orderId and order["status"] == "PENDING":
            order["status"] = "CANCELED"
            logger.info(f"Order canceled: {orderId}")
            await websocket_manager.broadcast({"action": "order_cancelled", "data": order}, order_id=orderId)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Order not found or already executed"
    )


@router.websocket("/ws")
async def websocket_connection(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            action = message.get("action")
            order_id = message.get("order_id")
            if action == "subscribe" and order_id:
                websocket_manager.order_subscribers[order_id].add(websocket)
                logger.info(f"WebSocket subscribed to order ID: {order_id}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
