import pathlib
import unittest.mock

import pandas as pd
import pytest

from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, LongTable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.constans import TABLE_STYLE, TOTAL_TABLE_STYLE
from src.summary import Summary
from src.report import Report
from src.utils import TEMP_DIR_PATH


@unittest.mock.patch('src.report.Report.save')
class TestSummary:
    @unittest.mock.patch('pandas.read_excel', side_effect=[
        pd.DataFrame({
            'id': [4, 5, 6],
            'name': ['Product1', 'Product3', 'Product5'],
            'price': [100.0, 180.0, 200.0],
            'quantity': [1, 30, 60]
        }),
        pd.DataFrame({
            'id': [3, 3, 3],
            'name': ['Product1', 'Product2', 'Product3'],
            'price': [100.0, 150.0, 100.0],
            'quantity': [10, 20, 30]
        }),
        pd.DataFrame({
            'id': [1, 1, 2],
            'name': ['Product1', 'Product2', 'Product1'],
            'price': [100.0, 150.0, 100.0],
            'quantity': [10, 20, 30]
        })
    ])
    def get_summary(self, *args, **kwargs) -> Summary:
        reports = [
            Report(
                pathlib.Path(f'2025_01_0{i}.xlsx'),
                datetime(2025, 1, i).date())
            for i in range(3, 0, -1)
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
            'price': [100.0, 150.0, 100.0,
                      100.0, 150.0, 100.0,
                      100.0, 180.0, 200.0],
            'quantity': [10, 20, 30,
                         10, 20, 30,
                         1, 30, 60],
            'TAX': [.23 for _ in range(9)],
            'gross': [123.0, 184.5, 123.0,
                      123.0, 184.5, 123.0,
                      123.0, 221.4, 246.0],
            'total': [1230.0, 3690.0, 3690.0,
                      1230.0, 3690.0, 3690.0,
                      123.0, 6642.0, 14760.0]
        })

        summary = self.get_summary()

        reports_expected_order = [datetime(2025, 1,  i).date() for i in range(1, 4)]
        assert [report.date for report in summary.reports] == reports_expected_order
        assert report_save_mock.call_count == 3
        assert summary.data.equals(expected_data)

    @pytest.mark.parametrize('reports_number', [1,2,3], ids=['One report', 'Two reports', 'Three reports'])
    @unittest.mock.patch.object(Image, '__repr__', return_value='Image obj')
    @unittest.mock.patch('reportlab.platypus.doctemplate.SimpleDocTemplate.build')
    @unittest.mock.patch('matplotlib.pyplot.plot')
    @unittest.mock.patch('matplotlib.pyplot.pie')
    @unittest.mock.patch('matplotlib.pyplot.savefig')
    @unittest.mock.patch('src.summary.Summary.get_image_size')
    def test_save(
        self,
        get_image_size: unittest.mock.MagicMock,
        savefig_mock: unittest.mock.MagicMock,
        pie_plot_mock: unittest.mock.MagicMock,
        plot_mock: unittest.mock.MagicMock,
        build_mock: unittest.mock.MagicMock,
        image_obj_mock: unittest.mock.MagicMock,
        report_save_mock: unittest.mock.MagicMock,
        reports_number: int,
    ):
        expected_title = [
            'Summary 2025-01-01',
            'Summary 2025-01-01 - 2025-01-02',
            'Summary 2025-01-01 - 2025-01-03'
        ][reports_number - 1]
        expected_table = [
            [
                [1, 'Product1', 100.0, 10, 0.23, 123.0, 1230.0],
                [1, 'Product2', 150.0, 20, 0.23, 184.5, 3690.0],
                [2, 'Product1', 100.0, 30, 0.23, 123.0, 3690.0]
            ],
            [
                [1, 'Product1', 100.0, 10, 0.23, 123.0, 1230.0],
                [1, 'Product2', 150.0, 20, 0.23, 184.5, 3690.0],
                [2, 'Product1', 100.0, 30, 0.23, 123.0, 3690.0],
                [3, 'Product1', 100.0, 10, 0.23, 123.0, 1230.0],
                [3, 'Product2', 150.0, 20, 0.23, 184.5, 3690.0],
                [3, 'Product3', 100.0, 30, 0.23, 123.0, 3690.0]
            ],
            [
                [1, 'Product1', 100.0, 10, 0.23, 123.0, 1230.0],
                [1, 'Product2', 150.0, 20, 0.23, 184.5, 3690.0],
                [2, 'Product1', 100.0, 30, 0.23, 123.0, 3690.0],
                [3, 'Product1', 100.0, 10, 0.23, 123.0, 1230.0],
                [3, 'Product2', 150.0, 20, 0.23, 184.5, 3690.0],
                [3, 'Product3', 100.0, 30, 0.23, 123.0, 3690.0],
                [4, 'Product1', 100.0, 1, 0.23, 123.0, 123.0],
                [5, 'Product3', 180.0, 30, 0.23, 221.4, 6642.0],
                [6, 'Product5', 200.0, 60, 0.23, 246.0, 14760.0]
            ]
        ][reports_number - 1]
        expected_total_table = [
            ['Net'] + [sum([data[2] for data in expected_table])],
            ['Gross'] + [sum([data[5] for data in expected_table])],
            ['Total'] + [sum([data[6] for data in expected_table])]
        ]
        expected_table.insert(0, ['Id', 'Name', 'Price', 'Quantity', 'Tax', 'Gross', 'Total'])
        expected_plot_calls = [
            unittest.mock.call(['2025-01-01'], [8610.0], marker='o'),
            unittest.mock.call(['2025-01-01', '2025-01-02'], [8610.0, 8610.0], marker='o'),
            unittest.mock.call(['2025-01-01', '2025-01-02', '2025-01-03'], [8610.0, 8610.0, 21525.0], marker='o'),
        ]
        expected_pie_plot_calls = [
            unittest.mock.call(
                [4920.0, 3690.0],
                labels=['Product1', 'Product2'],
                autopct='%1.1f%%'
            ),
            unittest.mock.call(
                [6150.0, 7380.0, 3690.0],
                labels=['Product1', 'Product2', 'Product3'],
                autopct='%1.1f%%'
            ),
            unittest.mock.call(
                [6273.0, 7380.0, 10332.0, 14760.0],
                labels=['Product1', 'Product2', 'Product3', 'Product5'],
                autopct='%1.1f%%'
            )
        ]
        get_image_size.return_value = (100, 100)

        summary = self.get_summary()
        summary.reports = summary.reports[:reports_number]
        summary.data = summary.data[:reports_number * 3]
        summary.save()

        expected_calls = [
            Paragraph(expected_title, style=getSampleStyleSheet()['Title']),
            Spacer(1, 12),
            LongTable(
                expected_table,
                style=TableStyle(TABLE_STYLE), colWidths=[50, 80, 50, 80, 50, 80, 80],
                repeatRows=1
            ),
            Spacer(1, 12),
            Paragraph('Total', style=getSampleStyleSheet()['Heading2']),
            Table(expected_total_table, style=TableStyle(TOTAL_TABLE_STYLE), hAlign='LEFT'),
            Spacer(1, 12),
        ]
        if reports_number > 1:
            expected_calls.extend([
                Paragraph(f'Total income by a date', style=getSampleStyleSheet()['Heading2']),
                Image(f'{TEMP_DIR_PATH}/total_by_date.png', width=550, height=250),
                Spacer(1, 12)
            ])
        expected_calls.extend([
            Paragraph(f'Total income by a product', style=getSampleStyleSheet()['Heading2']),
            Image(f'{TEMP_DIR_PATH}/total_by_name.png', width=100, height=200)
        ])

        assert get_image_size.call_count == 2
        assert str(build_mock.call_args) == str(unittest.mock.call(expected_calls))
        assert savefig_mock.call_count == 2
        assert plot_mock.call_args == expected_plot_calls[reports_number - 1]
        assert pie_plot_mock.call_args == expected_pie_plot_calls[reports_number - 1]
        report_save_mock.assert_called()
