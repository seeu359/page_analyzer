from urllib.parse import urlparse


import validators


def is_valid_url(url: str) -> bool:
    return isinstance(validators.url(url), bool)


def get_normalize_url(url: str) -> str:
    scheme = urlparse(url).scheme
    netloc = urlparse(url).netloc
    return f'{scheme}://{netloc}'
