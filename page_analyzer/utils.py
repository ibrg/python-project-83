from bs4 import BeautifulSoup as bs


def get_correct_url(url):
    if url[-1] in ['/', ' ']:
        return url[:-1]
    return url


def check_seo(resourse):
    content = resourse.text
    html = bs(content, 'html5lib')
    status_code = resourse.status_code
    h1 = html.find('h1').text if html.find('h1') else ''
    title = html.find('title').text if html.find('title') else ''
    meta_desc = html.find("meta", {"name": "description"})['content'] \
        if html.find("meta", {"name": "description"}) else ''
    return status_code, h1, title, meta_desc


def format_text(text: str):
    return text.strip().replace('\'', '`')
