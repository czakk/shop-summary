"""Report class."""

import pandas as pd
import pathlib

from datetime import datetime
from pydantic import ValidationError

from src.configs import OrderConfig
from src.constans import TAX_RATE
from src.order import Order
from src.utils import PROJECT_ROOT_PATH, VALIDATION_ERRORS_DIR_PATH


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
        errors = pd.DataFrame(columns=['index', 'col', 'msg'])

        for index, order in self.data.iterrows():
            try:
                self.orders.append(Order(OrderConfig(**order.to_dict())))
            except ValidationError as e:
                for err in e.errors():
                    errors.loc[len(errors)] = ({
                        'index': index,
                        'col': err.get('loc')[0],
                        'msg': err.get('msg'),
                    })
                rows_to_drop.append(index)

        if not errors.empty:
            errors.to_json(
                path_or_buf=VALIDATION_ERRORS_DIR_PATH / f'{self.path.stem}_errors.json',
                orient='records',
                default_handler=str,
                indent=4,
                index=False,
            )

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

    def get_col_sum_by(self, col_name: str) -> pd.DataFrame:
        return pd.DataFrame(
            self.data.groupby(col_name)['quantity'].sum().sort_values(ascending=False).reset_index()
        )

    def save(self) -> None:
        sheet_name = 'Report'

        with pd.ExcelWriter(path=PROJECT_ROOT_PATH / 'reports' / f'{self.path.stem}_report.xlsx') as writer:
            self.get_data_with_sum_row().to_excel(
                writer,
                sheet_name=sheet_name,
                index=False,
                header=True,
                startrow=1
            )
            self.get_col_sum_by(col_name='name').to_excel(
                writer,
                sheet_name=sheet_name,
                index=False,
                header=True,
                startrow=10
            )

            worksheet = writer.sheets[sheet_name]
            worksheet.cell(row=1, column=1).value = 'Summary for ' + str(self.date)
            worksheet.cell(row=9, column=1).value = 'Most often purchased'
