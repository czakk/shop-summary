"""Report class."""

import pandas as pd
import pathlib

from datetime import datetime

from src.configs import OrderConfig
from src.constans import TAX_RATE
from src.order import Order


class Report:
    def __init__(
        self,
        path: pathlib.Path,
        date: datetime.date,
    ):
        self.path = path
        self.date: datetime.date = date
        self.orders: list[Order] = []
        self.data: pd.DataFrame = pd.read_excel(self.path, header=0)

    def set_orders(self) -> None:
        rows_to_drop = []
        for index, order in self.data.iterrows():
            try:
                self.orders.append(Order(OrderConfig(**order.to_dict())))
            except ValueError:
                rows_to_drop.append(index)

        self.data.drop(rows_to_drop, inplace=True)

    def set_price_cols(self) -> None:
        self.data['TAX'] = [TAX_RATE for _ in range(len(self.orders))]
        self.data['gross'] = [order.calculate_gross_price() for order in self.orders]
        self.data['total'] = [order.calculate_total_price() for order in self.orders]

    def get_data_with_sum_row(self) -> pd.DataFrame:
        data = self.data.copy()
        cols = data.drop(columns=['id', 'quantity', 'TAX']).select_dtypes(include='number')
        sum_row = cols.sum()
        sum_row['name'] = 'Total'

        return pd.concat([data, pd.DataFrame([sum_row])], ignore_index=True)

    def save(self) -> None:
        self.get_data_with_sum_row().to_excel('./report.xlsx', index=False, header=True)
