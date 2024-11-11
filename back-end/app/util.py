from app import app
from flask import json
import re


def json_response(data, status):
    res = app.response_class(
        response=json.dumps(data),
        status=status,
        mimetype='application/json'
    )
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res


def url_root(url):
    regexp = re.compile(r'(www\.)?([\w\d-]+\.)+[\w]+(\/|$)')
    match = regexp.search(url)

    print(match, flush=True)

    if not match:
        return None

    root = match.group(0)

    root.removeprefix('www.')
    root.strip('/')

    return root


def name_from_url(url):

    matches = re.findall(r'[\w\d-]+\.', url)
    if not matches:
        return ''

    name = matches[-1][:-1]
    return name
