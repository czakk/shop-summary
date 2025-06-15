import numpy as np
import pathlib
import unittest.mock

import pandas as pd
import pytest

from datetime import datetime

from src.constans import DATE_FORMAT
from src.report import Report
from src.utils import PROJECT_ROOT_PATH, VALIDATION_ERRORS_DIR_PATH


TEST_REPORT_PATH = pathlib.Path(PROJECT_ROOT_PATH / 'data' / '2025_01_01.xlsx')


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
        return Report(TEST_REPORT_PATH, datetime.strptime(TEST_REPORT_PATH.stem, DATE_FORMAT).date())

    def test_read_orders(self):
        data = pd.DataFrame(
                    {
                        'id': [1, 1, 2],
                        'name': ['Product1', 'Product2', 'Product1'],
                        'price': [100.0, 150.0, 100.0],
                        'quantity': [10, 20, 30]
                    }
                )
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
        ids=[
            'Invalid ID type',
            'Invalid quantity type',
            'Missing col',
            'Invalid col name',
            'Missing data'
        ]
    )
    @unittest.mock.patch('pandas.io.json.to_json')
    def test_read_orders_with_invalid_data(
        self,
        to_json_mock: unittest.mock.MagicMock,
        data: pd.DataFrame,
        valid_orders_count: int
    ):
        report = self.get_report()
        report.data = data

        report.set_orders()

        assert len(report.orders) == valid_orders_count
        assert len(report.data) == valid_orders_count
        to_json_mock.assert_called_once()

    @pytest.mark.parametrize(
        'data, expected_errors_dataframe',
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
                pd.DataFrame(
                    {
                        'index': [0],
                        'col': ['id'],
                        'msg': ['Input should be a valid integer, got a number with a fractional part']
                    }
                )
            ),
            (
                pd.DataFrame(
                    {
                        'id': [1, 2, 3],
                        'name': ['Product1', np.nan, 'P2'],
                        'price': [100, np.nan, 150],
                        'quantity': [1, np.nan, 2]
                    }
                ),
                pd.DataFrame(
                    {
                        'index': [1, 1, 1, 2],
                        'col': ['name', 'price', 'quantity', 'name'],
                        'msg': [
                            'Input should be a valid string',
                            'Input should be greater than 0',
                            'Input should be a finite number',
                            'String should have at least 3 characters'
                        ]
                    }
                )
            ),
            (
                pd.DataFrame(
                    {
                        'id': [-1, -2],
                        'name': ['Product1', 'Product2'],
                        'price': [100, 150],
                        'quantity': [1, 2]
                    }
                ),
                pd.DataFrame(
                    {
                        'index': [0, 1],
                        'col': ['id', 'id'],
                        'msg': ['Input should be greater than 0', 'Input should be greater than 0']
                    }
                )
            ),
            (
                pd.DataFrame(
                    {
                        'id': [1, 2],
                        'name': ['Product1', 'Product2'],
                        'quantity': [1, 2]
                    }
                ),
                pd.DataFrame(
                    {
                        'index': [0, 1],
                        'col': ['price', 'price'],
                        'msg': ['Field required', 'Field required']
                    }
                )
            ),
            (
                pd.DataFrame(
                    {
                        'id': [1, 2],
                        'price': [100, 150],
                        'name': ['Product1', 'Product2'],
                        'quantity': [1, 2]
                    }
                ),
                pd.DataFrame()
            )
        ],
        ids=[
            'Invalid ID type',
            'Missing data',
            'Negative int',
            'Missing col',
            'Valid data'
        ]
    )
    @unittest.mock.patch('pandas.io.json.to_json')
    def test_read_orders_save_invalid_data(
        self,
        to_json_mock: unittest.mock.MagicMock,
        data: pd.DataFrame,
        expected_errors_dataframe: pd.DataFrame
    ):
        report = self.get_report()
        report.data = data

        report.set_orders()

        if not expected_errors_dataframe.empty:
            to_json_mock.assert_called_once()
            file_path = VALIDATION_ERRORS_DIR_PATH / f'{TEST_REPORT_PATH.stem}_errors.json'

            assert to_json_mock.call_args.kwargs.get('obj').equals(expected_errors_dataframe)
            assert to_json_mock.call_args.kwargs.get('path_or_buf') == file_path
            assert to_json_mock.call_args.kwargs.get('orient') == 'records'
            assert to_json_mock.call_args.kwargs.get('default_handler') == str
            assert to_json_mock.call_args.kwargs.get('indent') == 4
            assert to_json_mock.call_args.kwargs.get('index') == False
        else:
            to_json_mock.assert_not_called()

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

    def test_get_col_sum_by(self):
        report = self.get_report()
        report.set_orders()
        report.set_price_cols()

        expected_data = pd.DataFrame({
            'name': ['Product1', 'Product2'],
            'quantity': [40, 20]
        })

        assert report.get_col_sum_by(col_name='name').equals(expected_data)

    @unittest.mock.patch('pandas.ExcelWriter', return_value=unittest.mock.MagicMock())
    @unittest.mock.patch('pandas.DataFrame.to_excel')
    def test_save(
        self,
        to_excel_mock: unittest.mock.MagicMock,
        excel_writer: unittest.mock.MagicMock,
    ):
        report = self.get_report()
        report.set_orders()
        report.set_price_cols()

        report.save()

        excel_writer.assert_called_once_with(path=PROJECT_ROOT_PATH / 'reports' / '2025_01_01_report.xlsx')

        expected_calls = [
            unittest.mock.call(
                unittest.mock.ANY,
                sheet_name='Report',
                index=False,
                header=True,
                startrow=1,
                startcol=0
            ),
            unittest.mock.call(
                unittest.mock.ANY,
                sheet_name='Report',
                index=False,
                header=True,
                startrow=1,
                startcol=len(report.data.columns) + 4
            )
        ]

        to_excel_mock.assert_has_calls(expected_calls)
        assert to_excel_mock.call_count == 2
