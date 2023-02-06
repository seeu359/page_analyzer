from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from page_analyzer import constants, db
from page_analyzer import services as s
from page_analyzer.exceptions import VerificationError

routes = Blueprint('routes', __name__,)


@routes.route('/')
def main():
    return render_template('base.html')


@routes.post('/urls')
def urls(database: db.Database = db.Database()):
    url = request.form.get('url')

    if not s.is_valid_url(url):
        flash(s.FlashMessages.INCORRECT_URL.value, constants.FLASH_ERROR)
        return render_template('base.html'), \
            constants.HTTP_422_UNPROCESSABLE_ENTITY

    normalize_url = s.get_normalize_url(url)

    with database as db_session:
        cursor = db_session.cursor()
        cursor.execute("""SELECT id FROM urls WHERE name=%s""",
                       (normalize_url,))
        site_id = cursor.fetchone()

        if not site_id:

            cursor.execute("""INSERT INTO urls (name, created_at)
                            VALUES (%s, %s)
                            RETURNING id;""",
                           (normalize_url,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            site_id = cursor.fetchone()
            cursor.execute("""INSERT INTO all_sites (url_id)
                                        VALUES (%s);""",
                           (site_id,))
            db_session.commit()

            flash(s.FlashMessages.PAGE_SUCCESSFULLY_ADDED.value,
                  constants.FLASH_SUCCESS)
        else:
            flash(s.FlashMessages.PAGE_ALREADY_EXIST.value,
                  constants.FLASH_NOTIFY)

    return redirect(url_for('routes.site', _id=site_id[0]))


@routes.route('/urls/<int:_id>')
def site(
        _id: int,
        database: db.Database = db.Database(),
):
    with database as db_session:
        cursor = db_session.cursor()
        cursor.execute("""SELECT * FROM urls
                        WHERE id=%s""",
                       (_id,))
        _site = cursor.fetchone()

        if _site is None:
            return redirect(url_for('routes.main'))

        cursor.execute("""SELECT * FROM url_checks
                        WHERE url_id=%s
                        ORDER BY created_at DESC""",
                       (_id,))
        site_check = cursor.fetchall()

    return render_template('site.html', site=_site, site_check=site_check)


@routes.route('/urls')
def all_sites(database: db.Database = db.Database()):
    with database as db_session:
        cursor = db_session.cursor()
        cursor.execute("""SELECT
                        all_sites.url_id,
                        urls.name,
                        all_sites.created_at,
                        all_sites.status_code
                        FROM all_sites
                        INNER JOIN urls ON all_sites.url_id = urls.id
                        ORDER BY urls.created_at DESC""")
        sites = cursor.fetchall()

    return render_template('all_sites.html', sites=sites)


@routes.post('/urls/<int:_id>/checks')
def check_url(
        _id: int,
        database: db.Database = db.Database(),
):
    with database as db_session:
        cursor = db_session.cursor()
        cursor.execute("""SELECT name FROM urls
                        WHERE id=%s""", (_id,))
        resource_url = cursor.fetchone()[0]
        try:
            status_code = s.get_status_code(resource_url)
        except VerificationError:
            flash(s.FlashMessages.VERIFICATION_ERROR.value,
                  constants.FLASH_ERROR)
            return redirect(url_for('routes.site', _id=_id))

        seo_info = s.get_seo_info(resource_url)
        cursor.execute("""INSERT INTO url_checks
                        (url_id, status_code, h1,
                        title, description, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                       (
                           _id, status_code, seo_info.h1, seo_info.title,
                           seo_info.content,
                           datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                       )
        cursor.execute("""UPDATE all_sites
                        SET created_at = %s, status_code = %s
                        WHERE url_id = %s""",
                       (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        status_code, _id))

        database.session.commit()
        flash(s.FlashMessages.PAGE_SUCCESSFULLY_CHECKED.value,
              constants.FLASH_SUCCESS)

    return redirect(url_for('routes.site', _id=_id))
