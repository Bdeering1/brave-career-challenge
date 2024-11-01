import re
import requests
from requests_html import HTMLSession


def scrape(url):
    session = HTMLSession()

    try:
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        return str(e)

    title = response.html.find('title')
    if title is None or len(title) == 0:
        title = name_from_url(url)
    else:
        title = title[0].text

    desc = response.html.xpath('//meta[@name="description"]/@content', first=True)
    if desc is None:
        desc = ''

    return [title, desc]


def name_from_url(url):
    matches = re.findall(r'[\w\d]+\.', url)
    if not matches:
        return ''

    name = matches[-1][:-1]
    return name
