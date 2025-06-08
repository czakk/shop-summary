import pandas as pd
import pathlib
import unittest.mock

from datetime import datetime

from src.summary import Summary
from src.report import Report


@unittest.mock.patch('src.report.Report.save')
class TestSummary:
    @unittest.mock.patch('pandas.read_excel', side_effect=[
        pd.DataFrame({
            'id': [1, 1, 2],
            'name': ['Product1', 'Product2', 'Product1'],
            'price': [100.0, 150.0, 100.0],
            'quantity': [10, 20, 30]
        }),
        pd.DataFrame({
            'id': [3, 3, 3],
            'name': ['Product1', 'Product2', 'Product3'],
            'price': [100.0, 150.0, 100.0],
            'quantity': [10, 20, 30]
        }),
        pd.DataFrame({
            'id': [4, 5, 6],
            'name': ['Product1', 'Product3', 'Product5'],
            'price': [100.0, 180.0, 200.0],
            'quantity': [1, 30, 60]
        })
    ])
    def get_summary(self, *args, **kwargs) -> Summary:
        reports = [
            Report(pathlib.Path(f'2025_01_0{i}.xlsx'), datetime(2025, 1, i).date()) for i in range(3, 0, -1)
        ]
        summary =  Summary(reports)

        return summary

    def test_init(
        self,
        report_save_mock: unittest.mock.MagicMock
    ):
        expected_data = pd.DataFrame({
            'id': [1, 1, 2, 3, 3, 3, 4, 5, 6],
            'name': ['Product1', 'Product2', 'Product1',
                     'Product1', 'Product2', 'Product3',
                     'Product1', 'Product3', 'Product5'],
            'price': [100.0, 150.0, 100.0, 100.0, 150.0, 100.0, 100.0, 180.0, 200.0],
            'quantity': [10, 20, 30, 10, 20, 30, 1, 30, 60],
            'TAX': [.23 for _ in range(9)],
            'gross': [123.0, 184.5, 123.0, 123.0, 184.5, 123.0, 123.0, 221.4, 246.0],
            'total': [1230.0, 3690.0, 3690.0, 1230.0, 3690.0, 3690.0, 123.0, 6642.0, 14760.0]
        })

        summary = self.get_summary()

        reports_expected_order = [datetime(2025, 1,  i).date() for i in range(1, 4)]
        assert [report.date for report in summary.reports] == reports_expected_order
        assert report_save_mock.call_count == 3
        assert summary.data.equals(expected_data)

    @unittest.mock.patch('reportlab.platypus.doctemplate.SimpleDocTemplate.build')
    def test_save(
        self,
        build_mock: unittest.mock.MagicMock,
        report_save_mock: unittest.mock.MagicMock
    ):
        summary = self.get_summary()

        summary.save()

        build_mock.assert_called_once()
        report_save_mock.assert_called()
