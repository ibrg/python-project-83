import os

from flask import (Flask, flash, get_flashed_messages, redirect,
                   render_template, request, url_for)

from .db import DB
from .validator import valid_url

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
        SELECT urls.id, urls.name, url_checks.created_at
        FROM url_checks JOIN urls ON url_id = urls.id
        ORDER BY urls.id DESC;
    '''
    db.execute(query)
    urls_list = cur.fetchall()
    return render_template(
        'urls/urls_list.html',
        urls_list=urls_list)


@app.post('/urls')
def urls():
    url = request.form.get('url', '')
    errors = valid_url(url)
    if errors:
        return render_template(
            'urls/urls.html',
            url=url,
            messages=errors), 422
    db.save(url)
    query = f"SELECT id FROM urls WHERE name = '{url}'"\
            f" ORDER BY created_at DESC LIMIT 1"
    db.execute(query)
    url_id = cur.fetchone()[0]
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_detail', id=url_id))


@app.route('/urls/<id>')
def urls_detail(id):
    query = f"SELECT * FROM urls WHERE id = {id}"
    db.execute(query)
    url = cur.fetchone()

    query = f"SELECT * FROM url_checks WHERE url_id = {id}" \
            f"ORDER BY created_at DESC"
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
    query = f"INSERT INTO url_checks (url_id) VALUES ({id})"
    db.execute(query)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_detail', id=id))
