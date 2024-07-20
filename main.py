from fastapi import FastAPI
from routers import orders

app = FastAPI(title="Forex Trading Platform API",
              version="1.0.0",
              description="A RESTful API to simulate a Forex trading platform with WebSocket support for real-time "
                          "order updates.")

app.include_router(orders.router)

