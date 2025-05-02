"""Data configs."""

import pydantic

from datetime import time


class OrderConfig(pydantic.BaseModel):
    id: pydantic.PositiveInt = pydantic.Field(
        description='Order ID'
    )
    name: str = pydantic.Field(
        description='Product name'
    )
    price: float = pydantic.Field(
        description='Product price (net)'
    )
    quantity: pydantic.PositiveInt = pydantic.Field(
        description='Product quantity',
    )
