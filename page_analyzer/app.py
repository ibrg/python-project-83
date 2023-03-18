import os
import requests
from flask import (Flask, flash, get_flashed_messages, redirect,
                   render_template, request, url_for)

from .db import DB
from .validator import valid_url
from .utils import get_correct_url, check_seo, format_text


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = DB()
cur = db.connect()


@app.route('/')
def index():
    title = 'Анализатор страниц'
    return render_template('index.html', title=title)


@app.get('/urls')
def urls_list():
    query = '''
    SELECT DISTINCT ON (urls.id) urls.id, urls.name,
    MAX(url_checks.created_at),
    url_checks.status_code, url_checks.created_at FROM urls
    LEFT JOIN url_checks On urls.id = url_checks.url_id
    GROUP BY urls.id, url_checks.status_code, url_checks.created_at
    ORDER BY urls.id DESC
    '''
    db.execute(query)
    urls_list = cur.fetchall()
    return render_template(
        'urls/urls_list.html',
        urls_list=urls_list)


@app.post('/urls')
def urls():
    url = request.form.get('url', '')
    url = get_correct_url(url.strip())
    errors = valid_url(url)
    query = f"SELECT id FROM urls WHERE name='{url}'"\
            f" ORDER BY created_at DESC LIMIT 1"
    db.execute(query)

    if errors:
        return render_template(
            'urls/urls.html',
            url=url,
            messages=errors), 422

    url_id = cur.fetchone()
    if url_id is not None:
        flash('Страница уже существует', 'info')
    else:
        db.save(url)
        db.execute(query)
        url_id = cur.fetchone()
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_detail', id=url_id['id']))


@app.route('/urls/<id>')
def urls_detail(id):
    query = f"SELECT * FROM urls WHERE id = {id}"
    db.execute(query)
    url = cur.fetchone()

    query = f"SELECT * FROM url_checks WHERE url_id = {id}" \
            f" ORDER BY created_at DESC"
    db.execute(query)
    url_checks = cur.fetchall()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls/urls_detail.html',
        url=url,
        url_checks=url_checks,
        messages=messages)


@app.post('/urls/<id>/checks')
def urls_check(id):
    query_url = f"SELECT name FROM urls WHERE id = {id}"
    db.execute(query_url)
    link = cur.fetchone()['name']
    print('URL: --- ', link)
    resourse = None
    try:
        resourse = requests.get(link, timeout=5)

    except requests.exceptions.ConnectionError:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('urls_detail', id=id))

    status_code, h1, title, meta_desc = check_seo(resourse)

    query = " \
        INSERT INTO url_checks (url_id, status_code, h1, title, description)\
         VALUES ({id}, {code}, '{h1}', '{title}', '{meta_desc}')".format(
            id=id,
            code=status_code,
            h1=format_text(h1),
            title=format_text(title),
            meta_desc=format_text(meta_desc))
    db.execute(query)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_detail', id=id))
