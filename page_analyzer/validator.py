from urllib.parse import urlparse


def valid_url(url):
    correct_url = urlparse(url)
    errors = []
    if url == '':
        errors.append(("error", "URL обязателен"))
    if correct_url.scheme not in ['http', 'https'] or len(url) > 255:
        errors.append(("error", "Некорректный URL"))
    return errors
