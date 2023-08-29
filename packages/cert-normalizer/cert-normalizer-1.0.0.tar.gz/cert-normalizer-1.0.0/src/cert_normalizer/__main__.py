import pathlib

import typer

from .normalizer import normalize_all_certs_in_dir, normalize_cert


def main(path: pathlib.Path = typer.Argument(..., help='путь до файла сертификата или до директории с сертификатами')):
    if path.is_dir():
        normalize_all_certs_in_dir(path)
    else:
        normalize_cert(path)


if __name__ == '__main__':
    typer.run(main)
