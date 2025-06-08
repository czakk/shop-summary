"""Generate a summary report."""

import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, LongTable, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from src.constans import TABLE_STYLE, TOTAL_TABLE_STYLE
from src.report import Report
from src.utils import SUMMARY_PATH


class Summary:
    def __init__(self, reports: list[Report]):
        self.reports: list[Report] = reports
        self.data: pd.DataFrame = pd.DataFrame()
        self.path = SUMMARY_PATH

        self._prepare_reports()

    def _prepare_reports(self):
        for report in self.reports:
            report.set_orders()
            report.set_price_cols()
            report.save()

        self.data = pd.concat([report.data for report in self.reports], ignore_index=True)
        self.reports.sort(key=lambda r: r.date)

    def save(self):
        list_data = [[col.title() for col in self.data.columns.tolist()]] + self.data.round(2).values.tolist()
        table_style = TableStyle(TABLE_STYLE)
        pdf = SimpleDocTemplate(str(self.path), pagesize=A4)

        title_date_range = ' - '.join([
            str(self.reports[0].date),
            str(self.reports[-1].date)
        ]) if len(self.reports) > 1 else self.reports[0].date
        title = Paragraph(f'Summary {title_date_range}', style=getSampleStyleSheet()['Title'])
        total_heading = Paragraph(f'Total', style=getSampleStyleSheet()['Heading2'])

        table = LongTable(list_data, style=table_style, colWidths=[50, 80], repeatRows=1)
        total = self.data.drop(columns=['id', 'quantity', 'TAX']).select_dtypes(include='number').sum()
        total_data = list(zip(['Net', 'Gross', 'Total'], [*total.round(2).values.T]))
        total_table = Table(total_data, style=TableStyle(TOTAL_TABLE_STYLE), hAlign='LEFT')

        elements = [
            title,
            Spacer(1,12),
            table,
            Spacer(1,12),
            total_heading,
            total_table
        ]
        pdf.build(elements)
