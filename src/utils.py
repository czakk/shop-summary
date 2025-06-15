"""Utils for the project."""

import pandas as pd
import pathlib
import re

from datetime import datetime
from faker import Faker

from src.constans import DATA_DIR_NAME, DATE_FORMAT, TEMP_DIR_NAME


PROJECT_ROOT_PATH = pathlib.Path(__file__).parent.parent.resolve()
VALIDATION_ERRORS_DIR_PATH = PROJECT_ROOT_PATH / DATA_DIR_NAME / 'validation_errors'
SUMMARY_PATH = pathlib.Path(PROJECT_ROOT_PATH / 'Summary.pdf')
TEMP_DIR_PATH = pathlib.Path(PROJECT_ROOT_PATH / TEMP_DIR_NAME)

faker = Faker()

FAKE_PRODUCT_NAMES = [
    'AeroFlare',
    'QuantumBlend',
    'SolarPure',
    'EcoSphere',
    'VertexOne',
    'LumeTrack',
    'VitalBloom',
    'PulseCore',
    'OptiWave',
    'CrystalVibe',
    'ZenithPro',
    'FusionCraft',
    'NovaLite',
    'HyperShield',
    'PrismEdge',
    'GlideStream',
    'NimbusTouch',
    'AquaLuxe',
    'SkyBound',
    'ElementFlow'
]

fake_products = [
    {'name': name, 'price': faker.pyfloat(positive=True, min_value=1, max_value=10000, right_digits=2)}
    for name in FAKE_PRODUCT_NAMES
]

def dir_files(path: pathlib.Path, pattern: str = '*') -> list[pathlib.Path]:
    return [p for p in path.iterdir() if re.match(pattern, str(p.name))]

def generate_fake_data(order_id_start: int, rows=10) -> tuple[pd.DataFrame, pathlib.Path]:
    if order_id_start < 0:
        raise ValueError('order_id_start must be >= 0')

    report_dest_path = pathlib.Path(
        PROJECT_ROOT_PATH /
        DATA_DIR_NAME /
        f'{faker.unique.date(pattern=DATE_FORMAT, end_datetime=datetime.now())}.xlsx')
    report = pd.DataFrame(columns=['id', 'name', 'quantity', 'price'])

    ids = []
    for i in range(order_id_start, order_id_start + rows):
        if i > order_id_start and faker.boolean(chance_of_getting_true=25):
            id = ids[-1]
        else:
            id = ids[-1] + 1 if ids and ids[-1] + 1 != i else i
        ids.append(id)

    for id in ids:
        product = faker.random_element(fake_products)

        report.loc[len(report)] = [
            id,
            product['name'],
            faker.pydecimal(positive=True, min_value=1, max_value=9, right_digits=0),
            product['price']
        ]

    return report, report_dest_path
