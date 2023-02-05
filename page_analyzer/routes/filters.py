from datetime import datetime

from flask import Blueprint, render_template

filters = Blueprint('filters', __name__)

HTTP_404_NOT_FOUND = 404


@filters.app_template_filter('datetime_format')
def datetime_format(date: datetime, _format='%Y-%m-%d'):
    return date.strftime(_format)


@filters.errorhandler(HTTP_404_NOT_FOUND)
def page_not_found(error):
    return render_template('components/errors/404.html'), HTTP_404_NOT_FOUND
