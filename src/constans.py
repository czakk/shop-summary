"""Project constants."""

from reportlab.lib import colors


XLSX_FILE_NAME_PATTERN = r'\d{4}_\d{2}_\d{2}\.xlsx'
DATE_FORMAT = '%Y_%m_%d'
DATA_DIR_NAME = 'data'
TAX_RATE = .23
TABLE_STYLE = [
    ('BACKGROUND', (0, 0), (-1, 0), colors.black),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 1, colors.white)
]
TOTAL_TABLE_STYLE = [
    ('BACKGROUND', (0, 0), (0, -1), colors.black),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('BACKGROUND', (1, 0), (-1, -1), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 1, colors.white)
]
TEMP_DIR_NAME = 'temp'
