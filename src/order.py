"""Order class."""

from src.configs import OrderConfig
from src.constans import TAX_RATE


class Order:
    def __init__(
        self,
        data: OrderConfig,
    ):
        self.data: OrderConfig = data

    def calculate_gross_price(self) -> float:
        return self.data.price * (1 + TAX_RATE)

    def calculate_total_price(self) -> float:
        return self.calculate_gross_price() * self.data.quantity
