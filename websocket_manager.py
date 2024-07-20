# manage ws connections and order updates
import json
from collections import defaultdict
from fastapi import WebSocket
from typing import Set
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    # store active ws connections and subscribers
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.order_subscribers: defaultdict[str, Set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket):
        # add connection and add it to active ws connections
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info("WebSocket connected")

    def disconnect(self, websocket: WebSocket):
        # remove ws connection from active connections and any subscription
        self.active_connections.remove(websocket)
        for subscribers in self.order_subscribers.values():
            if websocket in subscribers:
                subscribers.remove(websocket)
        logger.info("WebSocket disconnected")

    async def broadcast(self, message: dict, order_id: str = None):
        # if an order ID is provided, send the message only to subscribed clients for that order
        if order_id:
            subscribers = self.order_subscribers[order_id]
            logger.info(
                f"Broadcasting message to {len(subscribers)} subscriber(s) for order ID: {order_id}")
            for connection in subscribers:
                await connection.send_text(json.dumps(message))
        else:
            logger.info(f"Broadcasting message to {len(self.active_connections)} active connection(s)")
            for connection in self.active_connections:
                await connection.send_text(json.dumps(message))
