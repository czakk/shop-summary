"""Generate a summary report."""

import pathlib

import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, LongTable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.constans import TABLE_STYLE, TOTAL_TABLE_STYLE
from src.report import Report
from src.utils import SUMMARY_PATH, TEMP_DIR_PATH


class Summary:
    def __init__(self, reports: list[Report]) -> None:
        self.reports: list[Report] = reports
        self.data: pd.DataFrame = pd.DataFrame()
        self.path = SUMMARY_PATH

        self._prepare_reports()

    def _prepare_reports(self) -> None:
        self.reports.sort(key=lambda r: r.date)

        for report in self.reports:
            report.set_orders()
            report.set_price_cols()
            report.save()

        self.data = pd.concat([report.data for report in self.reports], ignore_index=True)

    def _get_total_by_product_name(self) -> pd.DataFrame:
        return self.data.groupby('name')['total'].sum()

    def get_image_size(self, path: pathlib.Path | str) -> tuple[int, int]:
        with PILImage.open(path) as img:
            return img.size

    def save(self) -> None:
        list_data = [[col.title() for col in self.data.columns.tolist()]] + self.data.round(2).values.tolist()
        pdf = SimpleDocTemplate(str(self.path), pagesize=A4)

        title_date_range = ' - '.join([
            str(self.reports[0].date),
            str(self.reports[-1].date)
        ]) if len(self.reports) > 1 else self.reports[0].date

        title = Paragraph(f'Summary {title_date_range}', style=getSampleStyleSheet()['Title'])
        total_heading = Paragraph(f'Total', style=getSampleStyleSheet()['Heading2'])

        total = self.data.drop(columns=['id', 'quantity', 'TAX']).select_dtypes(include='number').sum()
        total_data = list(zip(['Net', 'Gross', 'Total'], [value.item() for value in total.round(2).values]))

        table = LongTable(
            list_data,
            style=TableStyle(TABLE_STYLE),
            colWidths=[50, 80, 50, 80, 50, 80, 80],
            repeatRows=1
        )
        total_table = Table(total_data, style=TableStyle(TOTAL_TABLE_STYLE), hAlign='LEFT')

        x = [str(report.date) for report in self.reports]
        y = [report.get_data_with_sum_row().tail(1)['total'].round(2).item() for report in self.reports]

        plt.figure(figsize=(8, 6))
        plt.plot(x, y, marker='o',)
        plt.xticks(rotation=45)
        for i in range(len(x)):
            plt.text(x[i], y[i], str(y[i]), ha='center', va='bottom')

        plot_title = Paragraph(f'Total income by a date', style=getSampleStyleSheet()['Heading2'])
        plot_path = f'{TEMP_DIR_PATH}/total_by_date.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight', transparent=True)
        width, height = self.get_image_size(plot_path)
        total_plot = Image(plot_path, width=width * .2, height=height * .2)

        total_by_name = self._get_total_by_product_name()
        sizes = total_by_name.round(2).tolist()
        labels = total_by_name.index.tolist()
        plt.figure(figsize=(10, 8))
        plt.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%'
        )
        plt.axis('equal')

        pie_plot_title = Paragraph(f'Total income by a product', style=getSampleStyleSheet()['Heading2'])
        pie_plot_path = f'{TEMP_DIR_PATH}/total_by_name.png'
        plt.savefig(pie_plot_path, dpi=300, bbox_inches='tight', transparent=True)
        width, height = self.get_image_size(pie_plot_path)
        total_pie_plot = Image(pie_plot_path, width=width * .2, height=height * .2)

        elements = [
            title,
            Spacer(1,12),
            table,
            Spacer(1,12),
            total_heading,
            total_table,
            Spacer(1,12),
        ]
        if len(self.reports) > 1:
            elements.extend([
                plot_title,
                total_plot,
                Spacer(1,12),
            ])
        elements.extend([
            pie_plot_title,
            total_pie_plot,
        ])

        pdf.build(elements)
