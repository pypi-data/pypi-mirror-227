import logging
import os
import pathlib

CERT_PREFIX = '-----BEGIN CERTIFICATE-----'
CERT_POSTFIX = '-----END CERTIFICATE-----'
SEGMENT_LENGTH = 65

logger = logging.getLogger(__name__)


def normalize_all_certs_in_dir(path: pathlib.Path):
    """Нормализовать все сертификаты в директории"""
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.cer'):
                logger.debug(f'Нормализация файла "{filename}"')
                try_normalize_cert(pathlib.Path(dirpath) / filename)


def try_normalize_cert(filepath: pathlib.Path):
    """Попытаться нормализовать файл сертификата"""
    try:
        normalize_cert(filepath)
    except UnicodeDecodeError:
        logger.error(f'Не удалось нормализовать сертификат "{filepath}". Возможно сертификат закодирован не в base64')


def normalize_cert(filepath: pathlib.Path):
    """Нормализовать файл сертификата"""
    with open(filepath, 'r') as file:
        content = file.read()

    content = content.strip()
    content = content.replace(CERT_PREFIX, '')
    content = content.replace(CERT_POSTFIX, '')

    segments = [content[i:i + SEGMENT_LENGTH].strip() for i in range(0, len(content), SEGMENT_LENGTH)]

    new_content = CERT_PREFIX + '\n' + '\n'.join(segments) + '\n' + CERT_POSTFIX

    with open(filepath, 'w') as file:
        file.write(new_content)
