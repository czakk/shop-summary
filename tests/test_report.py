import numpy as np
import pathlib
import unittest.mock
import pandas as pd
import pytest

from datetime import date

from src.report import Report


@pytest.fixture
def data():
    return pd.DataFrame(
        {
            'id': [1, 1, 2],
            'name': ['Product1', 'Product2', 'Product1'],
            'price': [100.0, 150.0, 100.0],
            'quantity': [10, 20, 30]
        }
    )


class TestReport:
    @unittest.mock.patch('pandas.read_excel')
    def get_report(
        self,
        read_excel_mock: unittest.mock.MagicMock,
    ):
        data = pd.DataFrame(
            {
                'id': [1, 1, 2],
                'name': ['Product1', 'Product2', 'Product1'],
                'price': [100.0, 150.0, 100.0],
                'quantity': [10, 20, 30]
            }
        )

        read_excel_mock.return_value = data
        return Report(pathlib.Path('./'), date(2025, 1, 1))

    def test_read_orders(
        self,
        data: pd.DataFrame,
    ):
        report = self.get_report()
        report.set_orders()

        assert len(report.orders) == 3

        for report_order, data_order in zip(report.orders, data.to_dict('records')):
            for attr in data.columns:
                assert getattr(report_order.data, attr) == data_order[attr]

    @pytest.mark.parametrize(
        'data, valid_orders_count',
        [
            (
                pd.DataFrame(
                    {
                        'id': [0.1, 2],
                        'name': ['Product1', 'Product2'],
                        'price': [100, 200],
                        'quantity': [1, 2]
                    }
                ),
                1
            ),
            (
                pd.DataFrame(
                    {
                        'id': [1, 2],
                        'name': ['Product1', 'Product2'],
                        'price': [100, 150],
                        'quantity': [0.1, 1]
                    }
                ),
                1
            ),
            (
                pd.DataFrame(
                    {
                        'id': [1, 2],
                        'name': ['Product1', 'Product2'],
                        'quantity': [1, 2]
                    }
                ),
                0
            ),
            (
                pd.DataFrame(
                    {
                        'id': [1, 2],
                        'namee': ['Product1', 'Product2'],
                        'price': [100, 150],
                        'quantity': [1, 2]
                    }
                ),
                0
            ),
            (
                pd.DataFrame(
                    {
                        'id': [1, 2, 3],
                        'name': ['Product1', '', 'Product2'],
                        'price': [100, '', 150],
                        'quantity': [1, '', 2]
                    }
                ),
                2
            )
        ],
        ids=['Invalid ID type', 'Invalid quantity type', 'Missing col', 'Invalid col name', 'Missing data']
    )
    def test_read_orders_with_invalid_data(
        self,
        data: pd.DataFrame,
        valid_orders_count: int
    ):
        report = self.get_report()
        report.data = data

        report.set_orders()

        assert len(report.orders) == valid_orders_count
        assert len(report.data) == valid_orders_count

    def test_set_price_cols(self):
        expected_data = pd.DataFrame(
            {
                'id': [1, 1, 2],
                'name': ['Product1', 'Product2', 'Product1'],
                'price': [100.0, 150.0, 100.0],
                'quantity': [10, 20, 30],
                'TAX': [.23, .23, .23],
                'gross': [123.0, 184.5, 123.0],
                'total': [1230.0, 3690.0, 3690.0]
            }
        )

        report = self.get_report()
        report.set_orders()
        report.set_price_cols()

        assert report.data.equals(expected_data)

    def test_set_sum_row(self):
        expected_data = pd.DataFrame(
            {
                'id': [1, 1, 2],
                'name': ['Product1', 'Product2', 'Product1'],
                'price': [100.0, 150.0, 100.0],
                'quantity': [10, 20, 30],
                'TAX': [.23, .23, .23],
                'gross': [123.0, 184.5, 123.0],
                'total': [1230.0, 3690.0, 3690.0],
            }
        )
        expected_data.loc[len(expected_data)] = [np.nan, 'Total', 350.0, np.nan, np.nan, 430.5, 8610.0]

        report = self.get_report()
        report.set_orders()
        report.set_price_cols()

        assert report.get_data_with_sum_row().equals(expected_data)

    @unittest.mock.patch('pandas.DataFrame.to_excel')
    def test_save(
        self,
        to_excel_mock: unittest.mock.MagicMock,
    ):
        report = self.get_report()
        report.set_orders()
        report.set_price_cols()

        report.save()

        to_excel_mock.assert_called_once_with('./report.xlsx', index=False, header=True)

