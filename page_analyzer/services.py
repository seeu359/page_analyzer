from enum import Enum
from typing import NamedTuple
from urllib.parse import urlparse

import bs4
import requests
import validators

from page_analyzer.exceptions import VerificationError

StatusCode = int


class UrlSEOInfo(NamedTuple):
    h1: str | None = None
    title: str | None = None
    content: str | None = None


class FlashMessages(Enum):
    INCORRECT_URL = 'Некорректный URL'
    PAGE_SUCCESSFULLY_ADDED = 'Страница успешно добавлена'
    PAGE_SUCCESSFULLY_CHECKED = 'Страница успешно проверена'
    VERIFICATION_ERROR = 'Произошла ошибка при проверке'
    PAGE_ALREADY_EXIST = 'Страница уже существует'


def is_valid_url(url: str) -> bool:
    return isinstance(validators.url(url), bool)


def get_normalize_url(url: str) -> str:
    scheme = urlparse(url).scheme
    netloc = urlparse(url).netloc
    return f'{scheme}://{netloc}'


def get_status_code(url: str) -> StatusCode:
    try:
        return requests.get(url).status_code
    except Exception:
        raise VerificationError(FlashMessages.VERIFICATION_ERROR.value)


def get_seo_info(url: str) -> UrlSEOInfo:
    data = requests.get(url).text
    parser = bs4.BeautifulSoup(data, 'html.parser')

    h1 = parser.h1.text if parser.h1 else ''
    title = parser.title.text if parser.title else ''
    meta = parser.find_all('meta')
    content = ''

    for tag in meta:
        if _have_tags_in_meta(tag):
            content = tag['content']

    return UrlSEOInfo(h1=h1, title=title, content=content)


def _have_tags_in_meta(tag: bs4.Tag) -> bool:
    content_tag = 'content'
    name_tag = 'name'
    name_tag_value = 'description'
    return content_tag in tag.attrs and name_tag in tag.attrs \
        and tag[name_tag] == name_tag_value
