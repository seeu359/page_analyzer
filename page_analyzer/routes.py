from page_analyzer import db
from page_analyzer.services import get_normalize_url, is_valid_url

from flask import render_template, request, flash, redirect, url_for, Blueprint


routes = Blueprint('routes', __name__,)


@routes.route('/')
def main():
    return render_template('base.html')


@routes.post('/urls')
def urls(database: db.Database = db.Database()):
    url = request.form.get('url')

    if not is_valid_url(url):
        flash('Некорректный URL', 'error')
        return redirect(url_for('routes.main'))

    normalize_url = get_normalize_url(url)
    _id = database.insert('urls', normalize_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('routes.site', _id=_id), code=302)


@routes.route('/urls/<int:_id>')
def site(
        _id: int,
        database: db.Database = db.Database(),
):
    _site = database.select(_id)

    if _site is None:
        return redirect(url_for('routes.main'))

    return render_template('site.html', site=_site)


@routes.route('/urls')
def all_sites(database: db.Database = db.Database()):
    sites = database.select()
    return render_template('all_sites.html', sites=sites)


@routes.post('/urls/<int:_id>/checks')
def check_url(
        _id: int,
        database: db.Database = db.Database()
):
    database.insert('url_checks',)