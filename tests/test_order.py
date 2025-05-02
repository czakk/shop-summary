from src.configs import OrderConfig
from src.order import Order


class TestOrder:
    def get_order(self):
        return Order(data=OrderConfig(**{
            'id': 1,
            'name': 'Product1',
            'price': 100,
            'quantity': 3,
        }))

    def test_calculate_total_price(self):
        order = self.get_order()
        assert order.calculate_total_price() == 369

    def test_calculate_gross_price(self):
        order = self.get_order()
        assert order.calculate_gross_price() == 123