from flask import Flask, redirect, render_template, request, url_for

from page_analyzer import db
from page_analyzer.services import get_normalize_url, is_valid_url

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('base.html')


@app.post('/urls')
def urls(database: db.MainDatabase = db.MainDatabase()):
    url = request.form.get('url')

    if not is_valid_url(url):
        return redirect(url_for('redirect_test'))

    normalize_url = get_normalize_url(url)
    database.insert(normalize_url)
    return redirect(url_for('main'), code=302)


@app.route('/urls/<int:id>')
def site(
        _id: int,
        database: db.MainDatabase = db.MainDatabase(),
):

    data = database.select(_id)

    if data is None:
        return redirect(url_for('main'))
    return data


@app.route('/urls')
def all_sites(database: db.MainDatabase = db.MainDatabase()):
    sites = database.select()
    return render_template('all_sites.html', sites=sites)
