def get_correct_url(url):
    if url[-1] in ['/', ' ']:
        return url[:-1]
    return url
