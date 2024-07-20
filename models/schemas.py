from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    stocks: str = Field(None, description="Currency pair symbol (e.g. 'EURUSD'), or any other stuff")
    quantity: float = Field(None, description="Quantity of the currency pair to be traded")


class OrderInput(OrderBase):
    pass


class OrderOutput(OrderBase):
    id: str
    status: str = Field(None, enum=["PENDING", "EXECUTED", "CANCELED"], description="Status of the order")
