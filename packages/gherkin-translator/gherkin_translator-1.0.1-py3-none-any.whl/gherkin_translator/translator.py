import os
import pathlib
import re

MAPPING = (
    (r'Функционал:', 'Feature:'),
    (r'\s{2}Сценарий: |\s{2}Структура сценария: ', 'Scenario: '),
    (r'\s{4}Дано', 'Given'),
    (r'\s{4}Когда', 'When'),
    (r'\s{4}Тогда', 'Then'),
    (r'\s{4}И', 'And'),
    (r'^\s{6}\|', '  |'),
    (r'\s{4}Примеры:', 'Examples:'),
    (r'^\s{2}@', '@')
)


def translate_module(path: pathlib.Path):
    if path.is_dir():
        translate_suite(path)
    else:
        translate_file(path)


def translate_suite(path: pathlib.Path):
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith('.feature'):
                translate_file(pathlib.Path(dirpath) / filename)


def translate_file(filepath: pathlib.Path):
    with open(filepath, 'r') as file:
        content = file.read()

    content = translate(content)

    with open(filepath, 'w') as file:
        file.write(content)


def translate(value: str):
    for pattern, target in MAPPING:
        value = re.sub(pattern, target, value, flags=re.M)
    return value
