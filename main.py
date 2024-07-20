from fastapi import FastAPI, Request, Response
from routers import orders
import time
import random
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI(title="Forex Trading Platform API",
              version="1.0.0",
              description="A RESTful API to simulate a Forex trading platform with WebSocket support for real-time "
                          "order updates.")

app.include_router(orders.router)


@app.get("/", include_in_schema=False)
async def read_root():
    # healthcheck endpoint
    logger.info("Healthcheck request received")
    return "I live!"


@app.middleware("http")
# middleware decorator to simulate response delay
async def add_delay(request: Request, call_next):
    time.sleep(random.uniform(0.1, 1))
    logger.info(f"Processing request: {request.method} {request.url}")
    response = await call_next(request)
    return response
