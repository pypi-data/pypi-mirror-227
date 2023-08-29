import pathlib

import typer

from .translator import translate_module


def main(path: pathlib.Path = typer.Argument(..., help='путь до файла со сценарием или до директории со сценариями')):
    translate_module(path)


if __name__ == '__main__':
    typer.run(main)
