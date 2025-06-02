"""Utils for the project."""

import pathlib
import re

import pandas as pd

from datetime import datetime
from faker import Faker

from src.constans import DATA_DIR_NAME, DATE_FORMAT


PROJECT_ROOT_PATH = pathlib.Path(__file__).parent.parent.resolve()
VALIDATION_ERRORS_DIR_PATH = PROJECT_ROOT_PATH / DATA_DIR_NAME / 'validation_errors'

faker = Faker()

FAKE_PRODUCTS = [
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

def dir_files(path: pathlib.Path, pattern: str = '*') -> list[pathlib.Path]:
    return [p for p in path.iterdir() if re.match(pattern, str(p.name))]

def generate_fake_data(rows=10) -> tuple[pd.DataFrame, pathlib.Path]:
    report_dest_path = pathlib.Path(
        PROJECT_ROOT_PATH /
        DATA_DIR_NAME /
        f'{faker.unique.date(pattern=DATE_FORMAT, end_datetime=datetime.now())}.xlsx')
    report = pd.DataFrame(columns=['id', 'name', 'quantity', 'price'])

    for i in range(1, rows + 1):
        report.loc[len(report)] = [
            i - 1 if (faker.boolean(chance_of_getting_true=25) and i > 1) else i,
            faker.word(ext_word_list=FAKE_PRODUCTS),
            faker.pydecimal(positive=True, min_value=1, max_value=9, right_digits=0),
            faker.pyfloat(positive=True, min_value=1, max_value=10000, right_digits=2)
        ]

    return report, report_dest_path
