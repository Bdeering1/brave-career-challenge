from app import app, scraping
from flask import request, json


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/scrape')
def scrape_url():
    url = request.args.get('url')

    data = scraping.scrape(url)

    response = app.response_class(
        response=json.dumps(f'{data}'),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
