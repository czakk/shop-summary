"""Data configs."""

import pydantic

from datetime import time


class OrderConfig(pydantic.BaseModel):
    id: pydantic.PositiveInt = pydantic.Field(
        description='Order ID'
    )
    name: str = pydantic.Field(
        description='Product name',
        min_length=3,
        max_length=48,
    )
    price: pydantic.PositiveFloat = pydantic.Field(
        description='Product price (net)',
    )
    quantity: pydantic.PositiveInt = pydantic.Field(
        description='Product quantity',
    )
