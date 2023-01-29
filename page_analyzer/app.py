from flask import Flask, redirect, render_template, request, url_for, flash

from page_analyzer import db
from page_analyzer.services import get_normalize_url, is_valid_url

app = Flask(__name__)
app.secret_key = 'super_secret'


@app.route('/')
def main():
    return render_template('base.html')


@app.post('/urls')
def urls(database: db.MainDatabase = db.MainDatabase()):
    url = request.form.get('url')

    if not is_valid_url(url):
        flash('Некорректный URL', 'error')
        return redirect(url_for('main'))

    normalize_url = get_normalize_url(url)
    _id = database.insert(normalize_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('site', _id=_id), code=302)


@app.route('/urls/<int:_id>')
def site(
        _id: int,
        database: db.MainDatabase = db.MainDatabase(),
):
    _site = database.select(_id)

    if _site is None:
        return redirect(url_for('main'))

    return render_template('site.html', site=_site)


@app.route('/urls')
def all_sites(database: db.MainDatabase = db.MainDatabase()):
    sites = database.select()
    return render_template('all_sites.html', sites=sites)
