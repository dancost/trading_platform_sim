# manage ws connections and order updates
import json
from collections import defaultdict
from fastapi import WebSocket
from typing import Set, Dict
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # initialize and store all active connections
        self.active_connections: Set[WebSocket] = set()
        # store subscribers and order id
        self.order_subscribers: Dict[str, Set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket):
        # accept new connection and add it to active connections
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info("WebSocket connected")

    def disconnect(self, websocket: WebSocket):
        # remove websockets connection from active connections and subscriptions
        self.active_connections.remove(websocket)
        for subscribers in self.order_subscribers.values():
            if websocket in subscribers:
                subscribers.remove(websocket)
        logger.info("WebSocket disconnected")

    async def broadcast(self, message: dict, order_id: str = None):
        # send messages to subscribed clients
        if order_id:
            subscribers = self.order_subscribers[order_id]
            logger.info(f"Broadcasting message to {len(subscribers)} subscriber(s) for order ID: {order_id}")
            for connection in subscribers:
                await connection.send_text(json.dumps(message))
        else:
            logger.info(f"Broadcasting message to {len(self.active_connections)} active connection(s)")
            for connection in self.active_connections:
                await connection.send_text(json.dumps(message))
