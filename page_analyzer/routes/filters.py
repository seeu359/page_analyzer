from datetime import datetime

from flask import Blueprint, render_template
from page_analyzer.constants import HTTP_404_NOT_FOUND

filters = Blueprint('filters', __name__)


@filters.app_template_filter('datetime_format')
def datetime_format(date: datetime, _format='%Y-%m-%d'):
    return date.strftime(_format)


@filters.errorhandler(HTTP_404_NOT_FOUND)
def page_not_found(error):
    return render_template('components/errors/404.html'), HTTP_404_NOT_FOUND
